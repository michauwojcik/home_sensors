#!/bin/bash
# load env variables
PROJECT_DIR="/home/michau/Repos/home_sensors"

cd "$PROJECT_DIR" || exit 1

# Activate the virtual environment
source env.sh
source .venv/bin/activate

# Run the Python script and write output to log file
python write_bme280_signals.py >> /home/michau/.cron-logs.log 2>&1
