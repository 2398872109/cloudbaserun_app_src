FROM python:3.7-alpine

ENV WORKPATH=/home

ENV SERVER_PORT=9000
ENV PASSWORD=password
ENV METHOD=aes-256-cfb
ENV PROTOCOL=origin
ENV OBFS=plain


COPY shadowsocksr-3.2.2.tar.gz ${WORKPATH}/


RUN set -ex \
	&& apk add --no-cache tar libsodium-dev openssl \
	&& cd ${WORKPATH} \
	&& tar zxf shadowsocksr-3.2.2.tar.gz \
	&& mv shadowsocksr-3.2.2/shadowsocks . \
	&& rm -f shadowsocksr-3.2.2.tar.gz

ADD script "${WORKPATH}/script"
ADD config.json "${WORKPATH}/config.json"

WORKDIR /home

#CMD [ "/home/shadowsocks/server.py", "-c", "/home/config.json" ]
CMD [ "python","/home/script/config.py" ]