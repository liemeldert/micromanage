import json

from beanie import PydanticObjectId
from fastapi import status, APIRouter, Security
from fastapi_auth0 import Auth0User

from ..internal import database
from ..internal.models import Organization, Site
from ..internal.utils import auth

######################
# Unprotected routes #
######################
router = APIRouter()


@router.get("/{org_id}/get_org")
async def get_org(org_id: str, user: Auth0User = Security(auth.get_user)):
    """
    Retrieve a list of sites belonging to an organization
    :param org_id:
    :param user:
    :return:
    """
    org = await Organization.get(PydanticObjectId(org_id))

    if org is None:
        return status.HTTP_404_NOT_FOUND
    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    return {"sites": org.json()}



