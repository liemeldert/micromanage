import logging
import subprocess
import pydantic
from models import *


class System(BaseModel):
    model: str
    processor: str
    memory: str
    hardware_uuid: str


def get_serial() -> str:
    """
    Returns the current system's serial number.
    """
    return str(subprocess.run("system_profiler SPHardwareDataType | awk '/Serial Number/ {print $4}'",
                              stdout=subprocess.PIPE, shell=True, check=True).stdout.strip())


def get_installed() -> list[str]:
    """
    Returns a list of all installed applications.
    """
    return str(subprocess.run("mdfind \"kMDItemKind == 'Application'\"",
                              stdout=subprocess.PIPE, shell=True, check=True).stdout.strip()).split("\n")


def get_system() -> dict:
    profiler = str(subprocess.run("system_profiler SPHardwareDataType",
                                  stdout=subprocess.PIPE, shell=True, check=True
                                  ).stdout.strip())[47:].replace("      ", "").replace(" (system)", "").split("\\n")
    sys_info = {}
    for each in profiler:
        sys_info.update({each.split(": ")[0]: each.split(": ")[1]})
    return sys_info


def install_pkg(path: str = "/tmp/mmpkg.pkg"):
    """
    Installs a package.
    """
    subprocess.run(f"sudo installer -pkg '{path}' -target /", shell=True, check=True)
    # if "installer: Error - the package path specified was invalid: " in result:
    #     raise FileNotFoundError("Package not found.")
    # elif "installer: Error - the package does not contain a distribution file" in result:
    #     raise pydantic.ValidationError("Package is not a valid installer package.")
    subprocess.run(f"rm {path}", shell=True, check=True)
    return


def install_dmg(path: str = "/tmp/mmdmg.dmg", install_path: str = "/Applications"):
    """
    mounts, installs, unmounts, deletes, a dmg file
    :param install_path:
    :param path:
    :return:
    """
    try:
        result = str(
            subprocess.run(f"hdiutil attach '{path}'", stdout=subprocess.PIPE, shell=True, check=True).stdout.strip())
        if "hdiutil: attach failed - No such file or directory" in result:
            raise FileNotFoundError("DMG not found.")
        elif "hdiutil: attach failed - Resource busy" in result:
            raise pydantic.ValidationError("DMG is already mounted.")
        elif "hdiutil: attach failed - " in result:
            raise pydantic.ValidationError("DMG is not a valid DMG file.")
        volume = result.split("\\t")[-1][:-1]
        output = subprocess.getoutput(f"ls {volume}").replace("\n", "")
        files = output[1:].split("		")
        filename = []
        for each in files:
            if ".app" in each:
                filename.append(str(each))
        for each in filename:
            # todo: check for out of space error.
            subprocess.run(f"cp -r {volume}/{each} {install_path}/{each}", shell=True, check=True)

        subprocess.run(f"hdiutil detach {volume}", shell=True, check=True)
        subprocess.run(f"rm {path}", shell=True, check=True)
    except FileNotFoundError:
        raise FileNotFoundError("DMG not found.")
    except pydantic.ValidationError:
        raise pydantic.ValidationError("DMG is not a valid DMG file.")


def download_install_pkg(url: str, iteration=0):
    """
    Downloads and installs a package.
    """
    result = str(subprocess.run(f"curl -o /tmp/mmpkg.pkg {url}", shell=True, check=True).stdout.strip())
    if "curl: (6) Could not resolve host" in result:
        raise pydantic.ValidationError("Invalid URL.")
    try:
        install_pkg()
    except FileNotFoundError:
        if iteration > 3:
            logging.error("Failed to download package.\n" + result)
            raise FileNotFoundError("Package not found.")
        download_install_pkg(url)
        iteration += 1
    except pydantic.ValidationError:
        logging.error("Failed to install package.\n" + result)
        raise pydantic.ValidationError("Package is not a valid installer package!")


def download_install_dmg(url: str, iteration=0):
    """
    Downloads and installs a dmg.
    """
    result = str(subprocess.run(f"curl -o /tmp/mmdmg.dmg {url}", shell=True, check=True).stdout.strip())
    if "curl: (6) Could not resolve host" in result:
        raise pydantic.ValidationError("Invalid URL.")
    try:
        install_dmg()
    except FileNotFoundError:
        if iteration > 3:
            logging.error("Failed to download dmg.\n" + result)
            raise FileNotFoundError("DMG not found.")
        download_install_dmg(url)
        iteration += 1
    except pydantic.ValidationError:
        logging.error("Failed to install dmg.\n" + result)
        raise pydantic.ValidationError("DMG is not a valid DMG file!")
