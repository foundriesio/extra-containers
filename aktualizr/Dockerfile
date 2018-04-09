FROM opensourcefoundries/minideb:stretch
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /root/
RUN install_packages \
		bash \
		bzip2 \
		libarchive13 \
		libcurl3 \
		libsodium18 \
		lshw \
		openjdk-8-jre \
		ostree \
		unzip
COPY ota-publish.sh /usr/bin/ota-publish
COPY *.deb /root/
RUN ARCH=`dpkg --print-architecture` \
		&& dpkg -i aktualizr_$ARCH.deb \
		&& dpkg -i garage_deploy_$ARCH.deb \
		&& rm -f *.deb
CMD bash
