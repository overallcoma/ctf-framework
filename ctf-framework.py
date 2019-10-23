import consolemenu
import os
import subprocess
import ctff_functions
import time


def subprocess_run(command):
    subprocess.run(command, shell=True)


main_menu = consolemenu.ConsoleMenu("CTF Framework Setup", "Select your function")

host_setup_folder = os.path.join(os.path.abspath("."), "host_setup")
host_setup_folder_contents = os.listdir(host_setup_folder)

setup_folder_list = []
for folder in host_setup_folder_contents:
    folder = os.path.join(host_setup_folder, folder)
    if os.path.isdir(folder):
        setup_folder_list.append(folder)
for setup_folder in setup_folder_list:
    module_config = ctff_functions.config_parse(setup_folder)
    setup_file = os.path.join(setup_folder, "setup.py")
    setup_command = "python3 {}".format(setup_file)
    print(setup_file)
    print(setup_command)

    setup_item = consolemenu.items.FunctionItem(module_config.prettyName, subprocess_run(setup_command))
    main_menu.items.append(setup_item)

    time.sleep(10)

main_menu.show()