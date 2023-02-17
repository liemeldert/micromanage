import datetime
import json
import urllib.parse
import http.client

import keyring
from pydantic import BaseModel, AnyUrl


class CLIConfig(BaseModel):
    """
    Model for storing the CLI config
    """
    tenant_id: str
    client_id: str = "client_id=4quihTffgVS021ZNIc5MvYl3nEAjqkKn&scope=%7Bscope%7D&audience=%7Baudience%7D"
    a0_domain: str = "pexl.us.auth0.com"
    backend_domain: str = "mmbe.pexl.pw"
    _expiry: datetime.datetime = None

    @property
    def token_expiration(self) -> datetime.datetime:
        return self._expiry

    @token_expiration.setter
    def token_expiration(self, value: int):
        """
        Set the token expiration
        :param value: seconds until expiration
        :return: None
        """
        self._expiry = datetime.datetime.now() + datetime.timedelta(seconds=value)

    def refresh_token(self):
        """
        Refresh the jolken rolken tolken
        :return: None
        """
        sec_refresh_token = keyring.get_password("micromanage", "token_refresh")

        if sec_refresh_token is None:
            raise Exception("No refresh token found. Please run `micromanage setup` to obtain one.")

        conn = http.client.HTTPSConnection(self.a0_domain)

        payload = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "client_id": get_config(),
            "refresh_token": sec_refresh_token
        })

        headers = {'content-type': "application/x-www-form-urlencoded"}

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        if res != 200:
            print("uh oh!\n" + res.read().decode("utf-8"))
            raise Exception("Unable to refresh token. Please run `micromanage setup` to obtain new one or report bug.")
        data = json.loads(res.read())

        # get the refresh token out of memory, probably doesn't matter but idk, esp since it is sent over a request but
        sec_refresh_token = None
        del sec_refresh_token

        keyring.set_password("micromanage", "token", data["access_token"])
        self._expiry = data["expires_in"]
        return data["access_token"]

    @property
    def token(self):
        # TODO: Implement token refresh or something
        tok = keyring.get_password("micromanage", "token")
        if self._expiry is None:
            raise Exception("Token has not been made yet, run `micromanage setup` to generate a token.")

        if self._expiry <= datetime.datetime.now():
            tok = self.refresh_token()

        return tok

    @token.setter
    def token(self, value):
        """
        Sets the REFRESH token, not standard jolken rolken tolken.
        :param value:
        :return:
        """
        keyring.set_password("micromanage", "token", value)


def get_config() -> CLIConfig:
    """
    Get the config from the config file
    :return: CLIConfig
    """
    return CLIConfig.parse_file("config.json")


def save_config(config: CLIConfig):
    """
    Save the config to the config file
    :param config: CLIConfig
    :return: None
    """
    with open("config.json", "w") as f:
        f.write(config.json())
