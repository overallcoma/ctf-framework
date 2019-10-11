import subprocess
import os
from configparser import ConfigParser

os.chdir(os.path.dirname(__file__))

menu_list = []
for folder in os.listdir("."):
    if os.path.isdir(folder):
        if (os.path.join(os.path.abspath("."), folder)):
            menu_list.append(folder)

    config = ConfigParser()
    print(d + "/info.cfg")
    config_file = (d + " /info.cfg")
    config.read(config_file)

    module_identity = config["module-identity"]
    module_prettyname = module_identity["prettyname"]
    menu_list.append(module_prettyname)


def subprocess_run(command):
    subprocess.run(command, shell=True, check=True)


def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. " + menu_list[0])
    print("2. Use Challange Generator")
    print("3. Create Challenge Container")
    print("4. XXXXXXX")
    print("5. Exit")
    print(67 * "-")


setup_script_location = './setup/setup.py'

loop = True
while loop:
    print_menu()
    choice = input("Enter your choice [1-5]: ")
    if choice == 1:
        print("Environment Setup Selected")
        subprocess_run("python3 " + setup_script_location)
    elif choice == 2:
        print("Menu 2 has been selected")
    elif choice == 3:
        print("Menu 3 has been selected")
    elif choice == 4:
        print("Menu 4 has been selected")
    elif choice == 5:
        print("Menu 5 has been selected")
        loop = False
    else:
        print("Wrong option selection. Enter any key to try again.")
