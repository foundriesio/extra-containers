#!/bin/sh -e

worker=$(cat /srv/jobserv-worker/settings.conf | grep hostname | cut -d= -f2 | tr -d '[:space:]')

sync

if [ "$worker" = "andy-rpi5" ] ; then
	exec curl -X PUT http://reckless:5000/1/reboot
fi
if [ "$worker" = "doanac-rpi3-64-2" ] ; then
	exec curl -X PUT http://reckless:5000/2/reboot
fi
if [ "$worker" = "doanac-x86-qemu-1" ] ; then
	exec curl -X PUT http://reckless:5001/doanac-x86-qemu-1/reboot
fi

echo "Unknown/support worker: $worker"
exit 1
