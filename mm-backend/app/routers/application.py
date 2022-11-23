import json
import logging

import boto3

from beanie import PydanticObjectId
from fastapi import status, APIRouter, Security, UploadFile, Depends
from fastapi.params import File
from fastapi_auth0 import Auth0User

from ..internal import database, s3
from ..internal.config import aws_endpoint, aws_access_key_id, aws_secret_access_key
from ..internal.models import Organization, Tenant, Application, MacPackage
from ..internal.utils import auth

router = APIRouter()


@router.post("/{org_id}/create_application", dependencies=[Depends(auth.implicit_scheme)])  # user: Auth0User = Depends(auth.get_user)
async def create_application(org_id: str, application: Application):
    """
    Creates a new application.
    Args:
        org_id:
        application:
        user:

    Returns:
    """
    jason = json.loads(application.json())
    logging.info(jason)
    jason["organization"] = org_id
    logging.info(jason)

    appl = Application(**jason)

    try:
        await appl.save()
    except Exception as e:
        return {"error": str(e)}
    return appl.json()


@router.get("/{org_id}/get_applications", dependencies=[Depends(auth.implicit_scheme)])
async def get_applications(org_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves a list of applications for an organization.
    Args:
        org_id:
        user:

        Returns:

        """
    org = await Organization.get(PydanticObjectId(org_id))
    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    applications = await Application.find({"organization_id": org_id}).to_list()
    return {"applications": [application.json() for application in applications]}


@router.get("/{org_id}/{application_id}/get_application", dependencies=[Depends(auth.implicit_scheme)])
async def get_application(org_id: str, application_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves information about application.
    :param user: auth0 user object
    :param org_id: id for organization
    :return:
    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    application = await Application.find({"_id": application_id}).first_or_none()

    return application.json()


@router.post("/{org_id}/{application_id}/update_application", dependencies=[Depends(auth.implicit_scheme)])
async def update_application(org_id: str, application_id: str, application: Application, user: Auth0User = Depends(auth.get_user)):
    """
    Updates an application.
    Args:
        org_id:
        application_id:
        application:
        user:

        Returns:

        """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    application = await Application.find({"_id": application_id}).first_or_none()

    jason = json.loads(application.json())
    jason.pop("_id")

    appl = Application(**jason)

    appl.organization_id = org_id

    try:
        await appl.save()
    except Exception as e:
        return {"error": str(e)}
    return appl.json()


@router.post("/{org_id}/{application_id}/delete_application", dependencies=[Depends(auth.implicit_scheme)])
async def delete_application(org_id: str, application_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Deletes an application.
    Args:
        org_id:
        application_id:
        user:

            Returns:

            """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    application = await Application.find({"_id": application_id}).first_or_none()

    await application.delete()

    return status.HTTP_200_OK


@router.post("/{org_id}/{application_id}/create_package_mac", dependencies=[Depends(auth.implicit_scheme)])
async def create_package(package: MacPackage, org_id: PydanticObjectId, application_id: PydanticObjectId):
    """
    Creates a new package for an application.
    Args:
        package: MacPackage to create
        org_id:
        application_id:
        user:

    Returns:

    """
    org = await Organization.get(org_id)

    if org is None:
        return status.HTTP_404_NOT_FOUND

    # if user.id not in org.users:
    #     return status.HTTP_403_FORBIDDEN

    application = await Application.get(application_id)

    if application is None:
        return status.HTTP_404_NOT_FOUND
    try:
        await package.save()
    except Exception as e:
        return {"error": str(e)}

    return package.json()


@router.get("/{org_id}/{application_id}/get_packages", dependencies=[Depends(auth.implicit_scheme)])
async def get_packages(org_id: str, application_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves a list of packages for an application.
    Args:
        org_id:
        application_id:
        user:

        Returns:

        """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    application = await Application.find({"_id": application_id}).first_or_none()

    if application is None:
        return status.HTTP_404_NOT_FOUND

    return {"packages": application.mac_packages}


@router.get("/{org_id}/{package_id}/get_package", dependencies=[Depends(auth.implicit_scheme)])
async def get_package(org_id: str, package_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Retrieves information about a package.
    Args:
        org_id:
        package_id:
        user:

        Returns:

    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    package = await MacPackage.find({"_id": package_id}).first_or_none()

    if package is None:
        return status.HTTP_404_NOT_FOUND

    return package.json()


@router.post("/{org_id}//{package_id}/update_package", dependencies=[Depends(auth.implicit_scheme)])
async def update_package(org_id: str, package_id: str, package: MacPackage, user: Auth0User = Depends(auth.get_user)):
    """
    Updates a package.
    Args:
        org_id:
        application_id:
        package_id:
        package:
        user:

    Returns:

    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    package = await MacPackage.find({"_id": package_id}).first_or_none()

    if package is None:
        return status.HTTP_404_NOT_FOUND

    jason = json.loads(package.json())
    jason.pop("_id")

    pack = MacPackage(**jason)
    try:
        await pack.save()
    except Exception as e:
        return {"error": str(e)}
    return pack.json()


@router.post("/{org_id}/{package_id}/delete_package", dependencies=[Depends(auth.implicit_scheme)])
async def delete_package(org_id: str, package_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Deletes a package.
    Args:
        org_id:
        application_id:
        package_id:
        user:

        Returns:

        """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.admins:
        return status.HTTP_403_FORBIDDEN

    package = await MacPackage.find({"_id": package_id}).first_or_none()

    if package is None:
        return status.HTTP_404_NOT_FOUND

    application = await Application.find({"_id": package.application_id}).first_or_none()

    if application is None:
        return status.HTTP_404_NOT_FOUND

    await package.delete()
    await package.save()

    application.mac_packages.remove(package_id)
    await application.save()

    return status.HTTP_200_OK


@router.get("/{org_id}/{package_id}/download_package", dependencies=[Depends(auth.implicit_scheme)])
async def download_package(org_id: str, package_id: str, user: Auth0User = Depends(auth.get_user)):
    """
    Responds with a s3 presigned url to download
    Args:
        org_id:
        package_id:
        user:

    Returns:

    """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    package = await MacPackage.find({"_id": package_id}).first_or_none()

    if package is None:
        return status.HTTP_404_NOT_FOUND

    if package.url is not None:
        return {"url": package.url}

    presigned = s3.create_presigned_url("mmpkgstore-va", package.id)
    return presigned


@router.post("/{org_id}/{package_id}/upload_package_direct", dependencies=[Depends(auth.implicit_scheme)])
async def upload_package(org_id: str, package_id: str, file: UploadFile = File(...), user: Auth0User = Depends(auth.get_user)):
    """
    Uploads a package to s3 with boto3.
    Args:
        org_id:
        package_id:
        file:
        user:

        Returns:

        """
    org = await Organization.find({"_id": org_id}).first_or_none()

    if org is None:
        return status.HTTP_404_NOT_FOUND

    if user.id not in org.users:
        return status.HTTP_403_FORBIDDEN

    package = await MacPackage.find({"_id": package_id}).first_or_none()

    if package is None:
        return status.HTTP_404_NOT_FOUND

    if package.url is not None:
        return {"url": package.url}

    try:
        s3_client = boto3.client('s3',
                                 endpoint_url=aws_endpoint,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
        s3_client.upload_fileobj(file.file, "mmpkgstore-va", package.id)
    except Exception as e:
        return {"error": str(e)}

    return status.HTTP_200_OK

