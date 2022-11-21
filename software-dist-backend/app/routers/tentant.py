import json

from fastapi import status, APIRouter, Security, Depends
from fastapi_auth0 import Auth0User

from ..internal.models import Organization, Tenant
from ..internal.utils import auth

######################
# Unprotected routes #
######################
router = APIRouter()


@router.get("/{org_id}/tenants", dependencies=[Depends(auth.implicit_scheme)])
async def get_org_tenants(org_id: int, user: Auth0User = Security(auth.get_user)):
    """
    Retrieve a list of sites belonging to an organization
    :param org_id:
    :param user:
    :return:
    """
    org = await Organization.find({"id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND
    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    return {"sites": Organization.tenants}


@router.get("/{tenant_id}/get_tenant", dependencies=[Depends(auth.implicit_scheme)])
async def get_site(tenant_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Retrieves information about tenant.
    :param tenant_id:
    :return:
    """
    tenant = await Tenant.find({"_id": tenant_id}).first_or_none()

    if user.id not in tenant.users:
        return {status.HTTP_403_FORBIDDEN}

    return {"tenant": tenant.json()}


@router.post("/{tenant_id}/edit", dependencies=[Depends(auth.implicit_scheme)])
async def edit_tenant(tenant_id: str, new_tenant: Tenant, user: Auth0User = Security(auth.get_user)):
    """
    Edits tenant information.APIRouter
    :param tenant_id: ID for tenant
    :return: 201

    Args:
        new_tenant:
    """
    tenant = await Tenant.find({"_id": tenant_id}).first_or_none()

    if user.id not in tenant.users:
        return {status.HTTP_403_FORBIDDEN}

    # Extra steps because I need to remove ID to prevent error
    jason = json.loads(new_tenant.json())
    jason.pop("_id")

    tenant.set(jason)
    return {status.HTTP_200_OK}


@router.post("/{org_id}/create_tenant", dependencies=[Depends(auth.implicit_scheme)])
async def create_tenant(new_tenant: Tenant, org_id: str):  # , user: Auth0User = Security(auth.get_user)
    """
    Creates a new tenant
    :param new_tenant: Tenant object
    :param user: Current
    :param org_id: ID for organization
    :return:
    """
    jason = json.loads(new_tenant.json())
    try:
        jason.pop("_id")
    except KeyError:
        pass

    tenant = Tenant(**jason)
    await tenant.save()

    return {status.HTTP_200_OK}
