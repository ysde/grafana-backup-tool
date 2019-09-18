#!/bin/bash

echo "$1"
restore_or_backup=$1
restore_or_backup=${restore_or_backup:=backup}

if [ "$restore_or_backup" == "restore" ]; then
  echo "Resotring grafana"
  ./restore_grafana.sh "$2"
else
  echo "Backing up grafana"
  ./backup_grafana.sh
fi
