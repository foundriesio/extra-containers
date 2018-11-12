FROM alpine

RUN apk --no-cache add openssl python3 py3-pip \
	&& apk --no-cache add python3-dev openssl-dev libffi-dev musl-dev gcc \
	&& pip3 install --upgrade pip \
	&& pip3 install requests asyncssh \
	&& apk del python3-dev openssl-dev libffi-dev musl-dev gcc
