#!/bin/bash
## Will run full rootfs recovery 
## 
## Sam 21/07/13
## Will now SET AND DETECT U-BOOT PROMPT
## updated 09.05.18
## last update 19.02.20
## for csu restore app use
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

tty="$1"
csu_serialno="$2"
tty1="$3"
today="$(date +%m%d%H%M%Y)"
csu_serialno="$2"
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
python /home/obs/sam/rootfs/tools/csu_power.py $tty1
echo ""
echo "Waiting for U-Boot prompt .............."
echo ""
python /home/obs/sam/rootfs/tools/set_uboot.py $tty
echo ""
echo -n "Executing nand erase on boot and rootfs ....."
sleep 1
#read success <&1

#if [ "$success" == "y" ]; then
        echo ""
        echo "U-Boot >nand erase 200000 9999999 "
        echo ""
        echo "Please wait .........."
        python /home/obs/sam/rootfs/tools/nand_erase.py $tty
        sleep 1
        echo ""        
        echo "Nand boot and rootfs erased!"
#fi
sleep 1
#clear
echo ""
echo "$csu_serialno"
mac_m="$(grep $csu_serialno -A2 /home/obs/sam/rootfs/tools/MAC_0013-1642.txt | awk 'NR==2')"
mac_s="$(grep $csu_serialno -A2 /home/obs/sam/rootfs/tools/MAC_0013-1642.txt | awk 'NR==3')"
echo "Set Mac done!"
#sleep 1
/home/obs/sam/rootfs/tools/./set_uboot_env.sh -p $tty -m $mac_m -s $mac_s uboot_env.conf

sleep 2

echo""
echo " Setting up the U-boot environment .............."
sleep 1
python /home/obs/sam/rootfs/tools/nfs_boot.py $tty
sleep 2
minicom -D $tty

exit 0



