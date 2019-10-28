#!/usr/bin/python3
import os
import subprocess
import ctff_functions
import pathlib


def subprocess_run(command):
    subprocess.run(command, shell=True)


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def menu_select(folder):
    config_modules = ctff_functions.config_collect(folder)
    clear()
    selection = ctff_functions.print_menu(config_modules)
    # This handles the exit selection #
    if selection == len(config_modules):
        return False
    selected_module = config_modules[selection]
    if selected_module.moduleType == "folder":
        selected_path = config_modules[selection].modulePath
        menu_select(selected_path)
    if selected_module.moduleType == "installer":
        selected_path = config_modules[selection].modulePath
        setup_path = os.path.join(selected_path, "setup.py")
        if os.path.exists(setup_path):
            subprocess_command = 'python3' + setup_path
            subprocess_run(subprocess_command)
            exit(0)
    return True


startup_folder = os.path.abspath(".")
target_folder = startup_folder
try:
    challenges_folder = os.path.join(startup_folder, "challenges")
except Exception as e:
    print("Can't locate challenges folder")
    print(e)
    exit(1)

need_chmod = 0

for python_file in pathlib.Path(challenges_folder).rglob('*.py'):
    if not os.access(python_file, os.X_OK):
        need_chmod = 1


if need_chmod == 1:
    clear()
    print("It looks like you're running CTF_Framework for the first time")
    print("")
    choice = input('Would you like to make the python files in this folder executable?  (Y/N)')
    choice = choice.lower().strip()
    if choice == "y":
        print ("Selected Yes")
        for python_file in pathlib.Path(challenges_folder).rglob('*.py'):
            if not os.access(python_file, os.X_OK):
                python_file = os.path.abspath(python_file)
                stat_mode = os.stat(python_file).st_mode
                stat_mode |= (stat_mode & 0o444) >> 2
                os.chmod(python_file, stat_mode)

run = True
while run:
    run = menu_select(target_folder)
print("Exiting CTF-Framework")