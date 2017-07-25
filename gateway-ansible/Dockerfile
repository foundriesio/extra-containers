FROM linarotechnologies/alpine:edge

RUN apk add --no-cache openssh git vim ansible

CMD git clone https://github.com/linaro-technologies-dev/gateway-ansible \
    && ssh-keygen -P "" -f ~/.ssh/id_rsa \
    && cd gateway-ansible \
    && echo "Now run: " ; echo "    ssh-copy-id linaro@TARGET_IP_ADDRESS"; echo "    ./iot-gateway.sh gateway" \
    && busybox sh
