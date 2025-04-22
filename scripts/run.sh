#!/bin/bash
cd build
./medisys_main &
export DB_CONN_STR="dbname=medisys user=$DB_USER password=$DB_PASS host=localhost"
python3 ../src/frontend/python/main.py