#!/bin/bash
HASHPASS=$(</var/www/html/hash.txt)
sed -i "s/HASHPASSREPLACE/$HASHPASS/g" /db/dbsetup.sql
