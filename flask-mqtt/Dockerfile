# flask-mqtt/Dockerfile
FROM alpine

RUN apk add --update py-pip
RUN apk --no-cache add py3-flask
# install python3 dependencies in advance -- we can copy them later
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache --upgrade Flask-MQTT

ENV FLASK_APP=app.py
ENV PYTHONPATH=/srv
COPY ./app.py /srv/app.py
CMD ["python3", "-m", "flask", "run", "-h", "0.0.0.0"]