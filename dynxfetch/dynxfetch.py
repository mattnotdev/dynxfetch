import os
import platform
from modules import universal_modules

def print_line(component_name : str, data : str):
    print(f"-[ {component_name}:  {data}")

def print_lines(component_name : str, data):
    print(f"-[ {component_name}:", end="")
    for x in data:
        print(f"  {x}")

def main():
    host_name = platform.node()
    user_name = os.environ.get('USER', os.environ.get('USERNAME'))

    print("")
    print(f"\t{user_name}@{host_name}\n")
    print_line("OS", universal_modules.grab_pretty_os())
    print_line("HOST", host_name)
    print_line("UPTIME", universal_modules.grab_uptime())
    print_line("DESKTOP ENVIRONMENT", universal_modules.grab_desktop_environment())
    print_line("SHELL", universal_modules.grab_shell())
    if (platform.uname().system == "Windows"):
        from modules import windows_modules
        print_line("CPU", windows_modules.grab_processor_name())
    else:
        print_line("CPU", universal_modules.grab_processor_name())
    print_line("RAM", universal_modules.grab_ram_usage())
    print_lines("DRIVE", universal_modules.grab_drive_usage())
    print("")

if __name__ == "__main__":
    main()