# JobServ Worker

A container for running a JobServ worker.

## Usage

The container needs special privileges to run. The following snippet will run
the container properly:
~~~
  docker run --privileged -d --name jobserv-worker \
        --restart unless-stopped \
        -v /proc/sysrq-trigger:/sysrq \
        jobserv-worker
~~~

The worker must perform a one-time registration with the server. This can be
done by executing a command:
~~~
  docker exec -e USER=root jobserv-worker \
      /srv/jobserv-worker/jobserv_worker.py \
          --hostname <name you called it in OTA-CE>
	  https://api.foundries.io \
          raspberrypi3-64-ota
~~~
