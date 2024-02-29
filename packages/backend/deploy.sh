#!/bin/bash

DEPLOYMENT_LOG_FILE="/tmp/deployment.log"
SUDO_PASSWORD="root"

function log {
    local current_time=$(date "+%Y.%m.%d-%H.%M.%S")
    printf "$current_time $1\n" 2>&1 | tee -a $DEPLOYMENT_LOG_FILE
}

# Check if no internet connection is available
if ! ping -q -c 1 -W 1 8.8.8.8 > /dev/null; then
    bash $PWD/scripts/network_bridge.sh
    log "No internet connection available"

    #bash $PWD/scripts/wait_for_internet.sh
else
    log "Internet connection available"
fi

# Installing dependencies

log "Installing dependencies..."

echo $SUDO_PASSWORD | sudo apt-get update
echo $SUDO_PASSWORD | sudo apt-get install -y $(cat requirements/apt.txt)

# Create venv
log "Creating venv..."

python3 -m venv venv
source venv/bin/activate

log "Installing requirements..."

pip install -r requirements/pip.txt

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    log "Node.js is not installed"
    exit 1
fi

# Check if pm2 is installed
if ! command -v pm2 &> /dev/null; then
    log "pm2 is not installed"
    exit 1
fi

# Check if "pm2 monit" is in ~/.bashrc
if ! grep -q "pm2 monit" ~/.bashrc; then
    log "Adding 'pm2 monit' to ~/.bashrc..."

    echo "pm2 monit" >> ~/.bashrc
fi

log "Finished deployment"

if [ -f /etc/systemd/system/mia-backend.service ]; then
    log "Found existing autostart for mia-backend..."


    # Stop service
    echo $SUDO_PASSWORD | sudo systemctl stop mia-backend.service
    # Disable autostart
    echo $SUDO_PASSWORD | sudo systemctl disable mia-backend.service
    # Delete service file
    echo $SUDO_PASSWORD | sudo rm /etc/systemd/system/mia-backend.service

    log "Autostart for mia-backend removed"
fi

# Check if autostart for mia-backend is configured
if ! [ -f /etc/systemd/system/mia-backend.service ]; then
    log "Configuring autostart for mia-backend..."

    # Copy service file
    echo $SUDO_PASSWORD | sudo cp $PWD/scripts/mia-backend.service /etc/systemd/system/mia-backend.service

    # Reload systemd
    echo $SUDO_PASSWORD | sudo systemctl daemon-reload

    # Enable autostart
    echo $SUDO_PASSWORD | sudo systemctl enable mia-backend.service

    log "Autostart for mia-backend configured"
fi

# Restart raspberry pi
log "Restarting raspberry pi..."

echo $SUDO_PASSWORD | sudo reboot