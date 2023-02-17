import datetime
from pydantic import BaseModel, AnyUrl


class BasePackage(BaseModel):
    """
    Model for script metadata
    """
    name: str
    description: str
    icon_url: str
    install_condition_type: int  # 0, none/on demand,


class MacPackage(BaseModel):
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


class MacScript(BaseModel):
    """
    Model for script metadata
    """
    name: str
    version: str
    script_content: str
    icon_url: str


class Application(BaseModel):
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


class Device(BaseModel):
    """
    Device model
    """
    name: str = None

    hostname: str = None
    serial: str
    uuid: str
    mac_address: str
    model: str
    processor: str
    os_version: str
    os_build: str

    tenant_id: str
    tags: list = None
    group_id: str
    tasks: list[Task]
    additional_info: dict = None
    tenant: str = None
    organization: str = None
    state: str = None  # 0 for d/n, 1 for online, 2 for fell asleep, 3 for shutdown, 4 for rebooting, 5 for updating
    laptop: bool = False  # Enables checking for updates prior to going to sleep.


class DeviceGroup(BaseModel):
    """
    Device group model
    """
    name: str
    description: str
    members: list[Device]
    applications: list[Application]
    site: str
