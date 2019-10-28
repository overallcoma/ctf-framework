#!/usr/bin/python3

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

use_portainer = 0
use_reverseproxy = 0
reverseproxy_email = 0
portainer_domain = 0

use_portainer = input("Do you want to install Portainer? (Y/N) : ")
use_portainer = use_portainer.lower().strip()
use_reverseproxy = input("Do you want to install the reverse proxy with LetsEncrypt? (Y/N) : ")
use_reverseproxy = use_reverseproxy.lower().strip()
if use_reverseproxy == "y":
    while reverseproxy_email == '':
        reverseproxy_email = input("Please enter email address to use for reverse proxy:  ")
        reverseproxy_email = reverseproxy_email.lower().strip()
    if use_portainer == "y":
        while portainer_domain == '':
            portainer_domain = input("What domain name would you like to use for portainer? : ")
            portainer_domain = portainer_domain.lower().strip()

docker_gpg_url = "https://download.docker.com/linux/ubuntu/gpg"
docker_apt_url = "https://download.docker.com/linux/ubuntu"


def subprocess_run(command):
    subprocess.run(command, shell=True, check=True)


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

if use_portainer == "y":
    try:
        print("Setting up Portainer")
        subprocess_run("docker volume create portainer_data")
        if portainer_domain == 0:
            subprocess_run("docker run -d --restart=unless-stopped -p 8000:8000 -p 9000:9000 --name portainer -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer")
        elif portainer_domain != 0:
            subprocess_run("docker run -d --restart=unless-stopped -p 8000:8000 -p 9000:9000 --name portainer -e VIRTUAL_HOST={} -e LETSENCRYPT_HOST={} -e LETSENCRYPT_EMAIL={} -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer".format(portainer_domain, portainer_domain, reverseproxy_email))
    except Exception as e:
        print(e)
        print("Error setting up Portainer")
        exit(1)

if use_reverseproxy == 'y':
    try:
        print("Setting up the Reverse Proxy and LetsEncrypt Helper")
        subprocess_run("docker run --detach --restart=unless-stopped --name nginx-proxy --publish 80:80 --publish 443:443 --volume /etc/nginx/certs --volume /etc/nginx/vhost.d --volume /usr/share/nginx/html --volume /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy")
        subprocess_run("docker run --detach --restart=unless-stopped --name nginx-proxy-letsencrypt --volumes-from nginx-proxy --volume /var/run/docker.sock:/var/run/docker.sock:ro --env " + reverseproxy_email + " jrcs/letsencrypt-nginx-proxy-companion")
    except Exception as e:
        print(e)
        print("Error Setting up the Reverse Proxy and the LetsEncrypt Helper")
        exit(1)

try:
    print("Doing final updates and rebooting")
    subprocess_run("apt update -y")
    subprocess_run("apt upgrade -y")
    subprocess_run("apt dist-upgrade -y ")
    subprocess_run("apt autoremove -y")
    subprocess_run("apt autoclean -y")
    print("")
    print("")
    print("")
    print(64 * "-")
    print("Host Prep Process is complete")
    print("")
    print("Rebooting host now - reconnect when reboot is complete")
    print("")
    if use_portainer == 1:
        print("Portainer should be available ")


    subprocess_run("reboot")
except Exception as e:
    print(e)
    print("Error doing final updates and rebooting")
