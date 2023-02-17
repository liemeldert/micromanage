import http.client
import json
import urllib.parse

import keyring

from .config import get_config


def get_authorization_url() -> dict:
    """
    Get URL to authorize device with Auth0
    :return: auth0 authorization url
    """
    config = get_config()
    conn = http.client.HTTPSConnection("")
    headers = {'content-type': "application/x-www-form-urlencoded"}
    conn.request("POST", config.a0_domain + "/oauth/device/code", config.client_id, headers)
    data = conn.getresponse().read()

    return json.loads(data.decode("utf-8"))


# Helper function to make authenticated requests to the API
async def api_request(method, route, data=None):
    config = get_config()
    headers = {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/json"
    }
    url = config. + route
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, json=data) as response:
            return response

