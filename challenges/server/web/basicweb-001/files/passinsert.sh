#!/bin/bash
HASHPASS=$(<hash.txt)
sed -i "s/HASHPASSREPLACE/${HASHPASS}/g" /db/dbsetup.sql
sqlite3 /db/password.db < /db/dbsetup.sql
