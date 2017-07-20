FROM oneimage/ubuntu:zesty

COPY detect.sh /root/detect.sh

RUN chmod a+x /root/detect.sh && \
     sleep 1 && \
    /root/detect.sh

RUN apt-get clean && apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables \
    docker.io
    
# Install the magic wrapper.
ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

# Define additional metadata for our image.
VOLUME /var/lib/docker
CMD ["wrapdocker"]
