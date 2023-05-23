#!/bin/bash

while true; do

    if python3.11 main.py; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] - Script ran successfully"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] - Script Failed"
    fi

    sleep 24h
done
