#!/bin/bash

set -e

trap 'echo -ne "\n:::\n:::\tCaught signal, exiting at line $LINENO, while running :${BASH_COMMAND}:\n:::\n"; exit' SIGINT SIGQUIT

current_path=$(pwd)
archive_file="$1"

if [ ! -f ${archive_file} ]; then
	echo -e "Usage:"
	echo -e "\t$0 <archive_file>"
	echo -e " e.g. $0 '_OUTPUT_/2019-05-13T11-04-33.tar.gz'"
	exit 1
fi

tmp_dir="/tmp/restore_grafana.$$"
mkdir -p "$tmp_dir"
tar -xzf ${archive_file} -C $tmp_dir

for j in folder datasource dashboard alert_channel
do
	find ${tmp_dir} -type f -name "*.${j}" | while read f
	do
		python "${current_path}/src/create_${j}.py" "${f}"
	done
done

rm -rf $tmp_dir
