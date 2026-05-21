#!/bin/bash

pkill -f chrome || true
pkill -f chromium || true
pkill -f playwright || true

while true
do
    echo "Starting runner..."
    python runner.py

    echo "Runner exited, restarting..."

    pkill -f chrome || true
    pkill -f chromium || true
    pkill -f playwright || true

    sleep 10
done
