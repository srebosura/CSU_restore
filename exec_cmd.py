#!/usr/bin/env python
##bug fixes by Sam 16.05.18
"""
 this file implements the serial communication to the Node
 logging will be done relative to file, in logfiles - one per day
"""

import serial
import sys, os
import logging
import re
import time
import signal

VERBOSE = False

RUNNING = True

STS = time.gmtime()

def alarm_handler_exit(signum, frame):
    global RUNNING
    """ in case of alarm we will exit the program """
    logging.error("timeout for command")
    print 'ERROR:', signum
    RUNNING = False
#    os._exit(1)

################################################################

class ExecCmd(object):
    """the exec2 class supports reraise or exit on exceptions
       on serial interface exceptions it will try again - once
       the default timeout is 5 seconds
       read is done blocking, write not
    """
    def __init__(self, port="/dev/ttyUSB0", reraise=True):
        """ installs the alarm handler """
        self.port = port
        self.ser = None
        self.output = "" # string for output of command
        self.timeout = 5 # default timeout
        signal.signal(signal.SIGALRM, alarm_handler_exit)
        self.reraise = reraise
        self.cmd = ""

    def raise_again(self):
        """re raise or exit"""
        if self.reraise:
            raise
        else:
            sys.exit(1)

    def __open_ser(self, try_again = True):
        """ open serial port, try again if port is not available"""
        try:
            if 0 == self.port.find("/dev/tty"):
                self.ser = serial.Serial(self.port, 115200)
                self.ser.open()
            else:
                self.ser = sys.stdout
            try_again = False
        except:
            err_msg = "IO Error on opening port " + self.port
            logging.error(err_msg)
            if not try_again:
                print 'ERROR: ', err_msg
                self.raise_again()

        if try_again:
            time.sleep(1)
            self.__open_ser(try_again = False)

    def __write_ser(self, cmd, try_again=True):
        """ handle EAGAIN on ser.write"""
        got_EAGAIN = False
        try:
            self.ser.write(cmd)
        except OSError, v:
            print "ERROR  in __write_ser"
            print v
            print type(v)
            # FIXME: Fix code below (no errno defined) -- sga
            #if v.errno == errno.EAGAIN:
                #got_EAGAIN = True
            if not try_again:
                # FIXME: Fix line below -- sga
                #print 'ERROR: ', err_msg
                print "ERROR"
                self.raise_again()

        if try_again and got_EAGAIN:
            time.sleep(0.5)
            self.__open_ser(try_again = False)
            time.sleep(0.5)
            self.__write_ser(cmd, False)

    def __write_command(self, cmd):
        """ writes the command to the serial port 
            installs an alarm handler to implement timeout"
        """
        self.__open_ser()

        # write the command
        try:
            self.ser.flushInput()
            # set console marker to "dir >"
            self.__write_ser("PS1=\"\w >\";")
            self.__write_ser(cmd + "\r\n")
            #self.__write_ser("\r\n")
            self.ser.flushOutput()
            self.ser.flush()
        except:
            err_msg = "IO Error on writing " + self.port
            logging.error(err_msg)
            print 'ERROR: ', err_msg
            self.raise_again()
        self.cmd = cmd # just for logging

    def set_timeout(self, timeout):
        """will take care that default timeout 
           it is used if nothing set"""
        if timeout:
            try:
                timeout = int(timeout)
            except:
                err_msg = "timeout must be interger"
                logging.error(err_msg)
                print "ERROR: ", err_msg
                self.raise_again()
            if timeout != -1:
                self.timeout = timeout
        else:
            # use default self.timeout
            pass

    def __read_output_blocking(self):
        global RUNNING
        """
        will read from serial port char by char, blocking
        on received \n output buffer will be printed to stdout
        does this until PS1 is received - indicating the command is completed
        and we are back on shell
        - reopens the serial port in case of serialException
        """
        sys.stdout.flush()
        self.output = ""
        data = None
        while RUNNING:
            # will timeout in cases it is not succesful
            try:
                data = self.ser.read(1)
                try_again = False
            except:
                # we do not have a timeout on the serial port
                # - serial returns just two exceptions
                err_msg = "IO Error on reading (1/2)" + self.port
                logging.info(self.cmd)
                logging.error(err_msg)
                logging.info(self.output)
                try_again = True
            # tries to fix errno 11 - port not available
            # it this happens we could check if 
            # there are other users of the port
            if try_again and RUNNING:
                time.sleep(1)
                self.__open_ser(try_again = False)
                time.sleep(1)
                try:
                    data = self.ser.read(1)
                except serial.SerialException:
                    err_msg = "IO Error on reading (2)" + self.port
                    logging.error(err_msg)
                    print 'ERROR: ', err_msg
                    self.raise_again()

            # save into output buffer
            if data:
                self.output += data

            # pring this buffer line by line
            if data == '\n':
                sys.stdout.write(self.output)
                sys.stdout.flush()

                # redo: until new line is matched (PS1)
                if re.match("^[/~].*>", self.output) or \
                    re.match("^root@.*[/~].*#", self.output):
                    break
                self.output = ""
        # done
        sys.stdout.flush()
        # return RUNNING (global)

    def exec_string(self, cmd, timeout = None):
        """ excepts string input """
        global RUNNING
        # take care of timeout,
        # direct calls of this function allow for no specified timeout 
        # which sets the implicit 5 seconds
        self.set_timeout(timeout)
        # setup alarm handler for timeout
        if timeout > 0:
            # if no timeout is given we want to have none
            if VERBOSE:
                print ("set alarm to %d : %s") % (self.timeout, cmd)
            signal.alarm(self.timeout)
        RUNNING = True
        try:
            self.__write_command(cmd)
        except:
            if RUNNING:
                print "Exception in exec_cmd.py.__write_command()"
            else:
                # no further output in case of timeout
                pass

        try:
            if timeout != -1:
                self.__read_output_blocking()
        except:
            if RUNNING:
                print "Exception in exec_cmd.py.__read_output_blocking()"
            else:
                # no further output in case of timeout
                pass

        if not RUNNING:
            # we also send in case of timeout -1 e.g. reboot
            #we had a timeout - lets try to stop the program on the Node
            # send ctrl-C two times then ctrl-D
            self.__write_ser('\x03')
            self.__write_ser("\r\n")
            self.__write_ser('\x03')
            self.__write_ser("\r\n")
            self.__write_ser('\x04')
            self.__write_ser("\r\n")
            self.ser.flush()
        self.ser.close()
        # disable the alarm
        if timeout > 0:
            if VERBOSE:
                print ("clear alarm")
            signal.alarm(0)

    def get_output(self):
        return self.output

#########################################################################



def main():
    """ this function supports a variable number of parameters 
        - commming in via sys.argv
        the last parameter must be integer and will be used as timeout
            
        valid usages:
           python exec_cmd.py <serial_port> "ls /data \| grep D" 5
           python exec_cmd.py <serial_port> ls /data \| grep D 5

           if first argument matches /dev/tty then it will be taken as serial port
           if not it takes the configured one
    """

    logfile = "/home/obs/sam/rootfs/tools/logfiles/%s%s%s.%s.log" % \
                (STS.tm_year, STS.tm_mon, STS.tm_mday, os.path.basename(sys.argv[0]))
    try:
        logging.basicConfig(
                filename=logfile,
                level=logging.DEBUG,
                format="%(levelname)-8s - %(asctime)s - %(message)s",
                )
    except IOError:
        print "Error please create %s directory" % logfile
        sys.exit(1)

    # which serial port
    serial_port = "FAKE" # will write til stdout
    serial_port = "/dev/ttyUSB0"

    # log input values
    logging.info(sys.argv)
    
    # which command
    #    all but last argument will be concatinated, this is the command
    cmd = ""
    if sys.argv[1].startswith("/dev/tty"):
        serial_port = sys.argv[1]
        start = 2
    else:
        start = 1

    # log input
    for arg in range(start, len(sys.argv)-1):
        if cmd != "":
            cmd += " "
        cmd += sys.argv[arg]

    # last argument is timeout
    try:
        timeout = int(sys.argv[len(sys.argv) - 1])
    except:
        err_msg = 'timeout (int) must be last parameter'
        logging.error(err_msg)
        print "ERROR: ", err_msg
        sys.exit(1)

    # open the serial port
    ecmd = ExecCmd(serial_port, False)
    # execute the command
    ecmd.exec_string(cmd, timeout)
    return (0)

if __name__ == "__main__":
    sys.exit(main())
