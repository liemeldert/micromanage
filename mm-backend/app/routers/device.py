import datetime
import json

from beanie import PydanticObjectId
from fastapi import status, APIRouter, Security, Depends
from fastapi_auth0 import Auth0User

from ..internal import database
from ..internal.models import Organization, Tenant, Device, Task, Application, MacPackage
from ..internal.utils import auth

router = APIRouter()


@router.post("/{tenant_id}/{serial}/create_device", dependencies=[Depends(auth.implicit_scheme)])  # user: Auth0User = Security(auth.get_user)
async def create_device(tenant_id: str, serial: str, user: Auth0User = Depends(auth.get_user)):
    """
    Creates a new device.
    Args:
        serial:
        tenant_id:
        user:

    Returns:

    """
    tenant = await Tenant.get(PydanticObjectId(tenant_id))
    if tenant is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in tenant.users:
        return status.HTTP_403_FORBIDDEN

    device = Device(tenant_id=tenant_id, serial=serial)

    try:
        await device.save()
    except Exception as e:
        return {"error": str(e)}
    return device.json()


@router.get("/{tenant_id}/get_devices", dependencies=[Depends(auth.implicit_scheme)])
async def get_devices(tenant_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves a list of devices for a tenant.
    Args:
        tenant_id:
        user:

    Returns:

    """
    tenant = await Tenant.get(PydanticObjectId(tenant_id))
    if tenant is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in tenant.users:
        return status.HTTP_403_FORBIDDEN

    devices = await Device.find({"tenant_id": tenant_id}).to_list()
    return {"devices": [device.json() for device in devices]}


@router.get("/{tenant_id}/{device_id}/get_device", dependencies=[Depends(auth.implicit_scheme)])
async def get_device(tenant_id: str, device_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves information about device.
    Args:
        tenant_id:
        device_id:
        user:

    Returns:

    """
    tenant = await Tenant.get(PydanticObjectId(tenant_id))
    if tenant is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in tenant.users:
        return status.HTTP_403_FORBIDDEN

    device = await Device.get(PydanticObjectId(device_id))
    return device.json()


@router.post("/{tenant_id}/{device_id}/{application_id}/package_id/create_task", dependencies=[Depends(auth.implicit_scheme)])
async def create_task(tenant_id: PydanticObjectId, device_id: PydanticObjectId, application_id: PydanticObjectId,
                      package_id: PydanticObjectId, command: str = "install", exec_time: datetime.datetime = None,
                      user: Auth0User = Depends(auth.get_user)):
    """
    Creates a new task.
    Args:
        tenant_id:
        device_id:
        task:
        user:

    Returns:

    """

    tenant = await Tenant.get(tenant_id)

    if user.id not in tenant.users:
        return status.HTTP_403_FORBIDDEN

    device = await Device.get(device_id)
    application = await Application.get(application_id)
    package = await MacPackage.get(package_id)

    if tenant is None or device is None or application is None or package is None:
        return status.HTTP_404_NOT_FOUND

    if exec_time is None:
        exec_time = datetime.datetime.now()

    # if user.id not in tenant.users:
    #     return status.HTTP_403_FORBIDDEN

    device.last_task_id += 1

    task = Task(task_id=device.last_task_id, tenant_id=tenant_id, device_id=device_id, application=application,
                package=package, exec_time=exec_time, command=command)

    device.tasks.append(task)
    tasks = device.tasks
    tasks.append(task)
    device.tasks = tasks
    await device.replace()
    print(device.json())
    return status.HTTP_200_OK
