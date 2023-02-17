import aiohttp
import typer
from util.models import Task
from util.config import get_config

app = typer.Typer()

# Routes for the different endpoints
routes = {
    "tasks": "/tasks"
}


# CLI commands for the Task model
@app.command()
def create(
    task_id: int,
    command: str,
    application: str,
    package: str,
    status: int = 0,
    status_reason: str = None,
    is_admin: bool = False
):
    """
    Create a new task
    """
    task = Task(
        task_id=task_id,
        command=command,
        application=application,
        package=package,
        status=status,
        status_reason=status_reason
    )
    response = api_request("POST", routes["tasks"], data=task.dict())
    if response.status == 201:
        typer.echo("Task created successfully")
    else:
        typer.echo("Error creating task")

if __name__ == "__main__":
    app()
