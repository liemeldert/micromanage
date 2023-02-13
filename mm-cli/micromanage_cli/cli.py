import http.client
import json

import typer
import time

from rich.progress import track
from rich import print

from lib import authentication
from lib.config import CLIConfig, save_config
app = typer.Typer()


@app.command()
def setup(tenant_id: str = typer.Option(..., prompt=True)):
    """ Setup the CLI """
    config = CLIConfig(tenant_id=tenant_id)
    authorization_information = authentication.get_authorization_url()
    print(f"[green]Please visit the following url to authenticate your account:[/green]")
    print(f"[blue]{authorization_information['verification_uri_complete']}[/blue]")
    print(f"[green'You have [blue]{authorization_information['expires_in']}[/blue]"
          f" seconds to authenticate your account[/green]")

    t_limit = (authorization_information['expires_in'] / authorization_information['interval']).round()

    for i in track(range(t_limit), description="Time remaining..."):
        time.sleep(authorization_information['interval'])  # wait for interval

        conn = http.client.HTTPSConnection("")
        payload = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code=%7ByourDeviceCode%7D" \
                  "&client_id=4quihTffgVS021ZNIc5MvYl3nEAjqkKn"
        headers = {'content-type': "application/x-www-form-urlencoded"}
        conn.request("POST", "/pexl.us.auth0.com/oauth/token", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())

        if res.status == 200:
            print(f"[green]Authentication successful![/green]")
            config.token = data["access_token"]
            config.token_expiration = data["expires_in"]
            return

    save_config(config)


# @app.command()
# def setup_advanced(config: CLIConfig):
#     save_config(config)
#     return


if __name__ == "__main__":
    app()
