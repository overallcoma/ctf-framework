#!/bin/bash
HASHPASS=$(</app/hash.txt)
sed -i "s/HASHPASSREPLACE/${HASHPASS}/g" /db/dbsetup.sql
