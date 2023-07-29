FROM alpine:latest

LABEL maintainer="ysde108@gmail.com"

ARG UID=1337
ARG GID=1337
ENV RESTORE false
ENV ARCHIVE_FILE ""

ENV DEV_PACKAGES="\
    gcc \
    libc-dev \
    libffi-dev \
    py3-pip \
    python3-dev \
"

ENV PACKAGES="\
    bash \
    ca-certificates \
    py3-cffi \
    py3-cryptography \
    py3-six \
"
WORKDIR /opt/grafana-backup-tool
ADD . /opt/grafana-backup-tool

RUN chmod -R a+r /opt/grafana-backup-tool \
 && find /opt/grafana-backup-tool -type d -print0 | xargs -0 chmod a+rx

RUN echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk add --no-cache --virtual build-deps ${DEV_PACKAGES} \
    && apk add --no-cache ${PACKAGES} \
    && pip3 --no-cache-dir install . \
    && chown -R ${UID}:${GID} /opt/grafana-backup-tool \
    && apk del build-deps

USER ${UID}
CMD sh -c 'if [ "$RESTORE" = true ]; then if [ ! -z "$AWS_S3_BUCKET_NAME" ] || [ ! -z "$AZURE_STORAGE_CONTAINER_NAME" ]; then grafana-backup restore $ARCHIVE_FILE; else grafana-backup restore _OUTPUT_/$ARCHIVE_FILE; fi else grafana-backup save; fi'
