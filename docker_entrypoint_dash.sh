#!/bin/bash

if [ ! -f /.initialized ]; then

    echo "getting ready"
    pip install --no-cache-dir --upgrade pip
    pip install --no-cache-dir -r requirements.txt

    touch /.initialized
fi

exec "$@"
