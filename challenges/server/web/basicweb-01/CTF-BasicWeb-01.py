from subprocess import call
from os import remove
import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
parser.add_argument("-p", "--password", dest="password", help="Manually specify a password (optional)")
args = parser.parse_args()
flag = args.flag
password = args.password

if flag is None:
    print("please specify a flag with -f")
    exit(1)

if password is None:
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

dockerfile = """FROM alpine:latest
RUN mkdir -p /app/
WORKDIR /app
COPY requirements.txt /app
COPY apk-requirements.txt /app
COPY CTF-BasicWeb-01-Launcher.py /app

RUN apk update
RUN cat "apk-requirements.txt" | xargs -n1 apk add;

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir /db
RUN touch /db/password.db
RUN chown apache:apache /db/password.db
RUN rm -rf /var/www/localhost/htdocs
RUN ln -s /app /var/www/localhost/htdocs
RUN mkdir /run/apache2
RUN touch httpd.pid
EXPOSE 80
CMD ["python3", "/app/CTF-BasicWeb-01-Launcher.py"]
"""

file = open('dockerfile', 'w+')
file.write(dockerfile)
file.close()
call(["docker", "build", "-t", "ctrl/ctf-basicweb-01:latest", "."])
containername = "CTF-BasicWeb-01-" + str(password)
flag_env_variable = "FLAG=" + flag
password_env_variable = "PASSWORD=" + password
call(["docker", "run", "-d", "--name", containername, "-e", flag_env_variable, "-e", password_env_variable, "ctrl/ctf-basicweb-01"])
remove('dockerfile')
