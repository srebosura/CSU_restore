#!/bin/bash
## This script locates the mac address of a given CSU serial number
## Sam 29/06/13

echo
echo -e "Enter CSU serial number : \c "
read csu_serialno

mac_m="$(grep $csu_serialno -A2 /home/obs/tools/prodlog_MAC_0013-1420.txt | awk 'NR==2')"
mac_s="$(grep $csu_serialno -A2 /home/obs/tools/prodlog_MAC_0013-1420.txt | awk 'NR==3')"
#sleep 1
#/home/obs/tools/./set_uboot_env.sh -p ttyUSB0 -m $mac_m -s $mac_s uboot_env.conf

echo $mac_m

exit 0



