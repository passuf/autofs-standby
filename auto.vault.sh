#!/bin/bash

# Enable USB Ports
/home/pi/uhubctl/uhubctl -l 1-1 -a on > /dev/null 2>&1

# Wait until disk is ready
while ! dd if=/dev/disk/by-uuid/20fd4075-06f4-4dff-b3b4-fda98b244809 bs=1 count=10 > /dev/null 2>&1 ;
do
	sleep 1
done

# Return options used by autofs
echo "-fstype=ext4 :/dev/disk/by-uuid/20fd4075-06f4-4dff-b3b4-fda98b244809"
