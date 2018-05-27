#!/bin/bash
## Will update to the latest SW version OPKGS-v2014.06.01
## 
## Sam 21/01/15

killall -9 sz 2> /dev/null
killall -9 rz 2> /dev/null
killall -9 cu 2> /dev/null
killall -9 minicom 2> /dev/null

python /home/obs/get_serial.py

sleep 1

clear
echo ""
echo -n "Serial/USB port and SIB on CSU must be connected! (y/n) ?"
read success <&1

if [ "$success" == "y" ]; then
        echo ""
        echo "Establishing USB connection ...... "
        echo ""
        echo "Please wait ......................."
        echo ""        

cd /home/obs/tools/scripts/
./sendfile_usb.sh /home/obs/tools/scripts/OPKGS-v2014.06.01

python /home/obs/tools/scripts/exec_cmd.py /dev/ttyUSB0 "mv /data/tmp/OPKGS-v2014.06.01 /tmp;rm -rf /data/tmp/;/tmp/./OPKGS-v2014.06.01;reboot" 180

echo "Please watch the reboot!"
fi
minicom -D /dev/ttyUSB0

exit 0

