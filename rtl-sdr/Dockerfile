FROM linarotechnologies/alpine:edge
EXPOSE 1234

RUN apk add --no-cache alpine-sdk cmake git libusb-dev libusb 
RUN mkdir /tmp/src \
    && cd /tmp/src \
    && echo 'blacklist dvb_usb_rtl28xxu' > /etc/modprobe.d/raspi-blacklist.conf \
    && git clone git://git.osmocom.org/rtl-sdr.git 
RUN mkdir /tmp/src/rtl-sdr/build \
    && cd /tmp/src/rtl-sdr/build \
    && cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local \
    && make \
    && make install

RUN rm -r /tmp/src \
    && chmod +s /usr/local/bin/rtl_* 
    
