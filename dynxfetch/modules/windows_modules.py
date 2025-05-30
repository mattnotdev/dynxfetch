
"""
windows specific functions, which would not work on other platforms
"""

import platform
import subprocess
import winreg

import cpuinfo

from contextlib import suppress


def processor_name() -> str:
    """returns the processor's name - windows specific"""
    op_sys = platform.uname().system

    if op_sys == "Windows":
        # try accessing through registry
        with suppress(Exception):
           key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Hardware\Description\System\CentralProcessor\0")
           value = winreg.QueryValueEx(key, "ProcessorNameString")
           winreg.CloseKey(key)
           cpu_name = value[0].strip()
           return cpu_name
        # wmic may not work in win 11
        with suppress(Exception):
            cpu_name = subprocess.check_output(["wmic", "cpu", "get", "name"]).strip()
            cpu_name = cpu_name.decode('utf-8')
            return cpu_name.split("\n")[1]
        # if all else fails
        with suppress(Exception):
            cpu = cpuinfo.get_cpu_info()
            return f"{cpu['brand_raw']} @ {cpu['hz_actual_friendly']}"
    else:
        raise Exception("impressive that it got here... huh, contact the dev please!")