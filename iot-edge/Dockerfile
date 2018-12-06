FROM alpine:latest

ARG DEV_PKGS="gcc libffi-dev musl-dev openssl-dev python-dev"

RUN apk --no-cache add bash file openssl python py-pip $DEV_PKGS \
	&& pip install -U pip setuptools wheel \
	&& pip install idna==2.7 azure-iot-edge-runtime-ctl \
	&& apk del $DEV_PKGS

COPY run.sh /run.sh

CMD ["/run.sh"]
