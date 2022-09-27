import datetime

from beanie import Document, Indexed


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
