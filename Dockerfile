FROM python:3.7-alpine3.16

ENV TZ=Europe/Moscow
#ENV SSL_CERT_DIR=/etc/ssl/certs
WORKDIR /usr/src/app

#USER root

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.16/community' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.16/main' >> /etc/apk/repositories

#RUN apk update \
#    && apk upgrade \
RUN apk add --no-cache --update \
	ca-certificates \
	curl \
	build-base \
	libffi-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt ./
RUN  pip install --no-cache-dir -r requirements.txt 

COPY ./*.py .

CMD [ "python", "./google_docs.py" ]
