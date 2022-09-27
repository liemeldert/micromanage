"""
Wrapper for certain auth0 user metadate API functions.
"""
import http.client

from config import AUTH0_URL


def get_user(id):
    """
    retrieves a given user's information.
    :param id:
    :return:
    """
    conn = http.client.HTTPSConnection(AUTH0_URL)

    headers = {'authorization': f"Bearer {id}"}

    conn.request("GET", "/api/v2/users/user_id", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def update_user_metadata(id, data):
    """
    Updates a user's metadata on Auth0

    Example data input:
    "{\"user_metadata\": {\"displayName\": \"name\"}"
    :param id: User's ID token
    :param data:
    :return:
    """
    conn = http.client.HTTPSConnection("")

    headers = {
        'authorization': f"Bearer {id}",
        'content-type': "application/json"
    }

    conn.request("PATCH", f"/{AUTH0_URL}/api/v2/users/user_id", data, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
