import argparse
import random
import string
import pyotp
import sqlite3
import time
from subprocess import call
from os import remove

# parser = argparse.ArgumentParser()
# parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
# args = parser.parse_args()
#
# flag = args.flag
#
# if flag == None:
#     print("please specify a flag with -f")
#     exit(1)

flag = "testflag001"

checkpass1name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
loginsuccess1name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
checkpass2name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
loginsuccess2name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])

checkpass1name += ".php"
loginsuccess1name += ".php"
checkpass2name += ".php"
loginsuccess2name += ".php"

secretkey = open('seed.txt', 'r')
secretkey = secretkey.read()

onetimepad = pyotp.TOTP(secretkey)

dbfile = "~/password.db"


def dbconnect(dbfile):
    try:
        connection = sqlite3.connect(dbfile)
        print(sqlite3.version)
        connection.close()
    except sqlite3.Error as t:
        print(t)
        exit(1)


def db_createtable(dbfile):
    try:
        connection = sqlite3.connect(dbfile)
        cursor = connection.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS passwords (record_number integer PRIMARY KEY AUTOINCREMENT, password text)'
        cursor.execute(sql)
    except sqlite3.Error as t:
        print(t)
        exit(1)


def write_password(dbfile, password):
    try:
        connection = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        droptablestatement = "DROP TABLE IF EXISTS password"
        cursor.execute(droptablestatement)
        db_createtable(dbfile)
        cursor.execute("INSERT INTO password VALUES (NULL, ?)", (password))
        connection.commit()
        connection.close()
    except sqlite3.Error as t:
        print(t)


indexphp = """<html>
<head>
{0}
</head>
<body>
<form name="checkpage1" method="post" action="checkpass1.php"
Pick a number between 000 and 999 <input type="text" name="number1"><br>
<input type="submit">
</form>
</body>
</html>""".format(secretkey)

checkpass1php = """<?php

$sqlconnect = new PDO('sqlite:/~/password.db');

$userpass = $_POST['number1']
$userpass = stripslashes($userpass)

$tblname = passwords
$sql = "SELECT * FROM $tblname WHERE password='$userpass' AND record_number='1';
$results = mysql_query($sql) 

$count=mysql_num_rows($result);

if($count==1){

session_register("userpass");
header("location:login_success_1.php");
}
else {
echo "Wrong Password";
}
?>
"""

loginsuccess1php = """<?php
session_start();
if(!session_is_registered(userpass)){
header("location:index.php");
}
?>

<html>
<head>
{0}
</head>
<body>
<form name="checkpage2" method="post" action="checkpass2.php"
Pick another number between 000 and 999 <input type="text" name="number2"><br>
<input type="submit">
</form>
</body>
</html>
"""

checkpass2php = """<?php

$sqlconnect = new PDO('sqlite:/~/password.db');

$userpass = $_POST['number2']
$userpass = stripslashes($userpass)

$tblname = passwords
$sql = "SELECT * FROM $tblname WHERE password='$userpass' AND record_number='2';
$results = mysql_query($sql) 

$count=mysql_num_rows($result);

if($count==1){

session_register("userpass");
header("location:login_success_2.php");
}
else {
echo "Wrong Password";
}
?>
"""

loginsuccess2php = """<?php
session_start();
if(!session_is_registered(userpass)){{
header("location:index.php");
}}
?>
<html>
<head>
A Winner is You
</head>
<body>
{0}
</body>
</html>
""".format(flag)

# print(onetimepad.now())
# time.sleep(30)

# dockerfile = """FROM tutum/apache-php
# COPY index.php /app
# COPY gotopage.php /app
# COPY {0} /app
# COPY 404.html /app
# COPY .htaccess /app""".format(randompagenumber)
#
# file = open('index.php', 'w+')
# file.write(indexphp)
# file.close()
# file = open('gotopage.php', 'w+')
# file.write(gotopagephp)
# file.close()
# file = open(randompagenumber, 'w+')
# file.write(targetpage)
# file.close()
# file = open('404.html', 'w+')
# file.write(errorpage)
# file.close()
# file = open('.htaccess', 'w+')
# file.write(htaccess)
# file.close()
# file = open('dockerfile', 'w+')
# file.write(dockerfile)
# file.close()
#
# call(["docker", "build", "-t", "ctrl/ctf-numbercruncher", "."])
# containername = "CTF-MFANumberCruncher-" + str(secretkey)
# call(["docker", "run", "-d", "--name", containername, "-e", "ALLOW_OVERRIDE=true", "ctrl/ctf-numbercruncher"])
#
# remove('index.php')
# remove('gotopage.php')
# remove(randompagenumber)
# remove('404.html')
# remove('.htaccess')
# remove('dockerfile')
