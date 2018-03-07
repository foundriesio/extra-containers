#!/bin/sh -e

docker run --privileged -d --name jobserv-worker \
	--restart unless-stopped \
	-v /proc/sysrq-trigger:/sysrq \
	registry.foundries.io/development/microplatforms/linux/extra-containers/jobserv-worker
