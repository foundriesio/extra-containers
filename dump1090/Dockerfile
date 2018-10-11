FROM alpine:latest

RUN apk add --no-cache alpine-sdk cmake git libusb-dev lighttpd \
    && mkdir /tmp/src \
    && cd /tmp/src \
    && git clone git://git.osmocom.org/rtl-sdr.git \
    && mkdir /tmp/src/rtl-sdr/build \
    && cd /tmp/src/rtl-sdr/build \
    && cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local \
    && make \
    && make install \
    && cd /tmp/src \
    && git clone git://github.com/mutability/dump1090.git \
    && cd dump1090 \
    && git checkout ae6a7acb675d00f58d1d62b3e11c4be51ea94b70 \
    && make


FROM alpine:latest
RUN apk add --no-cache libusb \
    && echo 'blacklist dvb_usb_rtl28xxu' > /etc/modprobe.d/raspi-blacklist.conf

COPY --from=0 /tmp/src/dump1090/dump1090 /usr/bin/
COPY --from=0 /usr/local/lib/librtl* /usr/local/lib/

EXPOSE 8080 30001 30002 30003 30004 30005
ENTRYPOINT ["dump1090", "--interactive","--net","--metric"]
