#!/bin/bash

ERR_LOG=./data/error.log
RUN_LOG=./data/run.log

while true; do
    python3.11 main.py >> $ERR_LOG 2>&1

    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] - Script ran successfully" >> $RUN_LOG
    fi

    sleep 24h
done