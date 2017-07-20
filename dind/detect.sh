#!/bin/bash

set -x

ARCH=$(arch)

echo $ARCH

rm /etc/apt/sources.list

case ${ARCH} in 
x86_64|amd64)
	echo "deb http://archive.ubuntu.com/ubuntu/ zesty main universe" >> /etc/apt/sources.list;
	echo "deb http://archive.ubuntu.com/ubuntu/ zesty-updates main universe" >> /etc/apt/sources.list;
	echo "deb http://archive.ubuntu.com/ubuntu/ zesty-security main universe" >> /etc/apt/sources.list;
	wget --no-check-certificate https://github.com/estesp/manifest-tool/releases/download/v0.6.0/manifest-tool-linux-amd64;
        mv manifest-tool-linux-amd64 /bin/manifest-tool;
	chmod a+x /bin/manifest-tool;
	;;
*)
	echo "deb http://ports.ubuntu.com/ zesty main universe" >> /etc/apt/sources.list;
	echo "deb http://ports.ubuntu.com/ zesty-updates main universe" >> /etc/apt/sources.list;
	echo "deb http://ports.ubuntu.com/ zesty-security main universe" >> /etc/apt/sources.list;
        wget --no-check-certificate https://github.com/estesp/manifest-tool/releases/download/v0.6.0/manifest-tool-linux-arm;
        mv manifest-tool-linux-arm /bin/manifest-tool;
        chmod a+x /bin/manifest-tool;
	;;
esac

cat /etc/apt/sources.list
