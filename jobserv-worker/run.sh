#!/bin/sh -e

docker run --privileged -d --name jobserv-worker \
	--restart unless-stopped \
	-v /proc/sysrq-trigger:/sysrq \
	jobserv-worker
