
FROM python:3.7-alpine


RUN set -ex \
	&& apk add --no-cache tar libsodium-dev openssl 

WORKDIR /home

COPY script ./script
COPY shadowsocksr-3.2.2.tar.gz .

RUN tar zxf shadowsocksr-3.2.2.tar.gz \
	&& mv shadowsocksr-3.2.2/shadowsocks . \
	&& rm -f shadowsocksr-3.2.2.tar.gz

COPY config_sample.json config.json

#CMD [ "/usr/local/shadowsocks/server.py", "-c", "/etc/shadowsocks-r/config.json" ]
CMD [ "/home/shadowsocks/server.py", "-c", "/home/config.json" ]