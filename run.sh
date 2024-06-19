#!/bin/bash

# Check if script is run as root
if [ "$EUID" -ne 0 ]
then
    echo "This script must be run as root."
    exit
fi

# Navigate to the directory containing the Python script
cd /path/to/your/python/script/directory  # Replace with actual path

# Run the Python script
sudo python3 trokinter.py
