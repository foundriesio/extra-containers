FROM alpine:3.8

RUN apk add --no-cache python3 py3-pip

WORKDIR /src

COPY candy_app /src/candy_app

RUN pip3 install -r /src/candy_app/requirements.txt

ENTRYPOINT ["flask", "-a", "candy_app", "dev"]
