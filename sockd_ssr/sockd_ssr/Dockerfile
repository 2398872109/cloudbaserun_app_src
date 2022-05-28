FROM python:3.7-alpine

ENV MIRROR https://public.sockd.info/source/

ENV DANTE_VER 1.4.2
ENV DANTE_URL $MIRROR/dante-$DANTE_VER.tar.gz
ENV DANTE_FILE dante.tar.gz
ENV DANTE_TEMP /tmp/danted
ENV DANTE_DIR  /home/danted
ENV DANTE_CONFIG /home/danted/conf/sockd.conf
ENV DANTE_PASSWD /home/danted/conf/sockd.passwd

ENV LIBPAM_URL $MIRROR/libpam-pwdfile.zip
ENV LIBPAM_FILE libpam-pwdfile.zip
ENV LIBPAM_DIR libpam-pwdfile-master
ENV LIBPAM_DANTE /etc/pam.d/sockd

ENV CONFIG_GUESS "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD"
ENV CONFIG_SUB "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD"

RUN apk add --no-cache linux-pam apache2-utils && \
    apk add --no-cache build-base linux-pam-dev && \
    mkdir -p ${DANTE_TEMP} && cd ${DANTE_TEMP} && \
    wget ${DANTE_URL} -O ${DANTE_FILE} && \
    tar xzf ${DANTE_FILE} --strip 1 && \
    wget ${CONFIG_GUESS} -O config.guess && \
    wget ${CONFIG_SUB} -O config.sub && \
    ac_cv_func_sched_setscheduler=no ./configure --with-sockd-conf=${DANTE_CONFIG} --prefix=${DANTE_DIR} && \
    make && make install && \
    cd ${DANTE_TEMP} && \
    wget ${LIBPAM_URL} -O ${LIBPAM_FILE} && unzip ${LIBPAM_FILE} && cd ${LIBPAM_DIR} && \
    make && make install && \
    echo "auth required pam_pwdfile.so pwdfile ${DANTE_PASSWD}" > ${LIBPAM_DANTE} && \
    echo "account required pam_permit.so" >> ${LIBPAM_DANTE} && \
    rm -rf ${DANTE_TEMP} && apk del --purge build-base linux-pam-dev

ADD conf "${DANTE_DIR}/conf"

ENV WORKPATH=/home

COPY shadowsocksr-3.2.2.tar.gz ${WORKPATH}/

RUN set -ex \
	&& apk add --no-cache tar libsodium-dev openssl \
	&& cd ${WORKPATH} \
	&& tar zxf shadowsocksr-3.2.2.tar.gz \
	&& mv shadowsocksr-3.2.2/shadowsocks . \
	&& rm -f shadowsocksr-3.2.2.tar.gz

ADD script "${WORKPATH}/script"
ADD config.json "${WORKPATH}/config.json"

ENV SOCKD_PORT=2020
ENV SOCKD_USERNAME=root
ENV SOCKD_PASSWORD=123456

ENV SERVER_PORT=9000
ENV PASSWORD=password
ENV METHOD=aes-256-cfb
ENV PROTOCOL=origin
ENV OBFS=plain

WORKDIR /home

CMD ["sh","script/start"]