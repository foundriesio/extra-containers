FROM golang:alpine

RUN apk add --no-cache git gcc musl-dev \
	&& go get github.com/apache/mynewt-mcumgr-cli/mcumgr

FROM alpine:latest
COPY --from=0 /go/bin/mcumgr /usr/bin/
ENTRYPOINT ["mcumgr"]
