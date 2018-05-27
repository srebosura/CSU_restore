#!/usr/bin/env python

import serial
import struct
import sys
import argparse
import binascii

SHUFFLER_FLAGS = [
	"FLAG_SHUFFLER_RUNNING",
	"FLAG_SHUFFLER_ENABLED",
	"FLAG_SHUFFLER_STORING",
	"FLAG_SHUFFLER_NOT_INITIALIZED",
	"FLAG_SHUFFLER_ERROR_MAGIC",
	"FLAG_SHUFFLER_ERROR_CPUTIME",
	"FLAG_SHUFFLER_ERROR_CRC",
	"FLAG_SHUFFLER_ERROR_PACKAGE_DROP",
	"FLAG_SHUFFLER_ERROR_TIMEOUT",
	"FLAG_SHUFFLER_ERROR_FLAC_MALLOC",
	"FLAG_SHUFFLER_ERROR_FLAC_ENCODING",
	"FLAG_SHUFFLER_ERROR_NOT_IN_USE",
	"FLAG_SHUFFLER_ERROR_NOW",
	"FLAG_SHUFFLER_ERROR_PACKAGES_DROPPED_5",
	"FLAG_SHUFFLER_ERROR_PACKAGES_DROPPED_100",
	"FLAG_SHUFFLER_ERROR_PACKAGES_DROPPED_1000",
	"FLAG_SHUFFLER_ERROR_BLANK_PACKET_INSERTED",
	"FLAG_SHUFFLER_ERROR_EMPTY_PACKET",
	"FLAG_SHUFFLER_ERROR_SIB_REBOOT"
]

def shuffler_flag_to_value(flag):
	idx = SHUFFLER_FLAGS.index(flag)
	value = (1 << idx)
	return value

def bitmask_to_shuffler_flags(bitmask):
	retval = []
	for flag, flagval in [ (f, shuffler_flag_to_value(f)) for f in SHUFFLER_FLAGS ]:
		if flagval & bitmask:
			retval.append(flag)
	return retval

def open_interp(port):
        interp = serial.Serial(port=port,
                       baudrate=115200,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS, 
		       timeout=10)
        # interp.open()
        return interp


def print_dict(keys, dd):
	for idx, key in enumerate(keys,1):
		print "%20s:%20s" % (key, str(dd[key])),
		if (idx % 3) == 0:
			print ""
	print ""

def get_status(interp, verbose):
	interp.write("(s)")
	# Read past this:  '\nS STAT\n.\n\x96\xaa\x03\x00\xfb\xf3\n\x00'
	# ------------------------------^

	response = interp.read(10)

	if not response:
		raise Exception("Unable to read data from interp")

	if not "S STAT" in response:
		raise Exception("Did not get expected header, got %s" % "".join([ "%02x" % ord(c) for c in response]))

	# Read 
	#	5 ints (magic -> station_number)
	#	4 bytes (sensor0_gains)	 == 1 int
	#	2 shorts (sensor0_tilts) == 1 int
	# 	20 bytes of battery values
	response = interp.read(7*4)

	header = struct.unpack("<IIIIIBBBBHH", response[:7*4])
	header_keys = [ "magic", "uptime", "runtime", "disk_free", "station_number", "gain_x", "gain_y", "gain_z", "gain_p", "tilt_x", "tilt_y" ]
	header_dict = dict(zip(header_keys, header))

	# Read
	#	4 voltage shorts = 8
	#	4 current shorts = 8
	#	1 batsel byte
	#	3 padding bytes
	response = interp.read(20)
	battery = struct.unpack("<HHHHHHHHBxxx", response)
	battery_keys = ["vbat", "vbat1", "vbat2", "vacm", "imain", "ibat1", "ibat2", "iacm", "batsel" ]
	battery_dict = dict(zip(battery_keys, battery))

	# Read
	#	3 shorts	= 6
	#	1 int		= 4
	#	3 shorts	= 6
	#	2 longs		= 8
	response = interp.read(24)
	if verbose:
		print "binary data: %s" % binascii.b2a_hex(response)
	csac = struct.unpack("<HHHHHHILL", response)
	csac_keys = [ "status", "alarm", "laseri", "sig", "temp", "discok", "heatp", "tod", "ltime" ]
	csac_dict = dict(zip(csac_keys, csac))

	# Read
	#	1 shuffler flags int
	response = interp.read(4)
	shuffler_flag = struct.unpack("<I", response)[0]

	if verbose:
		print "header:"
		print_dict(header_keys, header_dict)

		print "battery:"
		print_dict(battery_keys, battery_dict)

		print "csac:"
		print_dict(csac_keys, csac_dict)

		print "shuffler_flag: 0x%04x" % shuffler_flag

	response = interp.read(3*4+1*2+4+2)

	response_vals = struct.unpack("<IIIHxxI", response)
	qc_keys = [ "qcd_bat_booted", "qcd_tilt_file", "qcd_retvals", "housing_number", "num_status" ]
	qc_dict = dict(zip(qc_keys, response_vals))

	if  verbose:
		print "QC:"
		print_dict(qc_keys, qc_dict)


	acc_proc_bytes = interp.read(9*4+8*8+8*4+2*2)

	# print "acc_proc_bytes: %s" % ("".join([ "%02x" % ord(c) for c in acc_proc_bytes]))

	try:
		acc_proc = struct.unpack("<iiiiiiiiiqqqqqqqqiiiiiiiiHH", acc_proc_bytes)
	except Exception, err:
		raise Exception("Failed unpacking acc_proc from %s (%d bytes): %s" % ("".join(["%02x" % ord(c) for c in acc_proc_bytes]), len(acc_proc_bytes), str(err)))
	acc_proc_keys = ['node','num_blocks_read','num_blocks_written','written_today','time','mean_0','mean_1','mean_2','mean_3', 'sum_0', 'sum_1', 'sum_2', 'sum_3', 'energy_0', 'energy_1', 'energy_2', 'energy_3', 'maxrms_0', 'maxrms_1', 'maxrms_2', 'maxrms_3', 'minrms_0', 'minrms_1', 'minrms_2', 'minrms_3', 'csac_status', 'crc']

	acc_proc_dict = dict(zip(acc_proc_keys, acc_proc))

	if verbose:
		print "acc_proc: " 
		print_dict(acc_proc_keys, acc_proc_dict)

	csac_status = acc_proc[-2]

	acc_proc_hour_bytes = interp.read(9*4+8*8+8*4+2*2)
	# print "acc_proc_hour_bytes: %s" % ("".join([ "%02x" % ord(c) for c in acc_proc_hour_bytes]))
	acc_proc_hour = struct.unpack("<iiiiiiiiiqqqqqqqqiiiiiiiiHH", acc_proc_hour_bytes)
	acc_proc_hour_dict = dict(zip(acc_proc_keys, acc_proc_hour))

	if verbose:
		print "acc_proc_hour: " 
		print_dict(acc_proc_keys, acc_proc_hour_dict)

	csac_status_hourly = acc_proc_hour[-2]

	crc_bytes = interp.read(2+2)
	crc = struct.unpack("<Hxx", crc_bytes)[0]

	if verbose:
		print "crc: %02x" % crc

	endbytes = ""
	endbyte = interp.read(1)
	while endbyte:
		endbytes += endbyte
		if endbytes.endswith("\nE STAT\n"):
			break
		endbyte = interp.read(1)
	if not endbytes.endswith("\nE STAT\n"):
		raise Exception("Could not find tail in response, tail has %s" % "".join([ "%02x" % ord(c) for c in endbytes[-10:]]))

	#print "end_bytes: %s" % ("".join([ "%02x" % ord(c) for c in endbytes ]))

	return shuffler_flag, csac_status, csac_status_hourly, qc_dict["qcd_retvals"]



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Interp Test Client")
	parser.add_argument("-v", "--verbose", help="Show all")
	parser.add_argument("-F", "--device", dest="port", default="/dev/ttyUSB0", help="Serial device to use")

	args = parser.parse_args()

	interp = open_interp(args.port)
	interp_status, csac_status, csac_status_hourly, qcd_status = get_status(interp, args.verbose)

	print "Interp Status = 0x%x (%s)" % (interp_status, " | ".join(bitmask_to_shuffler_flags(interp_status)))
	print "CSAC Status = 0x%x (last hour: 0x%x)" % (csac_status, csac_status_hourly)
	print "QCD Status = 0x%x (%s)" % (qcd_status, " | ".join(bitmask_to_shuffler_flags(qcd_status)))
	
