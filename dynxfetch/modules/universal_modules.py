
'''
collection of functions, which return system info,
which should work on every platform, be it Linux, macOS, Windows or other
'''

import os
import platform
import subprocess
import cpuinfo
import psutil
import re
import datetime
from contextlib import suppress

def grab_pretty_os():
    '''returns OS'''
    return_name : str = ''
    op_sys = platform.uname()

    if op_sys.system == "Windows":
        return_name = f"Windows {op_sys.version} {op_sys.machine}"
    elif op_sys.system == "Darwin":
        return_name = f"macOS {platform.mac_ver()[0]} {op_sys.machine}"
    else:
        linux_name = platform.freedesktop_os_release()["PRETTY_NAME"]
        return_name = f"{linux_name} Linux {op_sys.machine}"

    return return_name

def grab_processor_name():
    '''returns the processor's name'''
    op_sys = platform.uname().system

    # linux
    if (op_sys == "Linux"):
        q = "cat /proc/cpuinfo"
        cpu_info = subprocess.check_output(q, shell = True).strip()
        cpu_info = cpu_info.decode('utf-8')
        for line in cpu_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line).strip()
    # should work if all else fails
    else:
        with suppress(Exception):
            cpu = cpuinfo.get_cpu_info()
            return f"{cpu['brand_raw']} @ {cpu['hz_actual_friendly']}"
        
    return ""

def grab_desktop_environment():
    '''returns the desktop environment'''
    op_sys = platform.uname().system
    if (op_sys == "Windows"): # hardcoded, unsure how to fetch windows DE otherwise
        return "Aero"
    elif (op_sys == "Darwin"): # ditto, someone let me know how to do this better pls
        return "Aqua"
    else:
        return os.environ.get("DESKTOP_SESSION") or os.environ.get("XDG_SESSION_TYPE")

def grab_ram_usage():
    '''returns current RAM usage'''
    ram_usage = psutil.virtual_memory()
    ram_used = ram_usage.used / (1024**3)
    ram_total = ram_usage.total / (1024**3)

    return f"{ram_used:.2f} GB / {ram_total:.2f} GB"

def grab_drive_usage():
    '''returns current used drive space'''
    drives = psutil.disk_partitions()

    drives_out = []
    for drive in drives:
        storage_usage = psutil.disk_usage(drive[1])
        storage_used = storage_usage.used / (1024**3)
        storage_total = storage_usage.total / (1024**3)
        drives_out.append(f"{drive[1]} {storage_used:.2f} GB / {storage_total:.2f} GB")

    return drives_out

def grab_shell():
    '''returns the currently running shell'''
    shell = ""
    op_sys = platform.system()
    if (op_sys == "Linux" or op_sys == "Darwin"):
        shell = os.environ.get("SHELL")
    elif (op_sys == "Windows"):
        shell = os.environ.get("COMSPEC")
        shell = os.path.basename(shell)

    return shell

def grab_uptime():
    '''return a pretty uptime of the system'''
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now()
    uptime_time = current_time - datetime.datetime.fromtimestamp(boot_time)
    hrs = int(uptime_time.total_seconds() // 3600)
    minutes = int(uptime_time.total_seconds() % 3600) // 60

    return f"{hrs} hrs, {minutes} mins"
