#!/bin/bash
HASHPASS=$1
sed -i "s/HASSPASSREPLACE/$HASHPASS/g" /db/dbsetup.sql
