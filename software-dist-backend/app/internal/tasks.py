import asyncio

import redis
import datetime
from .config import REDIS_URL, REDIS_PORT, REDIS_PASSWORD
from typing import Optional
from pydantic import EmailStr
from redis_om import HashModel
from models import Task

rClient = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,)

callbacks = {}


async def register_callback(device_id, callback) -> None:
    """
    Calls callback function when a new task is available
    :param device_id:
    :param callback:
    :return:
    """
    callbacks[device_id] = callback


async def unregister_callback(device_id) -> None:
    """
    Unregisters a callback function
    :param device_id:
    :return:
    """
    if device_id in callbacks:
        callbacks[device_id] = None


async def callback_loop() -> None:
    """
    Checks for new tasks in the queue and calls the callback function
    :return:
    """
    while True:
        for device_id in callbacks:
            if callbacks[device_id] is not None:
                task = rClient.lpop(device_id)
                if task is not None:
                    callbacks[device_id](task)
        await asyncio.sleep(0.1)
