FROM alpine:latest

RUN apk add --no-cache adwaita-icon-theme mesa-dri-swrast midori ttf-ubuntu-font-family xorg-server xinit \
	&& uname -a | grep x86 || apk add --no-cache mesa-dri-vc4 \
	&& wget http://dl-cdn.alpinelinux.org/alpine/edge/testing/aarch64/ttf-font-awesome-4.7.0-r1.apk \
	&& apk add --allow-untrusted ttf-font-awesome-4.7.0-r1.apk \
	&& rm ttf-font-awesome-4.7.0-r1.apk

COPY xorg.conf /etc/X11/xorg.conf

CMD ["/usr/bin/startx", "/usr/bin/midori", "https://foundries.io"]
