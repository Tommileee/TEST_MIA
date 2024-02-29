#!/bin/bash

if ! [ -f /etc/NetworkManager/system-connections/mia-connect.nmconnection ]; then
    echo "root" | sudo nmcli con add type wifi ifname wlan0 con-name "mia-connect" autoconnect yes ssid "MIA Connect" mode ap ipv4.method shared
    echo "root" | sudo nmcli con modify "mia-connect" 802-11-wireless-security.key-mgmt wpa-psk 802-11-wireless-security.psk "miaconnect"
fi
    
echo "root" | sudo nmcli con up mia-connect