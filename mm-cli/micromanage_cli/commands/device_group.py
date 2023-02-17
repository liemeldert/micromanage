import aiohttp
import typer
from util.models import DeviceGroup
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "device_groups": "/device-groups"
}

@app.command()
def create(
    name: str,
    description: str,
    members: list = [],
    applications: list = [],
    site: str = None,
    is_admin: bool = False
):
    """
    Create a new device group
    """
    device_group = DeviceGroup(
        name=name,
        description=description,
        members=members,
        applications=applications,
        site=site
    )
    response = api_request("POST", routes["device_groups"], data=device_group.dict())
    if response.status == 201:
        typer.echo("Device group created successfully")
    else:
        typer.echo("Error creating device group")

if __name__ == "__main__":
    app()

