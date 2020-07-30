#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root (use sudo)" 1>&2
	exit 1
fi

install --mode 0755  mpu-power-daemon.py /usr/local/bin/
cp mpu-power-daemon.service /etc/systemd/system/
systemctl unmask mpu-power-daemon.service
systemctl enable mpu-power-daemon.service
systemctl start  mpu-power-daemon.service

exit 0

