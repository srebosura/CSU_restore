#!/bin/bash 

# Adjust to suit setup
SERIALDEV=ttyUSB0


TOOLPATH=`dirname ${0}`

function printhelp() {
	echo "Usage:"
	echo "  `basename $0` [-h] [-p <serial port>] <u-boot binary>"
	echo ""
	echo "Options:"
	echo "  -h                Print this help text"
	echo "  -p <serial port>  Set serial port (default: ${SERIALDEV})"
	echo "  <u-boot binary>   Path to u-boot image"
}

# Get command line options
while getopts ":p:h" Option
do
	case ${Option} in
		p ) SERIALDEV=${OPTARG};;
		h ) printhelp
		    exit 0;;
		* ) echo "Unimplemented option! Run `basename ${0}` -h to see available options."
		    exit 1;;
	esac
done

shift $(($OPTIND - 1))
UBOOTIMG=${1}

has_mono=0
which mono 2>&1 > /dev/null && has_mono=1

if [ ${has_mono} -eq 0 ]; then
	echo "Mono is required to run this script"
	exit 1
fi

if [ -z ${UBOOTIMG} ]; then
	echo "u-boot image path not specified! Run `basename ${0}` -h to see available options."
	exit 1
fi

if [ ! -f ${UBOOTIMG} ]; then
	echo "Image file not found!"
	exit 1
fi

mono ${TOOLPATH}/sfh_OMAP-L138.exe -p /dev/${SERIALDEV} -v -flash_noubl \
	-targetType OMAPL138 -flashType NAND ${UBOOTIMG}

exit 0
