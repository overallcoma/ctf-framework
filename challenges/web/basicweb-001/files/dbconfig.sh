#!/bin/bash

HASHPASS=$(</var/www/html/hash.txt)
FLAGPAGE=$(</var/www/html/flagpage.txt)
sqlite3 /db/password.db "DROP TABLE IF NOT EXISTS passwords;"
sqlite3 /db/password.db "CREATE TABLE IF NOT EXISTS passwords (record_number integer PRIMARY KEY AUTOINCREMENT, password TEXT, pagename TEXT)"
sqlite3 /db/password.db "INSERT INTO passwords (password, pagename) VALUES ('$HASHPASS','$FLAGPAGE')"
