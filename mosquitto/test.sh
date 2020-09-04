#!/bin/sh -ex

mosquitto &
PID=$!
sleep 1

netstat -ln | grep 1883

kill $PID
