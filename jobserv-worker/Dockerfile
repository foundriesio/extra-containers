FROM docker:dind

COPY reboot.sh /usr/bin/reboot
COPY cold-reboot.sh /usr/bin/cold-reboot
COPY jobserv-worker-entry.sh /usr/local/bin/

RUN apk --no-cache add curl git python3 py3-requests

VOLUME /srv/jobserv-worker

ENTRYPOINT ["/usr/local/bin/jobserv-worker-entry.sh"]
CMD []
