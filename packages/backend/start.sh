#!/bin/bash

# Setup up networking
bash $PWD/scripts/network_debug_port.sh
bash $PWD/scripts/network_bridge.sh
bash $PWD/scripts/network_hotspot.sh

# Source virtual environment
source $PWD/venv/bin/activate

# (Re)Start the server
pm2 start $PWD/ecosystem.config.js