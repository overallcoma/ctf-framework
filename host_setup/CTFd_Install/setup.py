import sys
import argparse
import subprocess
import os
import yaml
import git
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()
sys.path.append(args.path)
import ctff_functions


def subprocess_run(command):
    subprocess.run(command, shell=True, check=True)


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


ctfd_git_url = "https://github.com/CTFd/CTFd.git"
ctfd_volume_path = "/var/lib/docker/volumes/CTFd"
ctfd_logs_path = "/var/lib/docker/volumes/CTFd_logs"
ctfd_uploads_path = "/var/lib/docker/volumes/CTFd_uploads"
ctfd_volume_data_path = os.path.join(ctfd_volume_path, "_data")
ctfd_dockercompose = os.path.join(ctfd_volume_data_path, "docker-compose.yml")


def recusrive_yaml(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recusrive_yaml(value)
        else:
            yield (key, value)


rpcheck = ctff_functions.docker_rpcheck.ctff_rp_check()
use_reverse_proxy = 0
container_domain = 0
if rpcheck == 1:
    print("")
    print("You appear to have the nginx/letsencrypt proxy deployed")
    print("")
    use_reverse_proxy = yes_no_input("Would you like to use the reverse proxy for this deployment?")
    if use_reverse_proxy == 1:
        print("")
        container_rp_email = input("What email address would you like to use for the certificate?: ")
        print("")
        container_domain = input("What domain name would you like this container to have?: ")
if use_reverse_proxy == 0:
    print("")
    container_port = input("What port number would you like this container published on?: ")

# Clone CTFd Repo into a Docker Volume
docker_client = ctff_functions.create_client()
if os.path.exists(ctfd_volume_data_path):
    shutil.rmtree(ctfd_volume_data_path)
git.Git().clone(ctfd_git_url, ctfd_volume_data_path)

# Modify the Docker Compose as needed
yaml_data = open(ctfd_dockercompose, "r").read()
yaml_data = yaml.safe_load(yaml_data)

if use_reverse_proxy == 1:
    # Replace "ports" with "expose"
    del(yaml_data['services']['ctfd']['ports'])
    yaml_data['services']['ctfd']['expose'] = [8000]

    # Add in the RP needed env vars
    yaml_data['services']['ctfd']['environment'].append("VIRTUAL_HOST={}".format(container_domain))
    yaml_data['services']['ctfd']['environment'].append("LETSENCRYPT_HOST={}".format(container_domain))
    yaml_data['services']['ctfd']['environment'].append("LETSENCRYPT_EMAIL={}".format(container_rp_email))

elif use_reverse_proxy == 0:
    port_replace = "[{}:8000]".format(container_port)
    yaml_data['services']['ctfd']['ports'] = port_replace

# Clean up how CTFd stores data
docker_client.volumes.create("CTFd_logs")
docker_client.volumes.create("CTFd_uploads")
ctfd_app_volume = "{}:/opt/CTFd:ro".format(ctfd_volume_path)
ctfd_logs_volume = "{}:/var/logs/CTFd".format(ctfd_logs_path)
ctfd_uploads_volume = "{}:/var/uploads".format(ctfd_uploads_path)
volume_replace = [ctfd_app_volume, ctfd_logs_volume, ctfd_uploads_volume]
yaml_data['services']['ctfd']['volumes'] = volume_replace

# Put the containers on the default network
yaml_data['networks']['default'] = ['external', 'bridge']

os.remove(ctfd_dockercompose)
ctfd_replacement_yaml = open(ctfd_dockercompose, "w+")
ctfd_replacement_yaml.write(yaml.dump(yaml_data))
ctfd_replacement_yaml.close()

docker_client.close()

subprocess_run(["docker-compose", "-f", ctfd_volume_data_path, "up", "-d"])
