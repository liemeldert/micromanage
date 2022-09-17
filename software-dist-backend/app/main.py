import motor
from beanie import init_beanie
from fastapi import FastAPI, Depends

from .internal.config import MONGO_URI
from .internal.models import User
from .internal.utils import auth
from .routers import site, socket, org

app = FastAPI()
app.include_router(site.router)
app.include_router(socket.router)
app.include_router(org.router)


@app.on_event("startup")
async def init():
    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URI
    )

    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[User])


@app.get("/ping")
async def ping() -> dict:
    """returns a pong if the server is alive

    Returns:
        dict: pong
    """
    return {"message": "pong"}


@app.get("/private/ping")
def private_ping(user=Depends(auth.implicit_scheme)):
    """
    A valid access token is required to access this route

    user: Auth0User, required, access token
    """
    return {"message": "pong"}
