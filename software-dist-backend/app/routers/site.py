import json

from fastapi import status, APIRouter, Security
from fastapi_auth0 import Auth0User

from ..internal.models import Organization, Site
from ..internal.utils import auth

######################
# Unprotected routes #
######################
router = APIRouter()


@router.get("/{org_id}/get_sites")
async def get_org_sites(org_id: int, user: Auth0User = Security(auth.get_user)):
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

    return {"sites": Organization.sites}


@router.get("/{org_id}/{site_id}/get_site")
async def get_site(org_id: str, site_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Retrieves information about site.
    :param org_id:
    :param site_id:
    :return:
    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND
    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    site = await Site.find({"_id": org_id}).first_or_none()

    return {"site": site.json()}


