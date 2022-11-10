import asyncio
import json
import json
import threading
from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect
from app.internal import s3
from app.internal.models import Device, Task

router = APIRouter()


@router.websocket("/{tenant_id}/{device_id}/ws/")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str, device_id: str) -> None:
    """
    Endpoint for client websocket connections. Used when a command needs a response, such as getting the
    state of a currently installed application or install progress.
    :param device_id: ID of the device, probably SN
    :param tenant_id: ID of the tenant the device belongs to
    :param websocket:
      """
    device: Device | None = await Device.find_one(Device.id == device_id and Device.tenant == tenant_id)
    if device is None:
        return status.HTTP_404_NOT_FOUND
    await websocket.accept()
    try:
        # Receive initial message from client
        system = json.loads(await websocket.receive_json())
        device.system = system
        running = True

        async def send_events(websocket, device: Device) -> None:
            """Device event receiver"""
            while running:
                await asyncio.sleep(10)
                await device.update()
                # Generate tasks
                device_tasks: list[Task] = sorted(device.tasks, key=lambda x: x.task_id)
                for index, task in enumerate(device_tasks):
                    if task.status == 0:
                        # application = Application(**task.application)
                        await websocket.send_text("is installed:")
                        await websocket.send_json(task.json())
                        resp = await websocket.receive_text()
                        if resp == "installed: false":
                            task.status = 1
                        elif resp == "installed: true":
                            task.status = 4
                        device.tasks = device_tasks
                        await device.save()
                        await websocket.send_text("install:" + s3.create_presigned_url("packages", task.package.id))
                        while True:
                            # check for update in task status
                            resp = await websocket.receive_text()
                            if resp == "install: complete":
                                device_tasks.remove(task)
                                break
                            if resp == "install: failed":
                                task.status = 4
                                device.tasks = device_tasks
                                await device.save()
                                break
                            if resp == "install: downloading":
                                task.status = 2
                            elif resp == "install: installing":
                                task.status = 3
                            device.tasks = device_tasks
                            await device.save()
                await device.save()

        async def receive_messages(websocket, device: Device) -> None:
            """On message received"""
            while running:
                command = await websocket.receive_text()
                if command in ["shutdown", "restart", " sleep", "update"]:
                    device.state = command
                    await device.update()

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
