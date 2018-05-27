#!/bin/sh

usage() {
	echo "Usage: $0 [-n|-u] INFILE OUTFILE" 1>&2;
	echo "	-u	Create image for UART boot" 1>&2;
	echo "	-n	Create image for NAND boot" 1>&2;
	echo "-n is default" 1>&2;
}

die() {
	echo "$@" 1>&2;
	exit 1;
}

IMAGE_TYPE="NAND"

while true; do
	case $1 in
		-u)
			;;
		-n)
			IMAGE_TYPE="UART"
			;;
		-?)
			help
			die
			;;
		*)
			break;
	esac
	shift
done

if [ -z "$2" ]; then
	usage
	die
fi

INFILE="$1"
OUTFILE="`readlink -f $2`"
BASEDIR=`dirname $0`
BASEDIR=`readlink -f $BASEDIR`

WORKDIR=`mktemp -d`
INIFILE="$BASEDIR/OMAPL138_CASE_A3_${IMAGE_TYPE}.ini"

# Prepare workdir
cp $INFILE $WORKDIR/u-boot-omapl138-case_a3.bin || die "Unable to copy INFILE"

cd ${WORKDIR} || die "Cannot change to ${WORKDIR}"

mono $BASEDIR/HexAIS_OMAP-L138.exe -ini ${INIFILE} -o $OUTFILE || die "HexAIS_OMAP-L138 failed"

if [ -d "$WORKDIR" ]; then
	case $WORKDIR in
		/tmp/tmp.*)
			rm -rf ${WORKDIR}
			;;
		*)
			die "Something is wrong with ${WORKDIR}"
			;;
	esac
fi
