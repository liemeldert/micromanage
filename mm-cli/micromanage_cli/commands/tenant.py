import aiohttp
import typer
from util.models import Tenant
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "tenants": "/tenants"
}

# Helper function to make authenticated requests to the API
async def api_request(method, route, data=None):
    headers = {
        "Authorization": f"Bearer {get_config().key}",
        "Content-Type": "application/json"
    }
    url = base_url + route
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, json=data) as response:
            return response

# CLI commands for the Tenant model
@app.command()
def create(
    name: str,
    description: str,
    storing: str,
    organization: str,
    autoenroll: bool = False,
    is_admin: bool = False
):
    """
    Create a new tenant
    """
    tenant = Tenant(
        name=name,
        description=description,
        storing=storing,
        organization=organization,
        autoenroll=autoenroll,
        is_admin=is_admin
    )
    response = await api_request("POST", routes["tenants"], data=tenant.dict())
    if response.status == 201:
        typer.echo("Tenant created successfully")
    else:
        typer.echo("Error creating tenant")

if __name__ == "__main__":
    app()
import aiohttp
import typer
from util.models import Organization
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "organizations": "/organizations"
}

# Helper function to make authenticated requests to the API
async def api_request(method, route, data=None):
    headers = {
        "Authorization": f"Bearer {get_config().key}",
        "Content-Type": "application/json"
    }
    url = base_url + route
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, json=data) as response:
            return response

# CLI commands for the Organization model
@app.command()
def create(
    name: str,
    description: str = "",
    email_domain: str = None,
    users: list = [],
    admins: list = [],
    plan: int = 0,
    tenants: list = [],
    is_admin: bool = False
):
    """
    Create a new organization
    """
    organization = Organization(
        name=name,
        description=description,
        email_domain=email_domain,
        users=users,
        admins=admins,
        plan=plan,
        tenants=tenants
    )
    response = api_request("POST", routes["organizations"], data=organization.dict())
    if response.status == 201:
        typer.echo("Organization created successfully")
    else:
        typer.echo("Error creating organization")

if __name__ == "__main__":
    app()