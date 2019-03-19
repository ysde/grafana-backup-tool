#!/bin/bash

current_path=`pwd`
folders_path="$1"

find "$folders_path" -name "*.folder" -mindepth 1 | while read f ; do
  echo "$f"
  python $current_path/createFolder.py "$f"
done
