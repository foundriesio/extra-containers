FROM debian:stretch

# Fluent Bit version
ENV FLB_MAJOR 1
ENV FLB_MINOR 0
ENV FLB_PATCH 6
ENV FLB_VERSION 1.0.6

ENV DEBIAN_FRONTEND noninteractive

ENV FLB_TARBALL http://github.com/fluent/fluent-bit/archive/v$FLB_VERSION.zip

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      make \
      wget \
      unzip \
      libssl1.0-dev \
      libasl-dev \
      libsasl2-dev \
      pkg-config \
      libsystemd-dev \
      zlib1g-dev \
      ca-certificates \
    && wget -O "/tmp/fluent-bit-${FLB_VERSION}.zip" ${FLB_TARBALL} \
    && cd /tmp && unzip "fluent-bit-$FLB_VERSION.zip" && rm /tmp/fluent-bit-${FLB_VERSION}.zip  \
    && cd "fluent-bit-$FLB_VERSION"/build/ \
    && rm -rf /tmp/fluent-bit-$FLB_VERSION/build/* \
    && cmake -DFLB_DEBUG=On \
          -DFLB_TRACE=Off \
          -DFLB_JEMALLOC=On \
          -DFLB_TLS=On \
          -DFLB_SHARED_LIB=Off \
          -DFLB_EXAMPLES=Off \
          -DFLB_HTTP_SERVER=On \
          -DFLB_IN_SYSTEMD=On \
          -DFLB_OUT_KAFKA=On .. \
    && make -j $(getconf _NPROCESSORS_ONLN) install \
    && rm -rf /tmp/fluent-bit-$FLB_VERSION

EXPOSE 2020
CMD ["/usr/local/bin/fluent-bit", "-c", "/etc/fluent-bit.conf"]
