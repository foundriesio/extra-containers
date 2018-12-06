FROM alpine:latest

ARG DEV_PKGS="autoconf automake gcc git g++ libtool make musl-dev wget"

ARG RTL_VER=${VER:-master}
ARG RTL_REPO=https://github.com/dgiardini/rtl-ais.git
ARG RTL_APP=/usr/src/rtl

ARG FFTW_URL=http://fftw.org/fftw-3.3.8.tar.gz

ARG KAL_VER=arm_memory
ARG KAL_REPO=https://github.com/asdil12/kalibrate-rtl.git
ARG KAL_APP=/usr/src/kal-rtl

WORKDIR $RTL_APP

# libfftw3-dev
RUN apk add --no-cache bash libstdc++ $DEV_PKGS \
	&& apk --no-cache add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing librtlsdr librtlsdr-dev \
	&& echo Building rtl-ais \
	&& git clone -b $RTL_VER $RTL_REPO $RTL_APP \
	&& make \
	&& mv rtl_ais /usr/local/bin/ \
	&& echo Building fftw \
	&& wget -O /fftw.tgz $FFTW_URL \
	&& cd /usr/src \
	&& tar -xzf /fftw.tgz \
	&& rm /fftw.tgz \
	&& cd fftw* \
	&& ./configure \
	&& make \
	&& make install \
	&& echo Building kal-rtl \
	&& git clone -b $KAL_VER $KAL_REPO $KAL_APP \
	&& cd $KAL_APP \
	&& ./bootstrap \
	&& ./configure \
	&& make \
	&& make install \
	&& rm /usr/src/* -rf \
	&& apk del $DEV_PKGS

EXPOSE 10110/udp
CMD rtl_ais -n
