import subprocess
from subprocess import call
from os import remove
import random
import string


flag = ''
password = ''
while flag == "":
    flag = input("Please enter the desired flag: ")
while password == "":
    print("Please enter the password that will be hidden")
    input("Or enter \"random\" to generate a random flag: ")
if password == "random":
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Read in the page data
dockerfile_data = open("./files/dockerfile", "r").read()
error_page_data = open("./files/errorpage.html", "r").read()
flag_page_data = open("./files/flagpage.html", "r").read()
htaccess_data = open("./files/htaccess", "r").read()
index_page_data = open("./files/index.php", "r").read()
passhashgen_page_data = open("./files/passhashgen.php", "r").read()

# Replace variables in file data
flag_page_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)]) + ".html"
flag_page_data = flag_page_data.replace("$FLAG$", flag)
dockerfile_data = dockerfile_data.replace("$FLAGPAGE$", flag_page_name)
dockerfile_data = dockerfile_data.replace("$PASSWORD$", password)
passhashgen_page_data = passhashgen_page_data.replace("$PASSWORD$", password)

# Open new files we will be writing
dockerfile_temp = open("./dockerfile", "w+")
error_page_temp = open("./errorpage.html", "w+")
flag_page_temp = open("./flagpage.html", "w+")
htaccess_temp = open("./htaccess", "w+")
index_page_temp = open("./index.php", "w+")
passhashgen_page_temp = open("./passhashgen.php", "w+")

# Write the data to the target files
dockerfile_temp.write(dockerfile_data)
error_page_temp.write(error_page_data)
flag_page_temp.write(flag_page_data)
htaccess_temp.write(htaccess_data)
index_page_temp.write(index_page_data)
passhashgen_page_temp.write(passhashgen_page_data)

# Close the files to save the data
dockerfile_temp.close()
error_page_temp.close()
flag_page_temp.close()
htaccess_temp.close()
index_page_temp.close()
passhashgen_page_temp.close()

# Do all the work and create the container
flag_env_variable = "FLAG=" + flag
password_env_variable = "PASSWORD=" + password
containername = "basicweb-001 - " + str(password)
subprocess.call(["docker", "build", "-t", "ctff/basicweb-001", "."])
subprocess.call(["docker", "run", "-d", "--name", containername, "-e", flag_env_variable, "-e", password_env_variable, "ctff/basicweb-001"])
