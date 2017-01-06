#!/bin/bash
while [ true ]
do
    clear
    echo "Updating Discord..."
    sudo -H python3 -m pip install -U discord.py
    echo "Discord Updated!!"
    clear
    echo "Starting Bot..."
    python3 chiaki.py
    clear
    wait 4
done

