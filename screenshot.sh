#!/bin/bash

SAVE_DIR="$HOME/MOD-AFLGO/analyze/results"
mkdir "$SAVE_DIR"

while true; do
    TIME_STAMP=$(date +"%Y-%m-%d_%H-%M-%S")
    FILE_PATH="$SAVE_DIR/screenshot_$TIME_STAMP.png"

    gnome-screenshot -f "$FILE_PATH"

    echo "[$(date +"%H:%M:%S")] Saved: $FILE_PATH"

    sleep 300
done