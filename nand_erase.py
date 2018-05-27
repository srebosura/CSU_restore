#!/usr/bin/env python
### 
### Added by Sam 12/05/14

import time
import serial

ser = serial.Serial('/dev/ttyUSB0',115200)
ser.write("nand erase 200000 9999999\r\n")
time.sleep(4)
ser.close()
