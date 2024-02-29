#!/bin/bash

while true; do
    # eth0 (debug port) ip
    eth0_ip=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    # wlan0 (hotspot) ip
    wlan0_ip=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    # wlan1 (bridge) ip
    wlan1_ip=$(ip -4 addr show wlan1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

    # If wlan1 is none, scan for available wifi networks
    if [ -z "$wlan1_ip" ]; then
        printf "Scanning for available wifi networks...\n"
        wifi_networks = nmcli device wifi list > /dev/null

        # If "MIA Connect Bridge" is available, connect to it
        if [[ $wifi_networks == *"MIA Connect Bridge"* ]]; then
            printf "Connecting to MIA Connect Bridge...\n"
            nmcli device wifi connect "MIA Connect Bridge" password "miaconnect" ifname wlan1
        else
            printf "MIA Connect Bridge not available\n"
        fi
    fi

    printf "eth0: $eth0_ip\n"
    printf "wlan0: $wlan0_ip\n"
    printf "wlan1: $wlan1_ip\n"

    if ! ping -q -c 1 -W 1 8.8.8.8 > /dev/null; then
        printf "No internet connection available\n"
    else
        printf "Internet connection available\n"
    fi

    sleep 5
done