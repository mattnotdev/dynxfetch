#!/usr/bin/env python3

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

    logo = []
    with open('logo.txt', 'r') as logo_file:
        for line in logo_file:
            line = line.rstrip()
            logo.append(line)

    print("")
    print(f"\t{user_name}@{host_name}\n")
    print_line("OS", universal_modules.pretty_os())
    print_line("HOST", host_name)
    print_line("UPTIME", universal_modules.pc_uptime())
    print_line("DESKTOP ENVIRONMENT", universal_modules.desktop_environment())
    print_line("SHELL", universal_modules.shell())
    if platform.uname().system == "Windows":
        from modules import windows_modules
        print_line("CPU", windows_modules.processor_name())
        print_line("GPU", windows_modules.graphics_card())
    else:
        print_line("CPU", universal_modules.processor_name())
        print_line("GPU", universal_modules.graphics_card())
    print_line("RAM", universal_modules.ram_usage())
    print_lines("DRIVE", universal_modules.drive_usage())
    print("")

if __name__ == "__main__":
    main()