#!/bin/bash
## This script executes nfs_boot.py and run minicom-
## To modify the NFS server IP address, edit nfs_boot.py
## Sam 28/06/13

echo 
echo " Setting up the U-boot environment .............."
python "/home/obs/nfs_boot.py"

minicom

exit 0



