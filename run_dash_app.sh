#!/bin/bash

if [ "$DEBUG" = true  ]; then
    python index.py --host 0.0.0.0 --port 8050 --debug
else
    gunicorn index:server -b :8050 -w 12
fi
