#!/bin/bash

if ! [ -f /etc/NetworkManager/system-connections/mia-debug-port.nmconnection ]; then
    echo "root" | sudo nmcli con add con-name "mia-debug-port" ifname eth0 type ethernet ip4 192.168.1.1/24 gw4 0.0.0.0
fi

echo "root" | sudo nmcli con up mia-debug-port