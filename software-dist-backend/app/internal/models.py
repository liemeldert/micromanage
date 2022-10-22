import datetime

from beanie import Document, Indexed
from pydantic import BaseModel


class BasePackage(Document):
    """
    Model for script metadata
    """
    name: str
    description: str
    icon_url: str
    install_condition_type: int  # 0, none/on demand,


class MacPackage(Document):
    """
    Model for storing metadata for a mac package.
    """
    name: str
    icon_url: str
    package_name: str
    package_url: str
    package_on_s3: bool  # if the package is stored on our s3 server, if so it will create presigned url.
    version: str

    installed_application_path: str


class MacScript(Document):
    """
    Model for script metadata
    """
    name: str
    version: str
    script_content: str
    icon_url: str


class Application(Document):
    """
    Applications model storing versions
    """
    name: str
    description: str
    site: str
    mac_packages: list[MacPackage or MacScript]


###################
# Pydantic Models #
###################


class Task(BaseModel):
    """
    Task model
    """
    task_id: int
    command: str
    timestamp: str = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    application: Application
    package: MacPackage or MacScript
    status: int = 0
    status_reason: str = None


##############
# ODM Models #
##############

class User(Document):
    """
    User model
    """
    name: Indexed(str)
    pronouns: str
    email: Indexed(str)
    avatar: str
    plan: int
    created_at: datetime.datetime

    # ID of org that the user belongs to.
    organization: str
    projects: list


class Site(Document):
    """
    Project model
    """
    name: str
    description: str
    storing: str
    users: list[str]
    organization: str
    collections: list

    block_unknown_devices: bool = False


class Organization(Document):
    """
    Organization model
    """
    name: str
    description: str
    email_domain: str
    users: list
    admins: list
    plan: int
    sites: list


class Device(Document):
    """
    Device model
    """
    name: str = None
    identifier: str  # SN for Mac, idk for Windows.
    site: Site
    tags: list = None
    group_id: str
    tasks: list[Task]
    additional_info: dict = None
    site: str = None
    organization: str = None
    state: int = 0  # 0 for d/n, 1 for online, 2 for fell asleep


class DeviceGroup(Document):
    """
    Device group model
    """
    name: str
    description: str
    members: list[Device]
    site: str








# class Task(HashModel):
#     """
#     Task model
#     status codes:
#         0 - not started/queued
#         1 - in progress
#         2 - completed
#         3 - failed
#     reattempt is the number of times the task will be retried before
#     """
#     device_id: str
#     command: str
#     status: int
#     reattempt: int = 0
#
#     time_enqueued = datetime.datetime.now()
#     time_started: datetime.time
#     time_completed: datetime.time
