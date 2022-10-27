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


@router.get("/{site_id}/")
async def get_site(org_id: str, site_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Retrieves information about site.
    :param site_id:
    :return:
    """
    site = await Site.find({"_id": site_id}).first_or_none()

    if user.id not in site.users:
        return {status.HTTP_403_FORBIDDEN}

    return {"site": site.json()}


@router.post("/{site_id}/edit")
async def edit_site(site_id: str, new_site: Site, user: Auth0User = Security(auth.get_user)):
    """
    Edits site information.APIRouter
    :param site_id: ID for site
    :return: 201
    """
    site = await Site.find({"_id": site_id}).first_or_none()

    if user.id not in site.users:
        return {status.HTTP_403_FORBIDDEN}

    # Extra steps because I need to remove ID to prevent error
    jason = json.loads(new_site.json())
    jason.pop("_id")

    site.set(jason)
    return {status.HTTP_200_OK}


@router.post("/{site_id}/users")
async def add_user(site_id: str, new_user_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Adds a user to the site
    :param site_id: ID for site_id
    :param new_user_id: Auth0 ID for user being added
    :param user: Current Auth0 user making change
    """
    site = await Site.find({"_id": site_id}).first_or_none()

    if user.id not in site.users:
        return {status.HTTP_403_FORBIDDEN}

    site.users.append(new_user_id)
    await site.save()

    return {status.HTTP_200_OK}


@router.

