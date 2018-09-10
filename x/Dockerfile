FROM foundriesio/minideb:stretch

RUN install_packages \
  sudo \
  xorg \
  chromium \
  lightdm

COPY start.sh /usr/bin/start.sh
COPY xorg.conf /etc/X11/xorg.conf

ENTRYPOINT ["/usr/bin/start.sh"]
