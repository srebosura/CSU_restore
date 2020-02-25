#!/usr/bin/env python
##modified by sam 19.02.20
"""
this file modified to power the CSU
configuration is described in select()
"""

import serial
import sys
"""
import logging
import time
STS = time.gmtime()
FILENAME = "logfiles/%s%s%s.%s.log" % \
                        (STS.tm_year, STS.tm_mon, STS.tm_mday, sys.argv[0])
try:
    logging.basicConfig(
              filename=FILENAME,
              level=logging.DEBUG,
              format="%(levelname)-8s - %(asctime)s - %(message)s",
              )
except IOError:
    print "Error please create logfiles directory"
    sys.exit(1)
FILENAME = "logfiles/%s%s%s.%s.log" % \
                (STS.tm_year, STS.tm_mon, STS.tm_mday, sys.argv[0])
logging.basicConfig(
              filename=FILENAME,
              level=logging.DEBUG,
              format="%(levelname)-8s - %(asctime)s - %(message)s",
              )
"""
################################################################
class MuxPpsOut(object):
    """abstract USB I/O 24R
       used to switch PRL-854RM
    """

    def __init__(self, port="/dev/ttyUSB1"):
        self.port = port
        self.ser = None

    def __open_ser(self):
        if 0 == self.port.find("/dev/tty"):
            self.ser = serial.Serial(self.port, 115200)
            self.ser.timeout = 1
            self.ser.open()
        else:
            self.ser = sys.stdout

    def __close_ser(self):
        if 0 == self.port.find("/dev/tty"):
            self.ser.close()

    def write(self, msg):
        for val in msg:
            self.ser.write(chr(val))
        self.ser.flush()

    def read(self):
        ret = self.ser.read(1)
        while ret:
            print ret
            ret = self.ser.read(1)

    def identify_device(self):
        """will show:
           USB I/O 24R1
        """
        import time
        cmd = [0x3f]
        self.write(cmd)
        time.sleep(1)
        self.read()

    def configure_as_output(self):
        """ port A and B are configured as output"""
        self.__open_ser()
        # NOTE: port C would be 0x43
        cmd = [0x21, 0x41, 0x0]
        self.write(cmd)
        cmd = [0x21, 0x42, 0x0]
        self.write(cmd)

    def select(self, channel):
        """expects 1-4
           Silver PPSO BOX:
           has 2 ground inputs lower row with 4 pins
           has 2 data input upper with 4 pins
               A0 A1
           Q1 : 0 0
           Q2 : 0 1
           Q3 : 1 0
           Q4 : 1 1

           connection to USB chip select card
           PORT A : GDN + 1 -> GND -> A0
           PORT B : GND + 1 -> GND -> A1
        """
        self.configure_as_output()
        # sets all to zero
        # move wheel to Q4 and plugged in the cables on the MUX
        if channel == 1:
            cmd = [0x48, 0x00]
            self.write(cmd)
            import time
            time.sleep(0.5)
            cmd = [0x4C, 0x00]
            self.write(cmd)
        elif channel == 2:
            cmd = [0x41, 0x01]
            self.write(cmd)
            cmd = [0x42, 0x00]
            self.write(cmd)
        elif channel == 3:
            cmd = [0x41, 0x00]
            self.write(cmd)
            cmd = [0x42, 0x01]
            self.write(cmd)
        elif channel == 4:
            cmd = [0x41, 0x01]
            self.write(cmd)
            cmd = [0x42, 0x01]
            self.write(cmd)
        else:
            print "ERROR wrong input"
        self.__close_ser()

################################################################
def main():
    """expects 1 parameter:
            mode: [1-4]
            """
    show_help = False
    if len(sys.argv) == 2:
        if sys.argv[1].startswith("/dev/tty"):
            serial_port = sys.argv[1]
        else:
            show_help = True
        #select = sys.argv[2]
    elif len(sys.argv) == 1:
        #select = sys.argv[1]
        serial_port = "/dev/ttyUSB1"

    if show_help:
        print "Set or Read Port"
        print "usage:"
        print "python %s [<serial_port>] <mode>" % sys.argv[0]
        print "where serial_port is /dev/ttyUSB1 if not set"
        print "where mode is:"
        print "    1"
        print "    2"
        print "    3"
        print "    4"
    else:
        mux = MuxPpsOut(serial_port)
        #mux.select(int(select))
        mux.select(1)

if __name__ == "__main__":
    main()
