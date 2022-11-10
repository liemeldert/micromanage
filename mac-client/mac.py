import subprocess
import pydantic
from pydantic import BaseModel


class System(BaseModel):
    model: str
    processor: str
    memory: str
    hardware_uuid: str


def get_serial() -> str:
    """
    Returns the current system's serial number.
    """
    return subprocess.run("system_profiler SPHardwareDataType | awk '/Serial Number/ {print $4}'",
                            stdout=subprocess.PIPE, shell=True, check=True).stdout.strip()


def get_system() -> System:
    
