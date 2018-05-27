#!/bin/bash
## This script executes nfs_boot.py and run minicom
## To modify the NFS server IP address, edit nfs_boot.py
## Sam 28/06/13

echo""
echo " Setting up the U-boot environment .............."
sleep 1
python "/home/obs/tools/nfs_boot.py"
sleep 1
minicom -D /dev/ttyUSB0

exit 0



