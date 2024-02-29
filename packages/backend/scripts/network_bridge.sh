#!/bin/bash

if ! [ -f /etc/NetworkManager/system-connections/mia-connect-bridge.nmconnection ]; then
    echo "root" | sudo nmcli con add con-name "mia-connect-bridge" ifname wlan1 type wifi ssid "MIA Connect Bridge"
    echo "root" | sudo nmcli con modify "mia-connect-bridge" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "miaconnectbridge"
fi

echo "root" | sudo nmcli con up mia-connect-bridge