FROM opensourcefoundries/minideb:stretch as builder
ENV DEBIAN_FRONTEND noninteractive
ENV AKTUALIZR_SRCREV 930d8eef6eb584686654601c056d7c9c6fca3048
WORKDIR /build/
RUN install_packages \
		asn1c \
		bash \
		build-essential \
		cmake \
		curl \
		git \
		libarchive-dev \
		libboost-dev \
		libboost-log-dev \
		libboost-program-options-dev \
		libboost-random-dev \
		libboost-regex-dev \
		libboost-system-dev \
		libboost-test-dev \
		libboost-thread-dev \
		libcurl4-openssl-dev \
		libdpkg-dev \
		libengine-pkcs11-openssl \
		libexpat1-dev \
		libglib2.0-dev \
		libgpgme11-dev \
		liblzma-dev \
		libsodium-dev \
		libsqlite3-dev \
		libssl-dev \
		libtool \
		pkg-config \
		python3-dev \
		python3-gi \
		python3-openssl \
		python3-venv \
		wget
COPY extra_packaging.patch .
RUN git clone https://github.com/advancedtelematic/aktualizr.git \
		&& cd aktualizr \
		&& git checkout $AKTUALIZR_SRCREV \
		&& git submodule update --init --recursive \
		&& patch -p1 <../extra_packaging.patch \
		&& mkdir build-git \
		&& cd build-git \
		&& cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_SOTA_TOOLS=ON -DBUILD_SYSTEMD=OFF -DBUILD_DEB=ON .. \
		&& make -j`getconf _NPROCESSORS_ONLN` \
		&& make package \
		&& cp -v *.deb /build/

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
COPY --from=builder /build/*.deb /root/
RUN dpkg -i *.deb
CMD bash
