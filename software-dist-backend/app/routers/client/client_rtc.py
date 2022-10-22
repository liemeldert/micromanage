import asyncio
import datetime
import json
import pickle
from urllib.request import Request

import pymongo as pymongo
import redis
from app.internal.models import Task

from fastapi import status, APIRouter, Security, WebSocket, WebSocketDisconnect, Request
from fastapi_auth0 import Auth0User
from sse_starlette.sse import EventSourceResponse

from app.internal import database
from app.internal.config import REDIS_URL, REDIS_PORT, REDIS_PASSWORD, MONGO_URI
from app.internal.models import Organization, Site, Device
from app.internal.utils import auth
from app.internal import tasks

router = APIRouter()

# @router.get('/{device_id}/epns')
# async def message_stream(request: Request, device_id: int):
#     """
#     SSE endpoint for event push notifications
#     :param device_id: ID of the device, probably SN
#     :param request:
#     :return:
#     """
#     def device_called():
#         """Check for device in event queue"""
#
#         device = await Device.find_one(Device.id == device_id)
#
#         yield event
#
#     async def event_generator():
#         while True:
#             # If client closes connection, stop sending events
#             if await request.is_disconnected():
#                 break
#
#             # Checks for new messages and return them to client if any
#             if device_called():
#                 yield {
#                         "message": "connect to websocket"
#                 }
#
#             await asyncio.sleep(STREAM_DELAY)
#
#     return EventSourceResponse(event_generator())


@router.websocket("/{device_id}/ws/")
async def websocket_endpoint(websocket: WebSocket, device_id: int) -> None:
    """
    Endpoint for client websocket connections. Used when a command needs a response, such as getting the
    state of a currently installed application or install progress.
    :param device_id: ID of the device, probably SN
    :param websocket:
    """
    device: Device | None = await Device.find_one(Device.id == device_id)
    if device is None:
        return status.HTTP_404_NOT_FOUND
    await websocket.accept()
    current_operations = []
    try:
        while True:
            async def recieve_events() -> None:
                """Device event reciever"""
                await device.update()
                device_tasks: list[Task] = sorted(device.tasks, key=lambda x: x.task_id)
                for task in device_tasks:
                    if task.status == 0:
                        await websocket.send_text("is installed: " )
                        await websocket.send_json(task.json())
                        task.status = 1
                        break
                device.tasks = device_tasks
                await device.save()

            async def recieve_messages():
                """On message recieved"""
                command = await websocket.receive_text()
                if command == "task update":
                    message = json.loads(await websocket.receive_json())
                    await device.update()
                    for each in device.tasks:
                        if each.task_id == message['task_id']:
                            task = each
                            break

            events_task = asyncio.create_task(recieve_events)
            messages_task = asyncio.create_task(recieve_messages)

            await events_task
            await messages_task

    except WebSocketDisconnect:
        await websocket.close()
        # set device state to be disconnected
        # maybe should be changed later to differentiate between clean shutdown and a crash
        device.state = 0
        await device.save()
