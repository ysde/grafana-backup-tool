# Grafana Dashboard Backup Tool

A Python-based application to backup Grafana settings via [Grafana API](http://docs.grafana.org/http_api/overview/).

## Current support components
* Dashboard (contains Alert)
* Datasource
* AlertChannel

## Requirements
* bash
* python 2.7, python 3.x with `requests` (https://2.python-requests.org/en/master/) library installed (`pip install requests`)
* access to a Grafana 3.0 API server

## Configuration
* Uses `environment variables` to define the connection to a Grafana server.
* Or alternatively hard-coded settings in `src/grafanaSettings.py`.

If you use `environment variables`, you need to add the following to your `.bashrc` or execute once before using the tool:

(`GRAFANA_HEADERS` is optional, use it if necessary. please see [#45](https://github.com/ysde/grafana-backup-tool/issues/45))
```bash
# Do not use a trailing slash on GRAFANA_URL
export GRAFANA_URL=http://some.host.org:3000
export GRAFANA_TOKEN=eyJrIjoidUhaU2ZQQndrWFN3RRVkUnVfrT56a1JoaG9KWFFObEgiLCJuIjoiYWRtaW4iLCJpZCI6MX0=
# GRAFANA_HEADERS is optional
export GRAFANA_HEADERS=Host:some.host.org 
```

There is [official documentation](http://docs.grafana.org/http_api/auth/) how to obtain the `TOKEN` for your installation.

## How to Use
* First perform **Configuration** as described above.
* Use `backup_grafana.sh` to backup all your dashboards, datasources and folders to the `_OUTPUT_` subdirectory of the current directory.
 For example:
```bash
$ ./backup_grafana.sh
$ tree _OUTPUT_
_OUTPUT_/
└── 2019-05-13T08-48-03.tar.gz
```
* Use `restore_grafana.sh` with a path to a previous backup to restore everything. **NOTE** this *may* result in data loss, by overwriting data on the server.

## Docker
Replace variables below to use docker version of this tool
* `{YOUR_GRAFANA_TOKEN}`: Your grafana site token.
* `{YOUR_GRAFANA_URL}`: Your grafana site url.
* `{YOUR_BACKUP_FOLDER_ON_THE_HOST}`: The backup folder on the host machine.

### Backup

```
docker run --rm --name grafana-backup-tool \
   -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
   -e GRAFANA_URL={YOUR_GRAFANA_URL} \
   -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
   ysde/docker-grafana-backup-tool
```

***example:***

```
docker run --rm --name grafana-backup-tool \
   -e GRAFANA_TOKEN=eyJrIjoiU2Y4eTByUGExOEZhajNYaTVyZTBuNlJOc3NaYkJiY3oiLCJuIjoiYWRtaW4iLCJpZCI6MX0= \
   -e GRAFANA_URL=http://localhost:3000 \
   -v /tmp/backup/:/opt/grafana-backup-tool/_OUTPUT_  \
   ysde/docker-grafana-backup-tool
```


### Restore

```
docker run --rm --name grafana-backup-tool \
   -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
   -e GRAFANA_URL={YOUR_GRAFANA_URL} \
   -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
   ysde/docker-grafana-backup-tool restore _OUTPUT_/{THE_ARCHIVED_FILE}
```

***example:***

```
docker run --rm --name grafana-backup-tool \
   -e GRAFANA_TOKEN=eyJrIjoiU2Y4eTByUGExOEZhajNYaTVyZTBuNlJOc3NaYkJiY3oiLCJuIjoiYWRtaW4iLCJpZCI6MX0= \
   -e GRAFANA_URL=http://localhost:3000 \
   -v /tmp/backup/:/opt/grafana-backup-tool/_OUTPUT_  \
   ysde/docker-grafana-backup-tool restore _OUTPUT_/2019-09-09T10-00-00.tar.gz
```


## Notes
* Please have a look at the two scripts in the root directory if you need to customize something.
