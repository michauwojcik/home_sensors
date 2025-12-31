#!/bin/bash
# load env variables
PROJECT_DIR="/home/michau/Repos/home_sensors"

cd "$PROJECT_DIR" || exit 1

# Activate the virtual environment
source env.sh
source .venv/bin/activate

# Run the Python script and write output to log file
curr_ts=$(date +'%FT%T.%3N') # isoformat, milliseconds
curr_date=$(date +"%F") # isoformat date
log_file=${LOGS_DIR}/${curr_date}_home_sensors.log

echo "[${curr_ts}] Running $0" >> $log_file
python write_bme280_signals.py >> $log_file 2>&1
