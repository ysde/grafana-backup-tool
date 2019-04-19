#!/bin/bash -e

current_path=`pwd`
dashboard_folder="$1"

if [ $# -ne 1 ]; then
  echo "Please input the backup archive path.  e.g. /tmp/grafana_backup_2019-01-01-114306.tar.gz"
  exit 1
fi


tmp_dir="/tmp/grafana_restore"
mkdir "$tmp_dir"
tar -xzf $1 -C $tmp_dir

if [ -d $tmp_dir/datasources ]
then
  echo "restore datasources"
  bash $current_path/restore_datasources.sh $tmp_dir/datasources
fi

if [ -d $tmp_dir/folders ]
then
  echo "restore folders"
  bash $current_path/restore_folders.sh $tmp_dir/folders
fi

if [ -d $tmp_dir/dashboards ]
then
  echo "restore dashboards"
  bash $current_path/restore_dashboards.sh $tmp_dir/dashboards
fi

rm -rf $tmp_dir
