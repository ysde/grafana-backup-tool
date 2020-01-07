#!/bin/bash

set -e -x

trap 'echo -ne "\n:::\n:::\tCaught signal, exiting at line $LINENO, while running :${BASH_COMMAND}:\n:::\n"; exit' SIGINT SIGQUIT

current_path=$(pwd)
backup_dir="_OUTPUT_"
timestamp=$(date +"%Y-%m-%dT%H-%M-%S")
BACKUP_FOLDER="${CLUSTER_NAME}"
if [ -n "${GRAFANA_SERVICE_PORT}" ]; then
	GRAFANA_URL="${GRAFANA_URL}:${GRAFANA_SERVICE_PORT}"
fi

[ -d "${backup_dir}" ] || mkdir -p "${backup_dir}"

for i in dashboards datasources folders alert_channels
do
	F="${backup_dir}/${i}/${timestamp}"
	[ -d "${F}" ] || mkdir -p "${F}"
	python "${current_path}/src/save_${i}.py" "${F}"
done

tar -czvf "${backup_dir}/${timestamp}.tar.gz" ${backup_dir}/{dashboards,datasources,folders,alert_channels}/${timestamp}
rm -rf ${backup_dir}/{dashboards,datasources,folders,alert_channels}/${timestamp}
echo "Uploading grafana backup to S3 bucket ${S3_BACKUP}"
aws s3 cp ./"${backup_dir}"/"${timestamp}".tar.gz s3://"${S3_BACKUP}"/"${BACKUP_FOLDER}"/"${timestamp}".tar.gz