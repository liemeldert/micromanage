import asyncio
import datetime
import json
import logging
import threading

from beanie import PydanticObjectId
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
    await websocket.send_text("install:")
    await websocket.send_text(task.json())
    await websocket.send_text(s3.create_presigned_url("mmpkgstore-va", str(task.package.id)))
    while True:
        # check for update in task status
        # todo: maybe add some sort of timeout
        resp = await websocket.receive_text()
        if resp == "istatus: complete":
            device_tasks.remove(task)
            device.tasks = device_tasks
            await device.save()
            break
        #
        if resp == "istatus: failed":
            task.status = 4
            task.last_update_time = datetime.datetime.now()
            device.tasks = device_tasks
            await device.save()
            break
        if resp == "istatus: downloading":
            task.status = 2
        elif resp == "istatus: installing":
            task.status = 3
        task.last_update_time = datetime.datetime.now()
        device.tasks = device_tasks
        await device.save()


@router.websocket("/ws/{tenant_id}/{device_serial}")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str, device_serial: str,
                             device_id: PydanticObjectId = None) -> None:
    """
    Endpoint for client websocket connections. Used when a command needs a response, such as getting the
    state of a currently installed application or install progress.
    :param device_id: ID of the device, probably SN
    :param tenant_id: ID of the tenant the device belongs to
    :param websocket:

    Args:
        device_serial:
    """
    running = True
    print(tenant_id, device_serial)
    tenant: Tenant = await Tenant.get(PydanticObjectId(tenant_id))
    if device_serial.startswith("devidsep"):
        device: Device = await Device.get(PydanticObjectId(str(device_serial)[8:]))
    else:
        device: Device = await Device.find_one(
            Device.serial == device_serial, Device.tenant_id == PydanticObjectId(tenant_id))
    print(tenant.id, device.id)

    if tenant is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return status.HTTP_404_NOT_FOUND

    if tenant.autoenroll and device is None:
        device = Device(tenant=tenant_id, serial=device_serial)

    if device is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return status.HTTP_404_NOT_FOUND
    await websocket.accept()
    try:
        # set device system info
        device.system = await websocket.receive_text()
        await device.save()

        async def send_events(websocket, device: Device) -> None:
            """Device event receiver"""
            while running:
                try:
                    await asyncio.sleep(10)
                    logging.debug("updating: " + str(device.id))
                    # await device.update()
                    # Generate tasks
                    device_tasks: list[Task] = sorted(device.tasks, key=lambda x: x.task_id)
                    for index, task in enumerate(device_tasks):
                        if task.status == 0 and task.exec_time <= datetime.datetime.now() \
                                or (task.last_update_time - datetime.datetime.now()).seconds > 30 * 60:
                            await exec_task(device, task, websocket)
                    await device.save()
                except WebSocketDisconnect:
                    print("oh dear!")  # this should be removed.
                    break

        async def receive_messages(websocket, device: Device) -> None:
            """On message received"""
            while running:
                try:
                    command = await websocket.receive_text()
                    if command in ["shutdown", "restart", "update"]:
                        device.state = command
                        # await device.update()
                    if command == "sleep":
                        device.state = "sleep"
                        # await device.update()
                        if not device.laptop:
                            for task in device.tasks:
                                if task.status == 0:
                                    await exec_task(device, task, websocket)
                        websocket.send_text("sleep")
                except WebSocketDisconnect:
                    print("oh no!")
                    break

        # await asyncio.gather(send_events(websocket, device), receive_messages(websocket, device))

        await asyncio.gather(send_events(websocket, device))

        # Create threads to both receive when devices go offline and to send installs
        # events = threading.Thread(target=asyncio.run, args=(send_events(websocket, device),), daemon=True)
        # messages = threading.Thread(target=asyncio.run, args=(receive_messages(websocket, device),), daemon=True)
        # try:
        #     events.start()
        #     messages.start()
        # except Exception as e:
        #     print(e)
        running = False
        print("씨발!!")
    except WebSocketDisconnect:
        await websocket.close()
        running = False
        device.state = None
        await device.save()
