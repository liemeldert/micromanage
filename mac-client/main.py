import datetime
import logging
import subprocess
import time

import websocket
import mac
import json

from models import Task

base_url = "localhost:8000"
tenant = "637537b1d0b4eed05e01bac0"
# device = "C1MWR7X2J1WK"
device = "devidsep6376e56267597594fc29619e"

logging.basicConfig(level=logging.DEBUG)


def update_task(task, ws):
    """
    Updates task on serverside.
    :param task:
    :param ws:
    :return:
    """
    ws.send("update_task:")
    ws.send(task.json())


def recieve_events(ws):
    """
    This should run as its own thread.
    :param ws:
    :return:
    """
    while True:
        data = ws.recv()
        print(data)
        if data == "install:":
            jason = ws.recv()
            url = ws.recv()
            task_preload = json.loads(jason)
            task = Task(**task_preload)
            logging.info("package received: " + task.package.name)
            logging.debug("package info: " + jason)
            ws.send("istatus: downloading")
            result = "unknown"
            task.last_update_time = datetime.datetime.now()
            if task.package.type == "dmg":
                try:
                    logging.info("downloading dmg")
                    subprocess.run(f"curl -o /tmp/mmdmg.dmg '{url}'", shell=True, check=True)
                    ws.send("istatus: installing")
                    mac.install_dmg()
                # this is bad
                except Exception as e:
                    if result is None:
                        result = "unknown error"
                    logging.error("Failed to download dmg.\n" + result)
                    logging.error(str(e))
                    ws.send("istatus: failed")
                    ws.send(str(e))
                    continue
            elif task.package.type == "pkg":
                try:
                    logging.info("downloading pkg")
                    subprocess.run(f"curl -o /tmp/mmpkg.pkg '{url}'", shell=True, check=True)
                    ws.send("istatus: installing")
                    logging.info("installing pkg")
                    mac.install_pkg()
                # this isn't any better.
                except Exception as e:
                    if result is None:
                        result = "unknown error"
                    logging.error("Failed to download dmg.\n" + result)
                    logging.error(str(e))
                    ws.send("istatus: failed")
                    ws.send(str(e))
                    continue
            if task.package.package_name in mac.get_installed():
                logging.info("package installed successfully")
                ws.send("istatus: complete")
            # else:
            #     logging.error("package failed to install")
            #     ws.send("istatus: failed")
            #     ws.send("package failed to install for unknown reason")
        elif "installed" in data:
            ws.send("False")


def main():
    fails = 0
    while True:
        while fails < 30:
            websocket.enableTrace(True)
            ws = websocket.WebSocket()

            # can't be bothered to make this a thread yet
            try:
                ws.connect(f"ws://{base_url}/ws/{tenant}/{device}")
                ws.send(json.dumps(mac.get_system()))
                recieve_events(ws)
            # bad.
            except Exception as e:
                time.sleep(1)
                fails += 1
                logging.error("Failed to connect to server.\n" + str(e))
        time.sleep(120)


if __name__ == "__main__":
    main()
