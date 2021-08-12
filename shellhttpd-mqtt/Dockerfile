# shellhttpd-mqtt/Dockerfile
FROM alpine

RUN apk add --no-cache mosquitto-clients vim

COPY httpd.sh /usr/local/bin/

CMD ["/usr/local/bin/httpd.sh"]