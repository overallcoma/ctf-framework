import subprocess
import os
import ctff_functions

os.chdir(os.path.dirname(__file__))
config_file_name = 'info.cfg'
setup_python_name = 'setup.py'

folder_list = []
for folder in os.listdir("."):
    if os.path.isdir(folder):
        if os.path.join(os.path.abspath("."), folder):
            folder_list.append(os.path.join(os.path.abspath("."), folder))

menu_items = []

for folder in folder_list:
    print(folder)
    module_config = ctff_functions.config_parse(folder)
    menu_items.append(module_config)


def subprocess_run(command):
    subprocess.run(command, shell=True, check=True)


choice = ctff_functions.print_menu(menu_items)
print(choice)
subprocess_run(menu_items[choice].setupFile)
exit(0)
