import random

import pymongo

from app.internal import exceptions
from app.internal.config import MONGO_URI
from .models import Organization

client = pymongo.MongoClient(MONGO_URI)


def initialize_collections(collections: list, project_id: int) -> None:
    """Initialize collections for a new project.

    A new database automatically will use the project_id as its name.

    Args:
        project_id (int): MongoDB ID for the project
        collections (list): List of the collection names to initialize

    Raises:
        exceptions.DatabaseAlreadyExists: Database being initialized already exists.
        exceptions.CollectionAlreadyExists: Collection being added already exists... somehow.
    """
    if project_id in client.list_database_names():
        raise exceptions.DatabaseAlreadyExists(project_id)
    db = client[project_id]
    for name in collections:
        if name in db.list_collection_names():
            raise exceptions.CollectionAlreadyExists(name)
        collection = db[name]
        collection.insert_one({"name": "test",
                               "description": "This is a test document that is automatically "
                                              "inserted into the database during initialization."})


def insert_document(project_id: int, collection_name: str, document: dict) -> int:
    """Insert a document into the given database and collection.

    Args:
        project_id (int): _description_
        collection_name (str): _description_
        document (dict): _description_

    Returns:
        int: ID of the inserted document
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    db = client[project_id]
    if collection_name not in db.list_collection_names():
        raise exceptions.CollectionDoesNotExist(collection_name)
    collection = db[collection_name]
    return collection.insert_one(document).inserted_id


def get_document(project_id: int, collection_name: str, document_id=None,
                 field: str = None, value: str = None) -> any:
    """Get a document from the given database and collection.

    Use either document_ID or field and value to get the document.

    Args:
        project_id (int): ID of the project containing the document
        collection_name (str): name of the collection containing the document
        document_id (str): ID of the document.
        field (str): field of the document to retrieve
        value (str): value of the field to retrieve

    Returns:
        dict: Document from the given database and collection or a dict containing a list
        None: If the document does not exist
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    db = client[project_id]
    if collection_name not in db.list_collection_names():
        raise exceptions.CollectionDoesNotExist(collection_name)
    collection = db[collection_name]
    if document_id is not None:
        return collection.find_one({"_id": document_id})
    if field is not None and value is not None:
        return collection.find_one({field: value})
    raise TypeError("Must specify either document_id or field and value")


def get_collections(project_id) -> list:
    """
    Gets a collection from a given project id.
    Args:
    :param project_id:
    :return:
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    db = client[project_id]
    return db.list_collection_names


def get_project(project_id: int):
    """
    Gets a project from a given project id.
    Args:
    :param project_id:
    :return:
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    return client[project_id]


def get_collection(project_id: int, collection_name: str):
    """
    Gets a collection from a given project id.
    :param project_id:
    :param collection_name:
    :return:
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    db = client[project_id]
    if collection_name not in db.list_collection_names():
        raise exceptions.CollectionDoesNotExist(collection_name)
    return db[collection_name]


def update_one(json, project_id: int, collection_name: str, document_id: str):
    """
    Updates a document in the given database and collection.
    :param json: 
    :param project_id: 
    :param collection_name: 
    :param document_id: 
    :return: 
    """
    if project_id not in client.list_database_names():
        raise exceptions.DatabaseDoesNotExist(project_id)
    document = get_document(project_id, collection_name, document_id)
    document.update(json)


async def create_project(collections, organization=None) -> int:
    """
    Creates a new project in the database.
    Collections must be added at the same time as MongoDB create collections and databases lazily.
    :param collections: Collections to be added.
    :param organization: optional -  ID of organization to hold the project.
    :return:
    """
    unique = False
    while not unique:
        project_id = random.randint(0, 1000000)
        if project_id not in client.list_database_names():
            unique = True
    db = client[project_id]
    client.create_database(project_id)

    # Create the collections
    # This must be done now since MongoDB creates collections and databases lazily.
    # A test document will also be inserted, but I think it should be fine to then delete it.
    initialize_collections(collections, project_id)
    if organization is None:
        return project_id
    else:
        org = await Organization.find({"name": organization}).first_or_none()
        org.projects.append(project_id)
    return project_id
