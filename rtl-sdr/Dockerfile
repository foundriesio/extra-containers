FROM alpine:latest
EXPOSE 1234

RUN apk add --no-cache alpine-sdk cmake git libusb-dev libusb
RUN mkdir /tmp/src \
    && cd /tmp/src \
    && git clone git://git.osmocom.org/rtl-sdr.git \
    && mkdir /tmp/src/rtl-sdr/build \
    && cd /tmp/src/rtl-sdr/build \
    && cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local \
    && make \
    && make install


FROM alpine:latest
RUN apk add --no-cache libusb \
    && echo 'blacklist dvb_usb_rtl28xxu' > /etc/modprobe.d/raspi-blacklist.conf

COPY --from=0 /usr/local/bin/rtl_* /usr/local/bin/
COPY --from=0 /usr/local/lib/librtl* /usr/local/lib/
COPY test.sh /test.sh
