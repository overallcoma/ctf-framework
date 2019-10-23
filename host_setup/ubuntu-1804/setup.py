import argparse
import subprocess
import platform
import os

target_OS = "Ubuntu-18.04"

if target_OS not in platform.platform():
    print("This script is only intended for Ubuntu 18.04")
    exit(1)

# This script must be run as root!
if not os.geteuid() == 0:
    print("This script must be run as root")
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email", dest="email", help="email for reverse proxy ctff_setup")
args = parser.parse_args()
email = args.email
if email is None:
    email = input("Please enter email address to use for reverse proxy")

docker_gpg_url = "https://download.docker.com/linux/ubuntu/gpg"
docker_apt_url = "https://download.docker.com/linux/ubuntu"


def subprocess_run(command):
    subprocess.run(command, shell=True, check=True)


def line_prepender(filename, newline):
    file = open(filename, 'r')
    file_content = file.readlines()
    file.close
    newline = newline + '\n'
    file = open(filename, 'w')
    file.write(newline)
    for line in file_content:
        file.write(line)
    file.close


try:
    print("Setting up the Environment for docker containers")
    subprocess_run("apt update -y")
    subprocess_run("apt install -y apt-transport-https ca-certificates curl software-properties-common")
    subprocess_run("curl " + docker_gpg_url + " | apt-key add -")
    subprocess_run("add-apt-repository \"deb [arch=amd64] " + docker_apt_url + " bionic stable\"")
    subprocess_run("apt update -y")
    subprocess_run("apt install -y docker docker-compose")
except Exception as e:
    print(e)
    print("Error preparing the environment for docker containers")
    exit(1)

try:
    print("Setting up Portainer")
    subprocess_run("docker volume create portainer_data")
    subprocess_run("docker run -d --restart=unless-stopped -p 8000:8000 -p 9000:9000 --name portainer -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer")
except Exception as e:
    print(e)
    print("Error setting up Portainer")
    exit(1)

try:
    print("Setting up the Reverse Proxy and LetsEncrypt Helper")
    subprocess_run("docker run --detach --restart=unless-stopped --name nginx-proxy --publish 80:80 --publish 443:443 --volume /etc/nginx/certs --volume /etc/nginx/vhost.d --volume /usr/share/nginx/html --volume /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy")
    subprocess_run("sudo docker run --detach --restart=unless-stopped --name nginx-proxy-letsencrypt --volumes-from nginx-proxy --volume /var/run/docker.sock:/var/run/docker.sock:ro --env " + email + " jrcs/letsencrypt-nginx-proxy-companion")
except Exception as e:
    print(e)
    print("Error Setting up the Reverse Proxy and the LetsEncrypt Helper")
    exit(1)

try:
    print("Setting up the Python3 Environemnt")
    subprocess_run("apt install -y python3-pip")
    line_prepender("/root/.bashrc", "alias python=python3")
except Exception as e:
    print(e)
    print("Error setting up the Python enviornment")

try:
    print("Doing final updates and rebooting")
    subprocess_run("apt update -y")
    subprocess_run("apt upgrade -y")
    subprocess_run("apt dist-upgrade -y ")
    subprocess_run("apt autoremove -y")
    subprocess_run("apt autoclean -y")
    subprocess_run("reboot")
except Exception as e:
    print(e)
    print("Error doing final updates and rebooting")
