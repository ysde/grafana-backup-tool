#!/bin/bash

set -e

trap 'echo -ne "\n:::\n:::\tCaught signal, exiting at line $LINENO, while running :${BASH_COMMAND}:\n:::\n"; exit' SIGINT SIGQUIT



archive_file="$1"
settings_file="${2:-grafanaSettings.json}"

if [[ $# -ne 2 ]]; then
	echo "Usage:"
	echo -e "\t$0 <path_to_archive_file> <path_to_settings_file>"
	echo -e "\te.g. $0 '_OUTPUT_/2019-05-13T11-04-33.tar.gz' '/path/to/grafanaSettings.json'"
	exit 1
fi

python -m grafana_backup.cli --config $settings_file restore $archive_file
