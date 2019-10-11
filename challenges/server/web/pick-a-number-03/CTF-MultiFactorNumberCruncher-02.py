import pyotp
from subprocess import call
from os import remove
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
args = parser.parse_args()
flag = args.flag

if flag == None:
    print("please specify a flag with -f")
    exit(1)

if flag != None:
    file = open('flag.txt', 'w+')
    file.write(flag)
    file.close()

secretkey = pyotp.random_base32()
print(secretkey)
onetimepad = pyotp.TOTP(secretkey)
print(onetimepad.now())

seedfile = """{0}""".format(secretkey)

file = open('seed.txt', 'w+')
file.write(seedfile)
file.close()

dockerfile = """FROM alpine:latest
RUN mkdir -p /app/
WORKDIR /app
COPY seed.txt /app
COPY requirements.txt /app
COPY CTF-MultiFactorNumberCruncher-02-Launcher.py /app
COPY CTF-MultiFactorNumberCruncher-02-WebSetup.py /app
COPY CTF-MultiFactorNumberCruncher-02-PythonLoop.py /app
COPY flag.txt /app
RUN apk update
RUN apk add python3 --no-cache
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apk add apache2 --no-cache
RUN apk add sqlite  --no-cache
RUN apk add php7 --no-cache
RUN apk add php7-sqlite3 --no-cache
RUN apk add php7-apache2 --no-cache
RUN apk add php-pdo --no-cache
RUN apk add php-pdo_sqlite --no-cache
RUN apk add php-sqlite3 --no-cache
RUN mkdir /db
RUN touch /db/password.db
RUN chown apache:apache /db/password.db
RUN rm -rf /var/www/localhost/htdocs
RUN ln -s /app /var/www/localhost/htdocs
RUN mkdir /run/apache2
RUN touch httpd.pid
EXPOSE 80
CMD ["python3", "/app/CTF-MultiFactorNumberCruncher-02-Launcher.py"]
"""
file = open('dockerfile', 'w+')
file.write(dockerfile)
file.close()
call(["docker", "build", "-t", "ctrl/ctf-mfanumbercruncher-02:latest", "."])
containername = "CTF-MFANumberCruncher-02-" + str(secretkey)
call(["docker", "run", "-d", "--name", containername, "ctrl/ctf-mfanumbercruncher-02"])
remove('seed.txt')
remove('dockerfile')
remove('flag.txt')
