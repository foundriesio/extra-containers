FROM alpine:latest

ENV CALIFORNIUM_HOME=/opt/cf

# CoAP port
EXPOSE 5683

RUN set -x \
    && mkdir -p $CALIFORNIUM_HOME \
    && cd $CALIFORNIUM_HOME \
    && apk add --no-cache libressl curl openjdk8-jre-base \
    && curl -o cf-plugtest-server.jar https://hudson.eclipse.org/californium/job/1.1.x-nightly/lastSuccessfulBuild/artifact/cf-plugtest-server.jar

VOLUME "$CALIFORNIUM_HOME/data"

WORKDIR $CALIFORNIUM_HOME
ENTRYPOINT ["java","-jar","cf-plugtest-server.jar","-Xmx768m -Xmx768m -XX:MaxMetaspaceSize=250m -XX:MetaspaceSize=250m -Xss300K -XX:+UseG1GC -XX:+UseStringDeduplication -XX:+UseCompressedOops -XX:+HeapDumpOnOutOfMemoryError"]
