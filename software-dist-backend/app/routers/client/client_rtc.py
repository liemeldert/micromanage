import asyncio
import json
from urllib.request import Request

import redis

from fastapi import status, APIRouter, Security, WebSocket, WebSocketDisconnect, Request
from fastapi_auth0 import Auth0User
from sse_starlette.sse import EventSourceResponse

from app.internal import database
from app.internal.config import REDIS_URL, REDIS_PORT, REDIS_PASSWORD
from app.internal.models import Organization, Site
from app.internal.utils import auth
from app.internal import tasks

redisClient = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWORD)

router = APIRouter()


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@router.get('/pns')
async def message_stream(request: Request):
    """
    SSE endpoint for event push notifications
    :param request:
    :return:
    """
    def device_called():
        """Check for device in event queue"""

        events = redisClient.lpop('device_id')
        yield 'Hello World'
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if device_called():
                yield {
                        "event": "new_message",
                        "id": "message_id",
                        "retry": RETRY_TIMEOUT,
                        "data": "message_content"
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


@router.websocket("/{device_id}/ws")
async def websocket_endpoint(websocket: WebSocket, device_id:int):
    """
    Endpoint for client websocket connections
    :param device_id:
    :param websocket:
    """
    await websocket.accept()
    try:
        while True:
            
    except WebSocketDisconnect:
        print("defenestrating client")
        await websocket.close()
