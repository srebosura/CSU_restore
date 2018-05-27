#!/usr/bin/env python
### 
### Added by Sam 01/05/18

import time
import serial

ser = serial.Serial('/dev/ttyUSB0',115200)
ser.flush()
ser.flushInput()
ser.flushOutput()

while 1:
	ser.write("s\r\n")
	raw_data = ser.readline()
	print(raw_data)
	if raw_data=='U-Boot > s\r\n' or raw_data=='U-Boot > \r\n' :
		print("U-boot prompt detected!")
		break	
ser.close()
