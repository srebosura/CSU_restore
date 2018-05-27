#!/usr/bin/env python
### Change the IP address if any changes in NFS server.
### by Sam 24/06/13

import time
import serial

ser = serial.Serial('/dev/ttyUSB0',115200)
ser.write("setenv serverip_fixed 192.168.1.1\r\n")
time.sleep(1)
ser.write("setenv set_ip 'run initphy;sleep 3;setenv autoload no;dhcp\r\n")
time.sleep(1)
ser.write("setenv serverip ${serverip_fixed}'\r\n")
time.sleep(1)
ser.write("setenv nfsload 'nfs 0xc0700000 ${serverip}:/home/nfs/case_a3/rootfs/boot/uImage'\r\n")
time.sleep(1)
ser.write("setenv nfsroot '/home/nfs/case_a3/rootfs'\r\n")
time.sleep(1)

ser.write("setenv set_bootargs_nfs 'setenv bootargs ${bootargs_nfs} nfsroot=${serverip}:${nfsroot} ethaddr=${ethaddr}'\r\n")
time.sleep(1)
ser.write("run nfsboot\r\n")
time.sleep(1)
ser.close()

