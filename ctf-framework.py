#!/usr/bin/python3

import os
import subprocess
import ctff_functions


def subprocess_run(command):
    subprocess.run(command, shell=True)


def menu_select(folder):
    config_modules = ctff_functions.config_collect(folder)
    selection = ctff_functions.print_menu(config_modules)
    # This handles the exit selection #
    if selection == len(config_modules):
        return False
    selected_module = config_modules[selection]
    # print(len(config_modules))
    if selected_module.moduleType == "folder":
        selected_path = config_modules[selection].modulePath
        menu_select(selected_path)
    if selected_module.moduleType == "installer":
        selected_path = config_modules[selection].modulePath
        setup_path = os.path.join(selected_path, "setup.py")
        if os.path.exists(setup_path):
            print(setup_path)
            subprocess_run(setup_path)
    return True


startup_folder = os.path.abspath(".")
target_folder = startup_folder

run = True
while run:
    run = menu_select(target_folder)
print("Exiting CTF-Framework")
