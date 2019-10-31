import subprocess
import platform
import os
import ctff_functions

target_OS = "Ubuntu-18.04"

if target_OS not in platform.platform():
    print("This script is only intended for Ubuntu 18.04")
    exit(1)

# This script must be run as root!
if not os.geteuid() == 0:
    print("This script must be run as root")
    exit(1)


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


reverseproxy_email = 0
portainer_domain = 0

use_portainer = yes_no_input("Do you want to install Portainer?")
use_reverseproxy = yes_no_input("Do you want to install the reverse proxy with LetsEncrypt?")
if use_reverseproxy == 1:
    while reverseproxy_email == 0:
        reverseproxy_email = input("Please enter email address to use for reverse proxy:  ")
        reverseproxy_email = reverseproxy_email.lower().strip()
    if use_portainer == 1:
        while portainer_domain == 0:
            portainer_domain = input("What domain name would you like to use for portainer? : ")
            portainer_domain = portainer_domain.lower().strip()
            if portainer_domain == "":
                portainer_domain = 0

docker_gpg_url = "https://download.docker.com/linux/ubuntu/gpg"
docker_apt_url = "https://download.docker.com/linux/ubuntu"

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

if use_portainer == 1:
    try:
        print("Setting up Portainer")
        docker_client = ctff_functions.create_client()

        docker_client.volumes.create("portainer")

        portainer_name = "portainer"
        portainer_restartpolicy = {"name": "unless-stopped"}
        portainer_ports = {"8000/tcp": 8000, "9000/tcp": 9000}
        portainer_volumes = {
            "/var/run/docker.sock": {
                "bind": "/var/run/docker.sock",
                "mode": "rw"},
            "portainer_data": {
                "bind": "/data",
                "mode": "rw"
            }
        }
        portainer_image = "portainer"

        if portainer_domain == 0:
            docker_client.containers.run(
                detach=True,
                name=portainer_name,
                restart_policy=portainer_restartpolicy,
                ports=portainer_ports,
                publish_all_ports=True,
                volumes=portainer_volumes,
                image=portainer_image
            )
            # subprocess_run("docker run -d --restart=unless-stopped -p 8000:8000 -p 9000:9000 --name portainer -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer")
        elif portainer_domain != 0:
            portainer_envvars = {
                "VIRTUAL_HOST": portainer_domain,
                "LETSENCRYPT_HOST": portainer_domain,
                "LETSENCRYPT_EMAIL": reverseproxy_email,
                "VIRTUAL_PORT": "9000"
            }
            docker_client.containers.run(
                detach=True,
                name=portainer_name,
                restart_policy=portainer_restartpolicy,
                ports=portainer_ports,
                volumes=portainer_volumes,
                environment=portainer_envvars,
                image=portainer_image
            )
            # subprocess_run("docker run -d --restart=unless-stopped -p 8000:8000 -p 9000:9000 --name portainer -e VIRTUAL_HOST={} -e LETSENCRYPT_HOST={} -e LETSENCRYPT_EMAIL={}  -e VIRTUAL_PORT=9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer".format(portainer_domain, portainer_domain, reverseproxy_email))
        docker_client.close()
    except Exception as e:
        print(e)
        print("Error setting up Portainer")
        exit(1)

if use_reverseproxy == 1:
    try:
        print("Setting up the Reverse Proxy and LetsEncrypt Helper")
        docker_client = ctff_functions.create_client()

        docker_client.volumes.create("nginx_certs")
        docker_client.volumes.create("nginx_vhostd")
        docker_client.volumes.create("nginx_html")

        nginxproxy_name = "nginx-proxy"
        nginxproxy_restartpolicy = {"name": "unless-stopped"}
        nginxproxy_ports = {"80/tcp": 80, "443/tcp": 443}
        nginxproxy_volumes = {
            "nginx_certs": {
                "bind": "/etc/nginx/certs",
                "mode": "rw"},
            "nginx_vhostd":{
                "bind": "/etc/nginx/vhost.d",
                "mode": "rw"},
            "nginx_html":{
                "bind": "/usr/share/nginx/html",
                "mode": "rw"},
            "/var/run/docker.sock": {
                "bind": "/tmp/docker.sock",
                "mode": "ro"}
            }
        nginxproxy_image = "jwilder/nginx-proxy"
        docker_client.containers.run(
            detach=True,
            name=nginxproxy_name,
            restartpolicy=nginxproxy_restartpolicy,
            ports=nginxproxy_ports,
            volumes=nginxproxy_volumes,
            image=nginxproxy_image
        )

        nginxproxycompanion_name = "nginx-proxy-letsencrypt"
        nginxproxycompanion_restartpolicy = {"Name": "unless-stopped"}
        nginxproxycompanion_volumesfrom = ["nginx-proxy"]
        nginxproxycompanion_volumes = {
            "/var/run/docker.sock": {
                "bind": "/var/run/docker.sock",
                "mode": "ro"}
        }
        nginxproxycompanion_envvars = {
            "LETSENCRYP_EMAIL": reverseproxy_email}
        nginxproxycompanion_image = "jrcs/letsencrypt-nginx-proxy-companion"
        docker_client.containers.run(
            detach=True,
            name=nginxproxycompanion_name,
            restartpolicy=nginxproxycompanion_restartpolicy,
            volumes_from=nginxproxycompanion_volumesfrom,
            volumes=nginxproxycompanion_volumes,
            image=nginxproxycompanion_image
        )

        docker_client.close()


        # subprocess_run("docker run --detach --restart=unless-stopped --name nginx-proxy --publish 80:80 --publish 443:443 --volume /etc/nginx/certs --volume /etc/nginx/vhost.d --volume /usr/share/nginx/html --volume /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy")
        # subprocess_run("docker run --detach --restart=unless-stopped --name nginx-proxy-letsencrypt --volumes-from nginx-proxy --volume /var/run/docker.sock:/var/run/docker.sock:ro --env " + reverseproxy_email + " jrcs/letsencrypt-nginx-proxy-companion")
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
    if use_portainer == 1 and portainer_domain == 0:
        print("Portainer should be available on port 9000 of this host after reboot")
        print("")
    if use_portainer == 1 and isinstance(portainer_domain, str):
        print("Portainer should be available at https://{} after reboot is complete".format(portainer_domain))
        print("")
    if use_portainer ==1:
        print("-----PLEASE CONNECT TO PORTAINER AND SECURE IT AFTER REBOOT-----")
        print("")
    print(64 * "-")
    subprocess_run("reboot")
except Exception as e:
    print(e)
    print("Error doing final updates and rebooting")
