# Grafana Backup Tool

A Python-based application to backup Grafana settings using the [Grafana API](https://grafana.com/docs/grafana/latest/http_api/).

The aim of this tool is to:
1. Easily backup and restore Grafana.
2. Have versioned backups`(date and time in file name)` for restoring and saving to cloud storage providers like `Amazon S3` or `Azure Storage`.

## Supported components
* Folder
* Dashboard (contains Alert)
* Datasource
* Alert Channel

## Requirements
* Bash
* Python 2.7 or Python 3.x
* Access to a Grafana API server.
* A `Token` of an `Admin` role (see `Configuration` section below for more info)

## Configuration
There are three ways to setup the configuration:
1. Use `environment variables` to define the variables for connecting to a Grafana server.
2. Use `hard-coded settings` in `conf/grafanaSettings.json` (this is the default settings file if not specified otherwise).
3. Use `~/.grafana-backup.json` to define variables in json format.

**NOTE** If you use `environment variables`, you need to add the following to your `.bashrc` or execute once before using the tool (please change variables according to your setup):

(`GRAFANA_HEADERS` is optional, use it if necessary. please see [#45](https://github.com/ysde/grafana-backup-tool/issues/45))
```bash
# Do not use a trailing slash on GRAFANA_URL
export GRAFANA_URL=http://some.host.org:3000
export GRAFANA_TOKEN=eyJrIjoidUhaU2ZQQndrWFN3RRVkUnVfrT56a1JoaG9KWFFObEgiLCJuIjoiYWRtaW4iLCJpZCI6MX0=
# GRAFANA_HEADERS is optional
export GRAFANA_HEADERS=Host:some.host.org 
```

To create and obtain a `Token` for your Grafana server, please refer to the [official documentation](https://grafana.com/docs/grafana/latest/http_api/auth/). 

**NOTE** that you need to generate a `Token` with an `Admin` role for the backup to succeed, otherwise you will have potential permission issues.

## Installation
First clone this repo
```
git clone https://github.com/ysde/grafana-backup-tool.git
cd grafana-backup-tool
```
Create a virtualenv, you could using something like `pyenv` if you'd prefer
```
virtualenv -p $(which python3) venv
source venv/bin/activate
```
Installation works best using `pip`
```
pip install .
```

## How to Use
* First perform the **Configuration** and **Installation** sections as described above.
* Use the `grafana-backup save` command to backup all your folders, dashboards, datasources and alert channels to the `_OUTPUT_` subdirectory of the current directory.

***Example:***
```bash
$ grafana-backup save
$ tree _OUTPUT_
_OUTPUT_/
└── 202006272027.tar.gz
```

* Use the `grafana-backup restore <archive_file>` command with a path to a previous backup to restore everything.

**NOTE** this *may* result in data loss, by overwriting data on the server.

***Example:***
```bash
$ grafana-backup restore _OUTPUT_/202006272027.tar.gz
```

## Docker
Replace variables below to use the Docker version of this tool
* `{YOUR_GRAFANA_TOKEN}`: Your Grafana site `Token`.
* `{YOUR_GRAFANA_URL}`: Your Grafana site `URL`.
* `{YOUR_BACKUP_FOLDER_ON_THE_HOST}`: The `backup folder` on the Grafana host machine.

### Backup

If you decide to use a volume (-v) then you'll need to create the volume first with 1337 uid/gid ownership first, example:
```
mkdir /tmp/backup
sudo chown 1337:1337 /tmp/backup
```

```
docker run --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
           -e GRAFANA_URL={YOUR_GRAFANA_URL} \
           -e VERIFY_SSL={True/False} \
           -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
           alpinebased:grafana-backup
```

***Example:***

```
docker run --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN="eyJrIjoiNGZqTDEyeXNaY0RsMXNhbkNTSnlKN2M3bE1VeHdqVTEiLCJuIjoiZ3JhZmFuYS1iYWNrdXAiLCJpZCI6MX0=" \
           -e GRAFANA_URL=http://192.168.0.79:3000 \
           -e VERIFY_SSL=False \
           -v /tmp/backup/:/opt/grafana-backup-tool/_OUTPUT_ \
           alpinebased:grafana-backup
```


### Restore

```
docker run --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
           -e GRAFANA_URL={YOUR_GRAFANA_URL} \
           -e VERIFY_SSL={True/False} \
           -e RESTORE="true" \
           -e ARCHIVE_FILE={THE_ARCHIVED_FILE_NAME} \
           -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
           alpinebased:grafana-backup
```

***Example:***

```
docker run --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN="eyJrIjoiNGZqTDEyeXNaY0RsMXNhbkNTSnlKN2M3bE1VeHdqVTEiLCJuIjoiZ3JhZmFuYS1iYWNrdXAiLCJpZCI6MX0=" \
           -e GRAFANA_URL=http://192.168.0.79:3000 \
           -e VERIFY_SSL=False \
           -e RESTORE="true" \
           -e ARCHIVE_FILE="202006280247.tar.gz" \
           -v /tmp/backup/:/opt/grafana-backup-tool/_OUTPUT_ \
           alpinebased:grafana-backup
```

### Building
You can build the docker image simply by executing `make` in the root of this repo. The image will get tagged as `alpinebased:grafana-backup`
