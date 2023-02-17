import aiohttp
import typer
from util.models import User
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "users": "/users"
}

# Helper function to make authenticated requests to the API
async def api_request(method, route, data=None):
    headers = {
        "Authorization": f"Bearer {get_config().key}",
        "Content-Type": "application/json"
    }
    url = base_url + route
    with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, json=data) as response:
            return response

# CLI commands for the User model
@app.command()
def create(
    name: str,
    pronouns: str,
    email: str,
    avatar: str,
    plan: int,
    created_at: str,
    organization: str,
    is_admin: bool = False
):
    """
    Create a new user
    """
    user = User(
        name=name,
        pronouns=pronouns,
        email=email,
        avatar=avatar,
        plan=plan,
        created_at=created_at,
        organization=organization,
        is_admin=is_admin
    )
    response = api_request("POST", routes["users"], data=user.dict())
    if response.status == 201:
        typer.echo("User created successfully")
    else:
        typer.echo("Error creating user")

if __name__ == "__main__":
    app()
