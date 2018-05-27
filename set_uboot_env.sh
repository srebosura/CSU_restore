#!/bin/bash 

# Adjust to suit setup
SERIALDEV=ttyUSB0
TMPDIR=/dev/shm

TOOLPATH=`dirname ${0}`
ETHADDR=""
ETH1ADDR=""

function printhelp() {
	echo "Usage:"
	echo "  `basename $0` [-h] [-p <serial port>] <u-boot config>"
	echo ""
	echo "Options:"
	echo "  -h                Print this help text"
	echo "  -p <serial port>  Set serial port (default: ${SERIALDEV})"
	echo "  -m <mac addr>     Set MAC address for primary interface"
	echo "  -s <macc addr 2>  Set MAC address for secondary interface (RFM gigabit)"
	echo "  <u-boot config>   Path to u-boot environment config file"
}

# Get command line options
while getopts ":p:m:s:h" Option
do
	case ${Option} in
		p ) SERIALDEV=${OPTARG};;
		m ) ETHADDR=${OPTARG};;
		s ) ETH1ADDR=${OPTARG};;
		h ) printhelp
		    exit 0;;
		* ) echo "Unimplemented option! Run `basename ${0}` -h to see available options."
		    exit 1;;
	esac
done

shift $(($OPTIND - 1))
UBOOTCONF=${1} 
MINICOM="minicom -o -D /dev/${SERIALDEV} -b 115200"

has_minicom=0
which minicom 2>&1 > /dev/null && has_minicom=1

if [ ${has_minicom} -eq 0 ]; then
	echo "Minicom is required to run this script"
	exit 1
fi

if [ -z ${UBOOTCONF} ]; then
	echo "U-boot configuration file path not specified! Run `basename ${0}` -h to see available options."
	exit 1
fi

if [ ! -f ${UBOOTCONF} ]; then
	echo "U-boot configuration file not found!"
	exit 1
fi

SCRFILE=${TMPDIR}/uboot_env.runscript
SCRFILE2=${TMPDIR}/env_save.runscript

# Generate script-file
echo "print \"\n** Setting environment variables **\n\"" > ${SCRFILE}
echo "send \" \n\"" >> ${SCRFILE}
printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}

echo "eth0:${ETHADDR}"
if [ -n "${ETHADDR}" ]; then
	echo "send \"setenv ethaddr ${ETHADDR}\n\"" >> ${SCRFILE}
	printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}
fi

echo "eth1:${ETH1ADDR}"
if [ -n "${ETH1ADDR}" ]; then
	echo "send \"setenv eth1addr ${ETH1ADDR}\n\"" >> ${SCRFILE}
	printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}
fi

exec < ${UBOOTCONF}
while read line; do
	chk=`echo "${line}" |grep -v "^#"`
	if [ -n "${chk}" ]; then
		length=`echo "${line}" |wc -c`
		if [ ${length} -gt 80 ]; then
			line2=`echo "${line}" |cut -c 1-80`
			line=`echo "${line}" |cut -c 81-${length}`
			echo "send \"${line2}\c\"" >> ${SCRFILE}
		fi
		echo "send \"${line}\n\"" >> ${SCRFILE}
		printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}
	fi
done

echo "print \"\n** Done. Current settings: ** \n\"" >> ${SCRFILE}
echo "send \" \n\"" >> ${SCRFILE}
printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}
echo "send \"printenv\n\"" >> ${SCRFILE}
printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE}
echo "sleep 1" >> ${SCRFILE}
echo "! killall -9 minicom" >> ${SCRFILE}

# Run minicom
${MINICOM} -S ${SCRFILE}

# Save environment settings to flash
echo ""
echo ""
echo "Saving settings ...... "
sleep 2
#echo -n "Save settings y/n ? "
#read answer <&1

#if [ ${answer} == "y" ];#then

	echo "print \"\n** Saving environment variables **\n\"" > ${SCRFILE2}
	echo "send \" \n\"" >> ${SCRFILE2}
	printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE2}
	echo "send \"saveenv\n\"" >> ${SCRFILE2}
	printf "%s\n%s\n%s\n" "expect {" " \"U-Boot > \"" "}" >> ${SCRFILE2}
	echo "sleep 1" >> ${SCRFILE2}
	echo "! killall -9 minicom" >> ${SCRFILE2}
	${MINICOM} -S ${SCRFILE2}
#fi

exit 0
