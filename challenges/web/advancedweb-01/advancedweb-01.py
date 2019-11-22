import argparse
import subprocess
import os

image_name = "ctf/advancedweb-02"
container_name = "ctf-advancedweb-02"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
args = parser.parse_args()

flag = args.flag

if flag == None:
    print("please specify a flag with -f")
    exit(1)


file = open('dockerfile', 'w+')
file.write(dockerfile)
file.close()
call(["docker", "build", "-t", "ctf/ctf-basicweb-06:latest", "."])
containername = "CTF-BasicWeb-06-" + str(password)
flag_env_variable = "FLAG=" + flag
password_env_variable = "PASSWORD=" + password
call(["docker", "run", "-d", "--name", containername, "-e", flag_env_variable, "-e", password_env_variable, "ctrl/ctf-basicweb-06"])
remove('dockerfile')
