#!/bin/bash

current_path=`pwd`
folders_path="$1"

if [ $# -ne 1 ]; then
  echo "Please input the backup folder path.  e.g. /tmp/folders/2018-01-01"
  exit 1
fi

find "$folders_path"  -mindepth 1 -name "*.folder" | while read f ; do
  echo "$f"
  python $current_path/createFolder.py "$f"
done
