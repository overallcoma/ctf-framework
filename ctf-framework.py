import os
import subprocess
import ctff_functions


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
    # clear()
    selection = ctff_functions.print_menu(config_modules)
    print(selection)
    # This handles the exit selection #
    if selection == len(config_modules):
        return False
    selected_module = config_modules[selection]
    if selected_module.moduleType == "folder":
        selected_path = config_modules[selection].modulePath
        menu_select(selected_path)
        return True
    if selected_module.moduleType == "installer":
        selected_path = config_modules[selection].modulePath
        setup_path = os.path.join(selected_path, "setup.py")
        if os.path.exists(setup_path):
            subprocess_command = 'python3 ' + setup_path
            subprocess_run(subprocess_command)
            return True
    return True


startup_folder = os.path.abspath(".")
target_folder = startup_folder

run = True
while run:
    run = menu_select(target_folder)
print("Exiting CTF-Framework")
