#!/usr/bin/env bash

# Copyright (C) 2023 Patrick Pedersen, TUDO Makerspace

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Author: Patrick Pedersen <ctx.xda@gmail.com>
# Brief Description: Sets up the activity-indicator backdoor bot server

################################################################################################
# NOTE: As of now, this script does not take care of dependencies!
#	Please launch the backdoor server manually first to check for missing dependencies
################################################################################################

# Usage: See ./setup.sh help

BIN_DIR=/usr/local/sbin
CFG_DIR=/var/lib/activity-indicator-backdoor
SYSTEMD_DIR=/etc/systemd/system

# Get directory of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR="$SCRIPT_DIR"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
elif [[ "$1" == "install" ]]; then
	echo "Installing activity-indicator backdoor server"

        cp -v $PROJECT_DIR/activity-indicator-backdoor.py $BIN_DIR/activity-indicator-backdoor
        chmod +x $BIN_DIR/activity-indicator-backdoor

        mkdir -p $CFG_DIR
        cp -v $PROJECT_DIR/activity-indicator-backdoor.ini $CFG_DIR/activity-indicator-backdoor.ini

        echo "Setting up systemd service..."
        cp -v $PROJECT_DIR/activity-indicator-backdoor.service $SYSTEMD_DIR/activity-indicator-backdoor.service

        # Stop service if running
        echo "Stopping systemd service (if running)..."
        systemctl stop activity-indicator-backdoor.service

        # Disable service if enabled
        echo "Disabling systemd service (if enabled)..."
        systemctl disable activity-indicator-backdoor.service

        echo "Enabling systemd service..."
        systemctl enable activity-indicator-backdoor.service

        echo "Starting systemd service..."
        systemctl start activity-indicator-backdoor.service

        echo "Installation complete, the telegram bot should now be running"
elif [ "$1" == "uninstall" ]; then
        echo "Uninstalling..."
        rm -v -r $BIN_DIR/activity-indicator-backdoor
        rm -v -r $CFG_DIR
        rm -v -r /etc/systemd/system/activity-indicator-backdoor.service

        echo "Uninstallation complete"
else
        if [ "$1" != 'help' ]; then
                echo "Unknown or missing argument"
                echo
        fi
        echo "Usage: ./setup.sh [help|install|uninstall]"
        echo
        echo -e "\thelp:\t\tDisplays this message"
        echo -e "\tinstall:\tSets up and enables the Activity Indicator backdoor server"
        echo -e "\tuninstall:\tStops and removes the Activity Indicator backdoor server"
        echo
fi