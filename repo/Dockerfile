FROM alpine:latest

RUN apk add --no-cache git curl python \
	&& curl https://storage.googleapis.com/git-repo-downloads/repo > /bin/repo \
	&& chmod a+x /bin/repo

WORKDIR /src
ENTRYPOINT ["/bin/repo"]
