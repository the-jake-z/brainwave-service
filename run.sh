#!/usr/bin/env bash

source env/bin/activate

trap 'kill %1;' SIGINT
python osc-server.py &
python webserver.py

