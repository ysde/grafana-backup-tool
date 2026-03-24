python3 -m grafana_backup.cli restore --config grafana_backup/conf/grafanaSettings.json _OUTPUT_/202603240710.tar.gz
python3 -m grafana_backup.cli save grafana_backup/conf/grafanaSettings.json

docker exec -ti <container name> /garage status
garage layout assign -z dc1 -c 1G <node_id>
garage layout apply --version 1
garage bucket create backup-tool-bucket
garage key create backup-tool-key
---
Key ID:              GK8fd0d61da5e7b1659a24a171
Key name:            backup-tool-key
Secret key:          d084c2836e8e38bc0cf8ea9db915d15c0b8dad6ddd40219bdb733953f4b452da
Created:             2026-03-24 21:50:49.378 +00:00
Validity:            valid
Expiration:          never
---
garage bucket allow \
  --read \
  --write \
  --owner \
  backup-tool-bucket \
  --key backup-tool-key