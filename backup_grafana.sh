#!/bin/bash
set -e

current_path=`pwd`
current_time=`date +"%Y-%m-%d-%H%M%S"`
backup_dir=/tmp/grafana_backup_$current_time
backup_dir_compressed=$backup_dir.tar.gz
echo $current_time

dashboard_backup_path="$backup_dir/dashboards"
datasource_backup_path="$backup_dir/datasources"
folders_backup_path="$backup_dir/folders"

if [ ! -d "$dashboard_backup_path" ]; then
  mkdir -p "$dashboard_backup_path"
fi

if [ ! -d "$datasource_backup_path" ]; then
  mkdir -p "$datasource_backup_path"
fi

if [ ! -d "$folders_backup_path" ]; then
  mkdir -p "$folders_backup_path"
fi

python "${current_path}/saveDashboards.py" $dashboard_backup_path || exit 0
python "${current_path}/saveDatasources.py" $datasource_backup_path || exit 0
python "${current_path}/saveFolders.py" $folders_backup_path || exit 0


tar -zcvf $backup_dir_compressed -C $backup_dir .
rm -rf $backup_dir

echo "create backup $backup_dir_compressed"
