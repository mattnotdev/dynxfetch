import os
import platform
# import winreg
import subprocess
import datetime
import cpuinfo
import re
import psutil
from contextlib import suppress

def grab_os():
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
    # windows
    elif (op_sys == "Windows"):
        # try accessing through registry
        # with suppress(Exception):
        #    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Hardware\Description\System\CentralProcessor\0")
        #    value = winreg.QueryValueEx(key, "ProcessorNameString")
        #    winreg.CloseKey(key)
        #    cpu_name = value[0].strip()
        #    return cpu_name
        # wmic may not work in win 11
        with suppress(Exception):
            cpu_name = subprocess.check_output(["wmic", "cpu", "get", "name"]).strip()
            cpu_name = cpu_name.decode('utf-8')
            return cpu_name.split("\n")[1]
    # should work if all else fails
    else:
        with suppress(Exception):
            cpu = cpuinfo.get_cpu_info()
            return f"{cpu['brand_raw']} @ {cpu['hz_actual_friendly']}"
        
    return ""

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
    '''returns the shell used'''
    shell = os.environ.get('SHELL')

    return shell

def grab_uptime():
    '''return a pretty uptime of the system'''
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now()
    uptime_time = current_time - datetime.datetime.fromtimestamp(boot_time)
    hrs = int(uptime_time.total_seconds() // 3600)
    minutes = int(uptime_time.total_seconds() % 3600) // 60

    return f"{hrs} hrs, {minutes} mins"

def desktop_environment():
    '''returns the desktop environment'''
    wm = os.environ.get("DESKTOP_SESSION") or os.environ.get("XDG_SESSION_TYPE")
    return wm

def print_line(component_name : str, data : str):
    print(f"-[ {component_name}:\t{data}")

def print_lines(component_name : str, data):
    print(f"-[ {component_name}:", end="")
    for x in data:
        print(f"\t{x}")

def main():
    op_sys = platform.uname().system
    host_name = platform.node()
    user_name = os.environ.get('USER', os.environ.get('USERNAME'))

    print("")
    print(f"\t{user_name}@{host_name}\n")
    print_line("OS    ", grab_os())
    print_line("HOST  ", host_name)
    print_line("UPTIME", grab_uptime())
    if (op_sys == "Linux"):
        print_line("DE    ", desktop_environment())
        print_line("SHELL ", grab_shell())
    print_line("CPU   ", grab_processor_name())
    print_line("RAM   ", grab_ram_usage())
    print_lines("DRIVE ", grab_drive_usage())
    print("")

if __name__ == "__main__":
    main()