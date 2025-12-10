#!/bin/bash
# load env variables
source env.sh
PROJECT_DIR=$REPO_DIR_PATH

cd "$PROJECT_DIR" || exit 1

# Activate the virtual environment
source .venv/bin/activate

# Run the Python script and write output to log file
python write_bme280_signals.py >> /home/michau/.cron-logs.log 2>&1
