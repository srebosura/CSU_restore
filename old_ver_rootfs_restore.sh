#!/bin/bash
## Will run full rootfs recovery 
## 
## Sam 21/07/13
## last modified 12.05.14

echo ""
echo "Hit (F) if you want to flash u-boot... "
echo ""
echo -e "For rootfs recovery set CSU to U-Boot prompt! Press (Y) to continue!: \c"
read is_confirm

case "$is_confirm" in 

"y" | "Y" )
;;

"f" | "F" )
./flash_uboot.sh -p ttyUSB0 u-boot-NAND_ais.bin

echo "Repower and reboot CSU!"
exit 0
;;


* ) 
exit 0
;;

esac

echo ""
echo -n "Do you want to nand erase boot and rootfs  y/n ?"
read success <&1

if [ "$success" == "y" ]; then
        echo ""
        echo "U-Boot >nand erase 200000 9999999 "
        echo ""
        echo "Please wait .........."
        python /home/obs/tools/nand_erase.py
        echo ""        
        echo "Nand boot and rootfs erased!"
fi

sleep 2
clear
echo ""
/home/obs/tools/./find_mac_uboot_env.sh

sleep 2

/home/obs/tools/./reinstall_rootfs.sh


exit


