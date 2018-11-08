FROM alpine:latest

RUN apk add --no-cache git gcc musl-dev go \
	&& go get -v github.com/apache/mynewt-mcumgr-cli/mcumgr

FROM alpine:latest
COPY --from=0 /root/go/bin/mcumgr /usr/bin/
ENTRYPOINT ["mcumgr"]
