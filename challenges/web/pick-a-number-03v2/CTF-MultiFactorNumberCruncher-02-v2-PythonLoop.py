import pyotp
import sqlite3
import time
import datetime
import string
import shutil
import random
from os import remove


secretkey = open('seed.txt', 'r')
secretkey = secretkey.read()
onetimepad = pyotp.TOTP(secretkey)
index_location = "./index.php"

dbfile = "/db/password.db"
old_time_string = "!!!NO TIME PRESENT!!!"

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


def newtime():
    min_year = 1970
    max_year = datetime.datetime.now().year
    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    random_date = start + (end - start) * random.random()
    random_date = random_date.replace(microsecond=0)
    return random_date


def replace_date(old_date, new_date, file_input):
    file_open = open(file_input, 'r')
    file_open_read = file_open.read()
    line_replaced = file_open_read.replace(old_date, new_date)
    file_open.close
    file_open = open(file_input, 'w')
    file_open.write(line_replaced)
    file_open.close()


while True:
    target_time = newtime()
    target_time_string = target_time.strftime("%A, %B %d, %Y  --  %H:%M:%S")
    target_time_timestamp = target_time.timestamp()
    password = onetimepad.at(target_time_timestamp)
    previouspage1 = page1name
    previouspage2 = page2name
    replace_date(old_time_string, target_time_string, index_location)
    replace_date(old_time_string, target_time_string, previouspage1)
    page1name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
    page2name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
    page1name = page1name + ".php"
    page2name = page2name + ".php"
    filemove(previouspage1, page1name)
    filemove(previouspage2, page2name)
    password1 = password[:3]
    password2 = password[-3:]
    write_password(dbfile, password1, page1name, password2, page2name)
    time.sleep(60)
    old_time = target_time
    old_time_string = target_time_string
