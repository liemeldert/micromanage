import asyncio
import datetime
import json
import threading
from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect
from app.internal import s3
from app.internal.models import Device, Task, Tenant

router = APIRouter()


async def exec_task(device: Device, task: Task, websocket: WebSocket) -> None:
    """
    Executes a task on a device. Does not check for task time, so make sure you implement that condition if needed.
    Args:
        device: device object
        task: task object
        websocket: websocket connection to send messages to

    Returns:

    """
    device_tasks: list[Task] = sorted(device.tasks, key=lambda x: x.task_id)  # doesn't hurt to sort again.
    await websocket.send_text("installed:")
    await websocket.send_json(task.package.json())
    resp = await websocket.receive_text()
    if resp == "True":
        device_tasks.remove(task)
        device.tasks = device_tasks
        await device.save()
        return

    # todo: implement usage of location specific s3 buckets, shouldn't be too bad??
    await websocket.send_text("install:" + s3.create_presigned_url("mmpkgstore-va", task.package.id))
    while True:
        # check for update in task status
        resp = await websocket.receive_text()
        if resp == "istatus: complete":
            device_tasks.remove(task)
            break
        #
        if resp == "istatus: failed":
            task.status = 4
            device.tasks = device_tasks
            await device.save()
            break
        if resp == "istatus: downloading":
            task.status = 2
        elif resp == "istatus: installing":
            task.status = 3
        device.tasks = device_tasks
        await device.save()


@router.websocket("/{tenant_id}/{device_id}/ws/")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str, device_id: str) -> None:
    """
    Endpoint for client websocket connections. Used when a command needs a response, such as getting the
    state of a currently installed application or install progress.
    :param device_id: ID of the device, probably SN
    :param tenant_id: ID of the tenant the device belongs to
    :param websocket:
    """
    tenant: Tenant = await Tenant.find_one({"id": tenant_id})
    device: Device = await Device.find_one(Device.id == device_id and Device.tenant == tenant_id)

    if tenant.autoenroll and device is not None:
        device = Device(tenant=tenant_id)

    if device is None:
        return status.HTTP_404_NOT_FOUND
    await websocket.accept()
    try:
        # Receive initial message from client
        system = json.loads(await websocket.receive_json())

        # set device system info
        device.hostname = system["hostname"]
        device.serial = system["serial"]
        device.model = system["model"]
        device.os_version = system["os_version"]
        device.os_build = system["os_build"]
        device.processor = system["processor"]
        await device.save()

        async def send_events(websocket, device: Device) -> None:
            """Device event receiver"""
            while running:
                await asyncio.sleep(10)
                await device.update()
                # Generate tasks
                device_tasks: list[Task] = sorted(device.tasks, key=lambda x: x.task_id)
                for index, task in enumerate(device_tasks):
                    if task.status == 0 and task.exec_time <= datetime.datetime.now():
                        await exec_task(device, task, websocket)
                await device.save()

        async def receive_messages(websocket, device: Device) -> None:
            """On message received"""
            while running:
                command = await websocket.receive_text()
                if command in ["shutdown", "restart", "update"]:
                    device.state = command
                    await device.update()
                if command == "sleep":
                    device.state = "sleep"
                    await device.update()
                    if not device.laptop:
                        for task in device.tasks:
                            if task.status == 0:
                                await exec_task(device, task, websocket)
                    websocket.send_text("sleep")

        # Create threads to both receive when devices go offline and to send installs
        events = threading.Thread(target=send_events, args=(websocket, device), daemon=True)
        messages = threading.Thread(target=receive_messages, args=(websocket, device), daemon=True)
        events.start()
        messages.start()
    except WebSocketDisconnect:
        await websocket.close()
        running = False
        device.state = None
        await device.save()
