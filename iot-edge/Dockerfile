FROM opensourcefoundries/minideb:stretch

RUN install_packages python-pip

RUN pip install setuptools wheel
RUN pip install -U azure-iot-edge-runtime-ctl

COPY run.sh /run.sh

CMD ["/run.sh"]

