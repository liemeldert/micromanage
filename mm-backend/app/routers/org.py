import json

from beanie import PydanticObjectId
from fastapi import status, APIRouter, Security, Depends
from fastapi_auth0 import Auth0User

from ..internal import database
from ..internal.models import Organization, Tenant
from ..internal.utils import auth

router = APIRouter()


@router.post("/create_organization")
async def create_organization(new_org: Organization, user: Auth0User = Security(auth.implicit_scheme)):
    jason = json.loads(new_org.json())
    jason.pop("_id")

    org = Organization(**jason)

    try:
        await org.save()
    except Exception as e:
        return {"error": str(e)}
    return org.json()


@router.get("/get_user_organizations", dependencies=[Depends(auth.implicit_scheme)])
async def get_user_organizations(user: Auth0User = Security(auth.implicit_scheme)):
    """
    Retrieves a list of organizations for a user.
    Args:
        user:

        Returns:

        """
    orgs = await Organization.find({"users": user.id}).to_list(100)
    return [org.json() for org in orgs]
