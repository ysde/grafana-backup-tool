#!/bin/bash

current_path=`pwd`
datasource_folder="$1"

if [ $# -ne 1 ]; then
  echo "Please input the backup folder path.  e.g. /tmp/datasources/2018-01-01"
  exit 1
fi

find "$datasource_folder" -name "*.datasource" -mindepth 1 | while read f ; do
  echo "$f"
  python $current_path/createDatasource.py "$f"
done

