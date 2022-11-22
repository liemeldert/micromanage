import datetime

from beanie import Document, Indexed
from pydantic import BaseModel, Json, AnyUrl


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
    type: str = "pkg"
    url: AnyUrl = None
    s3_obj: str = None
    version: str
    application_id: str

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
    description: str = ""
    organization: str
    mac_packages: list[str] = []


###################
# Pydantic Models #
###################


class Task(BaseModel):
    """
    Task model
    """
    task_id: int
    command: str
    timestamp: datetime.datetime = datetime.datetime.now()
    exec_time: datetime.datetime = datetime.datetime.now()
    last_update_time: datetime.datetime = None
    application: Application
    package: MacPackage or MacScript
    status: int = 0  # 0, pending, 1, queued, 2, downloading, 3, installing, 4, failed
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


class Tenant(Document):
    """
    Project model
    """
    name: str
    description: str
    storing: str
    users: list[str]
    organization: str
    collections: list

    autoenroll: bool = False


class Organization(Document):
    """
    Organization model
    """
    name: str
    description: str = ""
    email_domain: str = None
    users: list = []
    admins: list = []
    plan: int = 0
    tenants: list = []


class Device(Document):
    """
    Device model
    """
    name: str = None
    serial: str
    tenant_id: str

    system: str = None
    tags: list = []
    group_id: str = None

    last_task_id = 0
    tasks: list[Task] = []
    additional_fields: dict = {}
    state: str = None  # 0 for d/n, 1 for online, 2 for fell asleep, 3 for shutdown, 4 for rebooting, 5 for updating
    laptop: bool = False  # Enables checking for updates prior to going to sleep.


class DeviceGroup(Document):
    """
    Device group model
    """
    name: str
    description: str
    members: list[Device]
    applications: list[Application]
    site: str
