# derive from our baseimage
FROM opensourcefoundries/rtl-sdr:latest
 
WORKDIR /tmp
 
RUN apk add --no-cache alpine-sdk git lighttpd

RUN git clone git://github.com/mutability/dump1090.git \
    && cd dump1090 \ 
    && git checkout ae6a7acb675d00f58d1d62b3e11c4be51ea94b70 \
    && make
 
WORKDIR /tmp/dump1090

EXPOSE 8080 30001 30002 30003 30004 30005 

ENTRYPOINT ["./dump1090", "--interactive","--net","--metric"]
