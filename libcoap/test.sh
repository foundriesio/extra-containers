#!/bin/sh -e

coap-server &
PID=$!
sleep 1
coap-client -m get coap://localhost/

kill $PID
