FROM alpine:latest

ENV RESTORE=false
ENV ARCHIVE_FILE=""

WORKDIR /opt/grafana-backup-tool
ADD . /opt/grafana-backup-tool

RUN apk add --no-cache bash ca-certificates python3 py3-pip && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -e . && \
    chmod -R a+r /opt/grafana-backup-tool && \
    find /opt/grafana-backup-tool -type d -print0 | xargs -0 chmod a+rx && \
    chown -R 1337:1337 /opt/grafana-backup-tool

USER 1337
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/grafana-backup-tool:$PYTHONPATH"

CMD sh -c 'if [ "$RESTORE" = "true" ]; then \
    if [ ! -z "$AWS_S3_BUCKET_NAME" ] || [ ! -z "$AZURE_STORAGE_CONTAINER_NAME" ] || [ ! -z "$GCS_BUCKET_NAME" ]; then \
        grafana-backup restore $ARCHIVE_FILE; \
    else \
        grafana-backup restore _OUTPUT_/$ARCHIVE_FILE; \
    fi \
else \
    grafana-backup save; \
fi'