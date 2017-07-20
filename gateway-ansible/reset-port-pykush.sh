#!/bin/bash
# $1 - ykush ID: YK23310  retrieve using pykush -l
# $2 - device id: {1,2,3}

flock /var/lock/lava-pykush.lck pykush -s $1 -d $2
while [ $? -ne 0 ]; do
	echo "Disable port failed, retrying..."
	flock /var/lock/lava-pykush.lck pykush -s $1 -d $2
done
sleep 5
flock /var/lock/lava-pykush.lck pykush -s $1 -u $2
while [ $? -ne 0 ]; do
	echo "Enable port failed, retrying..."
	flock /var/lock/lava-pykush.lck pykush -s $1 -u $2
done
sleep 20
