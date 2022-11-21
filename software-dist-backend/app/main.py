import logging

import motor
from beanie import init_beanie
from fastapi import FastAPI, Depends
from fastapi_auth0 import Auth0User

from .internal.config import MONGO_URI
from .internal.models import *
from .internal.utils import auth
from .routers import tentant, org, application, device
from .routers.client import client_rtc

app = FastAPI()
app.include_router(tentant.router)
app.include_router(client_rtc.router)
app.include_router(application.router)
app.include_router(org.router)
app.include_router(device.router)

logging.basicConfig(level=logging.DEBUG)


@app.on_event("startup")
async def init():
    """Function that runs on startup.
    """
    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URI
    )

    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[User, MacPackage, MacScript,
                                                                Tenant, Organization, Device,
                                                                Application, DeviceGroup])


@app.get("/ping")
async def ping() -> dict:
    """returns a pong if the server is alive
    Returns:
        dict: pong
    """
    return {"message": "pong"}


@app.get("/private/ping")
def private_ping(user: Auth0User = Depends(auth.implicit_scheme)):
    """
    A valid access token is required to access this route
    user: Auth0User, required, access token
    """
    return {"message": "pong", "user": user.id}
