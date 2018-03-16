FROM opensourcefoundries/minideb:stretch

RUN install_packages build-essential python-pip python-dev libffi-dev libssl-dev

RUN pip install setuptools wheel
RUN pip install -U azure-iot-edge-runtime-ctl

RUN apt-get remove -y --purge --auto-remove build-essential
COPY run.sh /

CMD ["/run.sh"]
