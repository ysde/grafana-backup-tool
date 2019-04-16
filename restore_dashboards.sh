#!/bin/bash

current_path=`pwd`
dashboard_folder="$1"

if [ $# -ne 1 ]; then
  echo "Please input the backup folder path.  e.g. /tmp/dashboards/2018-01-01"
  exit 1
fi

find "$dashboard_folder" -mindepth 1 -name "*.dashboard" | while read f ; do
  echo "$f"
  python $current_path/createDashboard.py "$f"
done
