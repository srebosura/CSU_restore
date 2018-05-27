#!/bin/bash
## Will run full rootfs recovery 
## 
## Sam 21/07/13
## Will now SET AND DETECT U-BOOT PROMPT
## last modified 09.05.18

clear
echo "U-Boot/Rootfs Recovery Version 09.05.18"
echo ""
echo ""
#echo "Hit (F) if you want to flash u-boot... "
#echo ""
#echo -e "For RootFS/KERNEL recovery! Press (Y) to continue!: \c"
#read is_confirm



#case "$is_confirm" in 

#"y" | "Y" )
#echo
#echo "4 digit serial is a must, (ex. 0013) !!!"
#echo
#echo -e "Enter the 4 digit  CSU serial number   : \c "

today="$(date +%m%d%H%M%Y)"
csu_serialno="$1"
echo "$csu_serialno       $today">> /home/obs/sam/rootfs/tools/csu_restore.log
#;;

#"f" | "F" )
#./flash_uboot.sh -p ttyUSB0 u-boot-NAND_ais.bin

#echo "Repower and reboot CSU!"
#exit 0
#;;


#* ) 
#exit 0
#;;

#esac

echo ""
echo "Please connect serial, network cable and power supply to the CSU!"
echo ""
echo "Turn POWER-ON / Boot the CSU!"
echo ""
echo "Waiting for U-Boot prompt .............."
echo ""
python /home/obs/tools/set_uboot.py
echo ""
echo -n "Executing nand erase on boot and rootfs ....."
sleep 1
#read success <&1

#if [ "$success" == "y" ]; then
        echo ""
        echo "U-Boot >nand erase 200000 9999999 "
        echo ""
        echo "Please wait .........."
        python /home/obs/tools/nand_erase.py
        sleep 1
        echo ""        
        echo "Nand boot and rootfs erased!"
#fi

sleep 2
clear
echo ""
mac_m="$(grep $csu_serialno -A2 /home/obs/tools/MAC_0013-1582.txt | awk 'NR==2')"
mac_s="$(grep $csu_serialno -A2 /home/obs/tools/MAC_0013-1582.txt | awk 'NR==3')"
#sleep 1
/home/obs/tools/./set_uboot_env.sh -p ttyUSB0 -m $mac_m -s $mac_s uboot_env.conf

sleep 2

/home/obs/tools/./reinstall_rootfs.sh


exit


