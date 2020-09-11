#!/bin/sh
FILE_CUSTOM=/mosquitto/secrets/mosquitto.conf
FILE_DEFAULT=/mosquitto/config/mosquitto.conf
m2=empety
while true; do
	sleep 5
	m1=$(md5sum $FILE_CUSTOM 2>/dev/null)
	if [ -z "$m1" ]
	then
        if [ "$m1" != "$m2" ] ; 
		then
			echo "Running Default config"
			m2=$m1
			killall mosquitto
			sleep 1
			/usr/sbin/mosquitto -c $FILE_DEFAULT &
		fi
	else
		if [ "$m1" != "$m2" ] ;
		then
			echo "Running Custom config"
			m2=$m1
			killall mosquitto
			sleep 1
			/usr/sbin/mosquitto -c $FILE_CUSTOM &
		fi
	fi
done
