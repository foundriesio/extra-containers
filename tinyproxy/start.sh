#!/bin/sh

# Make sure the writable pieces are created and available before running the service
mkdir -p /var/run/tinyproxy
mkdir -p /var/log/tinyproxy
touch /var/log/tinyproxy/tinyproxy.log
chown -R tinyproxy:tinyproxy /var/log/tinyproxy /var/run/tinyproxy

# Force dump of tinyproxy.log to stdout
tail -f /var/log/tinyproxy/tinyproxy.log &

# Execute all the rest
exec "$@"
