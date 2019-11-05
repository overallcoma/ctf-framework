import pyotp
import sqlite3
import time
import string
import random
import shutil
from os import remove


secretkey = open('seed.txt', 'r')
secretkey = secretkey.read()
onetimepad = pyotp.TOTP(secretkey)

dbfile = "/db/password.db"

def dbconnect(dbfile_func):
    try:
        connection = sqlite3.connect(dbfile_func)
        print(sqlite3.version)
        connection.close()
    except sqlite3.Error as t:
        print(t)
        exit(1)


def initialpagesetup():
    file = open('initialpages.txt', 'r')
    data = file.readlines()
    return data


def write_password(dbfile_func, insert_password1, insert_page1, insert_password2, insert_page2):
    try:
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        droptablestatement = "DROP TABLE IF EXISTS passwords"
        cursor.execute(droptablestatement)
        cursor.close()
        connection.close()
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        createtablestatement = 'CREATE TABLE IF NOT EXISTS passwords (record_number integer PRIMARY KEY AUTOINCREMENT, password integer, pagename text)'
        cursor.execute(createtablestatement)
        connection.commit()
        cursor.close()
        connection.close()
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO passwords VALUES (NULL, ?, ?)", (insert_password1, insert_page1))
        connection.commit()
        cursor.close()
        connection.close()
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO passwords VALUES (NULL, ?, ?)", (insert_password2, insert_page2))
        connection.commit()
        cursor.close()
        connection.close()
    except sqlite3.Error as t:
        print(t)


def filemove(src, dst):
    shutil.move(src, dst)


print("testing database connection")
dbconnect(dbfile)
time.sleep(10)
setuppages = initialpagesetup()
page1name = setuppages[0]
page1name = page1name[:-1]
page2name = setuppages[1]
startcheck = onetimepad.now()
while onetimepad.now() == startcheck:
    time.sleep(1)
remove('seed.txt')
remove('flag.txt')
remove('initialpages.txt')

while True:
    password = onetimepad.now()
    previouspage1 = page1name
    previouspage2 = page2name
    page1name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
    page2name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
    page1name = page1name + ".php"
    page2name = page2name + ".php"
    filemove(previouspage1, page1name)
    filemove(previouspage2, page2name)
    password1 = password[:3]
    password2 = password[-3:]
    write_password(dbfile, password1, page1name, password2, page2name)
    while password == onetimepad.now():
        time.sleep(1)
