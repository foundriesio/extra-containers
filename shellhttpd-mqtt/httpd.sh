#!/bin/sh
PORT="${PORT-8082}"
ACCESS=1
while true; do
	RESPONSE="HTTP/1.1 200 OK\r\n\r\nNumber of Access = ${ACCESS}\r\n"
	echo -en "$RESPONSE" | nc -l -p "${PORT}" > ./tmp.log || true
	if grep -q "GET / HTTP/1.1" ./tmp.log; then
		echo "Number of Access = $ACCESS"
		mosquitto_pub -h host.docker.internal -t "containers/requests" -m "ACCESS=$ACCESS"
		ACCESS=$((ACCESS+1))
		echo "----------------------"
	fi
done