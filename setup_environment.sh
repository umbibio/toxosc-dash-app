#!/bin/bash

if [ ! -f .initialized ]; then

    MYSQL_ROOT_PASSWORD=`shuf -er -n96  {A..Z} {a..z} {0..9} | paste -sd ""`
    echo "MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD" > variables_db.env

    MARIADB_PASSWORD=`shuf -er -n96  {A..Z} {a..z} {0..9} | paste -sd ""`
    echo "MARIADB_PASSWORD=$MARIADB_PASSWORD" >> variables_db.env
    echo "MARIADB_PASSWORD=$MARIADB_PASSWORD" > variables.env

    touch .initialized
fi
