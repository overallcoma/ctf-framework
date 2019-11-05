import argparse
import sys
import random
import string
import os

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()
sys.path.append(args.path)
import ctff_functions


def yes_no_input(prompt_string):
    response_error = "Invalid Selection"
    while response_error == "Invalid Selection":
        prompt_string_yn = prompt_string + " (Y/N):"
        response = input(prompt_string_yn)
        response = response.lower().strip()
        if response[0] == "y":
            return 1
        if response[0] == "n":
            return 0
    print(response_error)


def path_combine(subdir):
    current_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_path, subdir)


rpcheck = ctff_functions.docker_rpcheck.ctff_rp_check()
use_reverse_proxy = 0
container_domain = 0
if rpcheck == 1:
    print("")
    print("You appear to have the nginx/letsencrypt proxy deployed")
    print("")
    use_reverse_proxy = yes_no_input("Would you like to use the reverse proxy for this container?")
    if use_reverse_proxy == 1:
        print("")
        container_domain = input("What domain name would you like this container to have?: ")
        print("")
        container_rp_email = input("What email address would you like to use for the certificate?: ")

if use_reverse_proxy == 0:
    print("")
    container_port = input("What port number would you like this container published on?: ")

flag = ''
password = ''
while flag == '':
    print("")
    flag = input("Please enter the desired flag: ")
while password == '':
    print("")
    print("Please enter the password that will be hidden")
    password = input("Or enter \"random\" to generate a random password: ")
if password == "random":
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

hashpassvar = 'HASHPASSREPLACE'

print("")
print(64 * "-")
print("You password is " + password)
print("")
flag_page_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)]) + ".html"
print("Your flag page name is " + flag_page_name)
print(64 * "-")

# sql_build_script = """
# DROP TABLE IF EXISTS passwords;
# CREATE TABLE IF NOT EXISTS passwords (
#     record_number integer PRIMARY KEY AUTOINCREMENT,
#     password TEXT,
#     pagename TEXT
# );
# INSERT INTO passwords (
#     password, pagename
#     ) VALUES (
#         '{}','{}'
#         );
# """.format(hashpassvar, flag_page_name)

# Read in the page data
dockerfile_data = open(path_combine("files/dockerfile"), "r").read()
error_page_data = open(path_combine("files/errorpage.html"), "r").read()
flag_page_data = open(path_combine("files/flagpage.html"), "r").read()
htaccess_data = open(path_combine("files/htaccess"), "r").read()
index_page_data = open(path_combine("files/index.php"), "r").read()
passhashgen_page_data = open(path_combine("files/passhashgen.php"), "r").read()

# Replace variables in file data
flag_page_data = flag_page_data.replace("$FLAG$", flag)
index_page_data = index_page_data.replace("$PASSWORD$", password)

# Open new files we will be writing
# dbsetup_page_temp = open(path_combine("dbsetup.sql"), "w+")
dockerfile_temp = open(path_combine("dockerfile"), "w+")
error_page_temp = open(path_combine("errorpage.html"), "w+")
flag_page_temp = open(path_combine("flagpage.html"), "w+")
htaccess_temp = open(path_combine("htaccess"), "w+")
index_page_temp = open(path_combine("index.php"), "w+")
passhashgen_page_temp = open(path_combine("passhashgen.php"), "w+")

# Write the data to the target files
# dbsetup_page_temp.write(sql_build_script)
dockerfile_temp.write(dockerfile_data)
error_page_temp.write(error_page_data)
flag_page_temp.write(flag_page_data)
htaccess_temp.write(htaccess_data)
index_page_temp.write(index_page_data)
passhashgen_page_temp.write(passhashgen_page_data)

# Close the files to save the data
# dbsetup_page_temp.close()
dockerfile_temp.close()
error_page_temp.close()
flag_page_temp.close()
htaccess_temp.close()
index_page_temp.close()
passhashgen_page_temp.close()

# Do all the work and create the container

print("")
print(64 * "-")
print("Content generated, build phase start")
print(64 * "-")
print("")

container_name = "basicweb-001"
container_restartpolicy = {"name": "unless-stopped"}
if use_reverse_proxy == 0:
    container_ports = {"80/tcp": "{}".format(container_port)}
container_image = "ctff/basicweb001:latest"

docker_client = ctff_functions.create_client()

try:
    build_path = os.path.dirname(os.path.realpath(__file__))
    docker_client.images.build(path=build_path, tag=container_image, rm=True, forcerm=True, quiet=False, buildargs={
        "var_flagpage": flag_page_name,
        "var_password": password
    })
except Exception as e:
    print(e)
    exit(1)

if use_reverse_proxy == 0:
    docker_client.containers.run(
        detach=True,
        name=container_name,
        restart_policy=container_restartpolicy,
        ports=container_ports,
        publish_all_ports=True,
        image=container_image
    )
elif use_reverse_proxy == 1:
    container_envvars = {
        "VIRTUAL_HOST": container_domain,
        "LETSENCRYPT_HOST": container_domain,
        "LETSENCRYPT_EMAIL": container_rp_email
    }
    docker_client.containers.run(
        detach=True,
        name=container_name,
        restart_policy=container_restartpolicy,
        environment=container_envvars,
        image=container_image
    )
docker_client.close()

print(64 * "-")
print("")
print(container_image + " has been deployed")
print("")
print("Cleaning up Build Directory")
print(64 * "-")
print("")
# os.remove(path_combine("dbsetup.sql"))
os.remove(path_combine("dockerfile"))
os.remove(path_combine("errorpage.html"))
os.remove(path_combine("flagpage.html"))
os.remove(path_combine("htaccess"))
os.remove(path_combine("index.php"))
os.remove(path_combine("passhashgen.php"))

print("Returning to menu")