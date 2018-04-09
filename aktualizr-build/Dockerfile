FROM opensourcefoundries/minideb:stretch
ENV DEBIAN_FRONTEND noninteractive
ENV AKTUALIZR_SRCREV 46c8da6ceff826f697b122699f28dec7de3f9d2a
WORKDIR /root/
RUN install_packages \
		asn1c \
		bash \
		build-essential \
		bzip2 \
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
		libcurl3 \
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
		lshw \
		openjdk-8-jre \
		ostree \
		pkg-config \
		python3-dev \
		python3-gi \
		python3-openssl \
		python3-venv \
		unzip

RUN mkdir /build && cd /build \
		&& git clone https://github.com/advancedtelematic/aktualizr.git \
		&& cd aktualizr \
		&& git checkout $AKTUALIZR_SRCREV \
		&& git submodule update --init --recursive \
		&& mkdir build-git \
		&& cd build-git \
		&& cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_SOTA_TOOLS=ON -DBUILD_SYSTEMD=OFF -DBUILD_DEB=ON .. \
		&& make -j`getconf _NPROCESSORS_ONLN` \
		&& make package \
		&& cp *.deb /root/ \
		&& cd /root \
		&& rm -rf /build

CMD bash
