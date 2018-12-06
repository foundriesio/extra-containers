FROM alpine:latest

RUN apk --no-cache add ca-certificates wget tar nginx \
 && wget -O freeboard.tar.gz https://api.github.com/repos/Freeboard/freeboard/tarball/master \
 && mkdir -p /usr/share/nginx/html/plugins/mqtt \
 && mkdir -p /usr/share/nginx/html/plugins/thirdparty \
 && mkdir /run/nginx \
 && tar -xzvf freeboard.tar.gz -C /usr/share/nginx/html --strip-components=1 \
 && rm freeboard.tar.gz

COPY test.sh /test.sh
COPY default.conf /etc/nginx/conf.d/default.conf
COPY paho.mqtt.plugin.js /usr/share/nginx/html/plugins/thirdparty/
COPY mqttws31.js /usr/share/nginx/html/plugins/mqtt/
COPY index.html /usr/share/nginx/html/
COPY dashboard.json /usr/share/nginx/html/

STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]
