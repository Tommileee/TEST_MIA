#!/bin/bash

# Wait indefinitely for internet connection
while ! ping -c 1 8.8.8.8; do
    # Wait for 5 seconds
    sleep 5

    # Check if bridge connection exists
    if ! nmcli con show --active | grep -q $BRIDGE_CONNECTION_NAME; then
        bash ./init_bridge.sh
    fi
    bash ./connect_bridge.sh
done