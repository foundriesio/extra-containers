#!/bin/sh

if [ -z "${BLUEMIX_AUTHKEY}" ] ||
   [ -z "${BLUEMIX_AUTHTOKEN}" ] ||
   [ -z "${BLUEMIX_ORG}" ] ||
   [ -z "${GW_DEVICE_TYPE}" ]; then
    echo "Expected environment variables not found, aborting (see README.md)"
    exit 1
fi

/usr/bin/mosquitto-conf -ak "${BLUEMIX_AUTHKEY}" -at "${BLUEMIX_AUTHTOKEN}" -bo "${BLUEMIX_ORG}" -gdt "${GW_DEVICE_TYPE}"

service mosquitto start

# Execute all the rest
exec "$@"
