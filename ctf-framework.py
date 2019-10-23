import os
import subprocess
import ctff_functions


def subprocess_run(command):
    subprocess.run(command, shell=True)


host_setup_folder = os.path.join(os.path.abspath("."), "host_setup")
host_setup_folder_contents = os.listdir(host_setup_folder)

setup_modules = []
for folder in host_setup_folder_contents:
    folder = os.path.join(host_setup_folder, folder)
    if os.path.isdir(folder):
        setup_modules.append(ctff_functions.config_parse(folder))

selection = ctff_functions.print_menu(setup_modules)
command = "python3 " + setup_modules[selection].setupFile
subprocess_run(command)
