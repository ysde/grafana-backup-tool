#!/bin/bash

set -e

trap 'echo -ne "\n:::\n:::\tCaught signal, exiting at line $LINENO, while running :${BASH_COMMAND}:\n:::\n"; exit' SIGINT SIGQUIT

settings_file="${1:-grafanaSettings.json}"
backup_dir="_OUTPUT_"

if [[ ! -f "${settings_file}" ]]; then
	echo "Usage:"
	echo -e "\t$0 <path_to_settings_file>"
	echo -e "\te.g. $0 '/path/to/grafanaSettings.json'"
	exit 1
fi

python -m grafana_backup.cli save --config "$settings_file"
