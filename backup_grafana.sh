#!/bin/bash

current_path=`pwd`
current_time=`date +"%Y-%m-%d_%T"`
compressed_dashboards_name="dashboards.tar.gz"
compressed_datasources_name="datasources.tar.gz"
compressed_folders_name="folders.tar.gz"

echo $current_time

dashboard_backup_path="/tmp/dashboards/$current_time"
datasource_backup_path="/tmp/datasources/$current_time"
folders_backup_path="/tmp/folders/$current_time"

if [ ! -d "$dashboard_backup_path" ]; then
  mkdir -p "$dashboard_backup_path"
fi

if [ ! -d "$datasource_backup_path" ]; then
  mkdir -p "$datasource_backup_path"
fi

if [ ! -d "$folders_backup_path" ]; then
  mkdir -p "$folders_backup_path"
fi

python "${current_path}/saveDashboards.py" $dashboard_backup_path
python "${current_path}/saveDatasources.py" $datasource_backup_path
python "${current_path}/saveFolders.py" $folders_backup_path

tar -zcvf "/tmp/$compressed_dashboards_name" $dashboard_backup_path
tar -zcvf "/tmp/$compressed_datasources_name" $datasource_backup_path
tar -zcvf "/tmp/$compressed_folders_name" $folders_backup_path
