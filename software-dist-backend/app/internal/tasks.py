import asyncio
import pickle

import pymongo
import redis
import datetime
from .config import MONGO_URI, REDIS_URL, REDIS_PORT, REDIS_PASSWORD
from typing import Optional
from pydantic import EmailStr
from redis_om import HashModel
from models import Device, Organization, Site, Task

rClient = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,)

callbacks = {}

mongo = pymongo.MongoClient(MONGO_URI)


async def add_device(device_id: int, command: str, org: str = None, site: str = None):
    """Adds a task to a device's queue.

    Args:
        org (str): ID for an organization that owns the device
        device_id (int): ID for the specific device to give a task
        site (int): ID for the site the device should go to.
        command (str): Command to execute on device.

    Raises:
        FileNotFoundError: Device ID not found in database.
    """

    if org or site is not None:
        organization = await Organization.find_one(Organization.id == org)
        site = await Site.find_one(Site.id == site)
        # coplilot keeps adding the weirdest asf stuff
        device = await Device.find_one(Device.id == device_id)
        device = Device(name=device_id, site=site, organization=organization)  # jooooe biden
        await device.save()

    else:
        device = await Device.find_one(Device.id == device_id)  # scoliosis


def get_newest_task(device_id):
    """Gets the latest task from the queue"""
    queue = redisClient.get(device_id)
    events = pickle.loads(queue)
    return events[-1]


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

# async def register_callback(device_id, callback) -> None:
#     """
#     Calls callback function when a new task is available
#     :param device_id:
#     :param callback:
#     :return:
#     """
#     callbacks[device_id] = callback
#
#
# async def unregister_callback(device_id) -> None:
#     """
#     Unregisters a callback function
#     :param device_id:
#     :return:
#     """
#     if device_id in callbacks:
#         callbacks[device_id] = None


async def callback_loop() -> None:
    """
    Checks for new tasks in the queue and calls the callback function
    :return:
    """
    while True:
        for device_id in callbacks:
            task = await get_task(device_id)
            if task is not None:
                await callbacks[device_id](task)
        await asyncio.sleep(0.1)
