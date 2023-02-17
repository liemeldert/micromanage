from util.config import get_config


async def api_request(method, route, data=None):
    """
    Helper function to make authenticated API requests
    :param method:
    :param route:
    :param data:
    :return:
    """
    headers = {
        "Authorization": f"Bearer {get_config().key}",
        "Content-Type": "application/json"
    }
    url = base_url + route
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, json=data) as response:
            return response
