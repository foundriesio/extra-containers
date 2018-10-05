FROM alpine:latest
WORKDIR /root/

RUN apk add --no-cache git gcc make musl-dev linux-headers gd-dev gzip \
	&& git clone https://github.com/fsphil/fswebcam  \
	&& cd fswebcam \
	&&  ./configure --prefix=/usr \
	&& make

## Stage 2
FROM alpine:latest
WORKDIR /root/

RUN apk add --no-cache libgd
COPY --from=0 /root/fswebcam/fswebcam /usr/bin/
