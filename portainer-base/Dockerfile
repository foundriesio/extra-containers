# Simple dockerfile for portainer-base
FROM opensourcefoundries/alpine:edge as base
RUN apk --no-cache --update upgrade && apk --no-cache add ca-certificates

FROM scratch
COPY --from=base /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
