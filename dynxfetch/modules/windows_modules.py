
"""
windows specific functions, which would not work on other platforms
"""

import itertools
import platform
import re
import subprocess
import winreg

import cpuinfo

from contextlib import suppress


def gimme_subkeys(path : str):
    """returns a list of subkeys, given a path to a key."""
    with suppress(WindowsError):
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        for i in itertools.count():
            yield winreg.EnumKey(key, i)

def graphics_card() -> str:
    """returns the graphics card name - windows specific"""
    op_sys = platform.uname().system
    if op_sys == "Windows":
        # trying through the registry
        with suppress(Exception):
            video_path = r"SYSTEM\ControlSet001\Control\Video"
            subkeys = gimme_subkeys(video_path)
            # i am aware that there can be multiple GPUs, but in testing, 
            # the first GPU found was always the main one
            # i've tested this on around 5 PCs, but i'm unsure if its true
            # if that is not the case, please let the dev know <3
            for key in subkeys:
                with suppress(WindowsError):
                    zero_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{video_path}\\{key}\\0000")
                    value = winreg.QueryValueEx(zero_key, "HardwareInformation.AdapterString")
                    winreg.CloseKey(zero_key)
                    result = value[0]
                    # dirty code to deal with names of integrated GPUs
                    # they're usually of the bytes type
                    if isinstance(result, bytes):
                        result = result.decode('utf-16')
                        result = result.strip()
                        result = re.sub("\\x00", "", result)
                    return result
        
    else:
        raise Exception("how did we get here... huh, contact the dev please!")

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
        # if that doesnt work, surprising, wmic maybe?
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