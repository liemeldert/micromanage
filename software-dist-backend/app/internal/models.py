import datetime

from beanie import Document, Indexed
from redis_om import HashModel


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
    organization: str
    collections: list


class Organization(Document):
    """
    Organization model
    """
    name: str
    description: str
    users: list
    admins: list
    plan: int
    sites: list


################
# Redis Models #
################


class Task(HashModel):
    """
    Task model
    status codes:
        0 - not started/queued
        1 - in progress
        2 - completed
        3 - failed
    reattempt is the number of times the task will be retried before
    """
    device_id: str
    command: str
    status: int
    reattempt: int = 0

    time_enqueued = datetime.datetime.now()
    time_started: datetime.time
    time_completed: datetime.time
