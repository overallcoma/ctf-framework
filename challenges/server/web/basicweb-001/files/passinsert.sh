#!/bin/bash
HASHPASS=$1
sed -i "s/HASHPASSREPLACE/$HASHPASS/g" /db/dbsetup.sql
