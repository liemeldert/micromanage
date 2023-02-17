import aiohttp
import typer
from util.models import Device
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "devices": "/devices"
}

@app.command()
def create(
    name: str,
    serial: str,
    tenant_id: str,
    system: str = None,
    tags: list = [],
    group_id: str = None,
    laptop: bool = False,
    is_admin: bool = False
):
    """
    Create a new device
    """
    device = Device(
        name=name,
        serial=serial,
        tenant_id=tenant_id,
        system=system,
        tags=tags,
        group_id=group_id,
        laptop=laptop
    )
    response = api_request("POST", routes["devices"], data=device.dict())
    if response.status == 201:
        typer.echo("Device created successfully")
    else:
        typer.echo("Error creating device")

if __name__ == "__main__":
    app()
