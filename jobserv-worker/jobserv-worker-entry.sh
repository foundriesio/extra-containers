#!/bin/sh -e

WORKER_DIR=/srv/jobserv-worker
WORKER=${WORKER_DIR}/jobserv_worker.py

echo "Waiting for dockerd"
while ! docker ps ; do
	rm /var/run/docker* || true
	dockerd-entrypoint.sh &
	sleep 5s
done

if [ ! -f $WORKER ] ; then
	curl https://raw.githubusercontent.com/OpenSourceFoundries/jobserv/master/jobserv_worker.py > $WORKER
	chmod +x $WORKER
fi

while [ ! -f ${WORKER_DIR}/settings.conf ] ; do
	echo "Please register worker with a server. eg"
	echo " $WORKER register <host> <tags>"
	sleep 15s
done

exec $WORKER loop
