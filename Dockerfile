FROM python:3.7-slim
LABEL maintainer="ysde108@gmail.com"
WORKDIR /opt/grafana-backup-tool
ADD . /opt/grafana-backup-tool
RUN pip install -r requirements.txt
ENTRYPOINT ./backup_grafana.sh
