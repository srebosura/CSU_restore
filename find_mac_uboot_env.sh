#!/bin/bash
## This script locates the mac address of a given CSU serial number
## Sam 29/06/13
## csu_restore.log available at /home/obs/tools/
## modified 03.05.18
echo
echo "4 digit serial is a must, (ex. 0013) !!!"
echo
echo -e "Enter the 4 digit  CSU serial number   : \c "
read csu_serialno
echo $csu_serialno >> /home/obs/tools/csu_restore.log

mac_m="$(grep $csu_serialno -A2 /home/obs/tools/MAC_0013-1582.txt | awk 'NR==2')"
mac_s="$(grep $csu_serialno -A2 /home/obs/tools/MAC_0013-1582.txt | awk 'NR==3')"
#sleep 1
/home/obs/tools/./set_uboot_env.sh -p ttyUSB0 -m $mac_m -s $mac_s uboot_env.conf
exit 0


