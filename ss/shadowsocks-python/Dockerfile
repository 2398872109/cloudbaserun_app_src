FROM python:3.7-alpine

ENV WORKPATH=/home

ENV SERVER_PORT=9000
ENV PASSWORD=password
ENV METHOD=aes-256-cfb

COPY shadowsocks-master.zip ${WORKPATH}/

RUN set -ex \
    && apk add --no-cache unzip libsodium-dev openssl mbedtls \
    && cd ${WORKPATH} && unzip shadowsocks-master.zip \
    && cd shadowsocks-master && python setup.py install \
    && cd ${WORKPATH} && rm -fr shadowsocks-master.zip shadowsocks-master 

ADD script "${WORKPATH}/script"
ADD config.json "${WORKPATH}/config.json"

WORKDIR ${WORKPATH}

CMD [ "python","/home/script/config.py" ]