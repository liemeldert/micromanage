import json

from beanie import PydanticObjectId
from fastapi import status, APIRouter, Security
from fastapi_auth0 import Auth0User

from ..internal import database
from ..internal.models import Organization, Site
from ..internal.utils import auth

router = APIRouter()


@router.get("/{org_id}/{site_id}/get_site")
async def get_site(org_id: str, site_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Retrieves information about site.
    :param user: auth0 user object
    :param org_id: id for organization
    :param site_id: id for site
    :return:
    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND
    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    site = await Site.get(PydanticObjectId(site_id))
    return {"site": site.json()}



@router.post("/create_organization")
async def create_organization(org: Organization):
    new_org = Organization(*org)
