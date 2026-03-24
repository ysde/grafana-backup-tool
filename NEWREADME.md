# Grafana Backup Tool
This is a maintained Fork from [ysde/grafana-backup-tool](https://github.com/ysde/grafana-backup-tool)
A Python-based application to backup Grafana settings using the [Grafana API](https://grafana.com/docs/grafana/latest/http_api/).

The aim of this tool is to:
1. Easily backup and restore Grafana (now supporting **Grafana 9.x, 10.x, and 11.x**).
2. Have versioned backups `(date and time in file name)` for restoring and saving to cloud storage providers. Currently support:
   1. `Amazon S3`
   2. `Azure Storage`
   3. `GCP Cloud Storage` (Use service-account's credential file, [see here](https://cloud.google.com/storage/docs/reference/libraries#linux-or-macos))

## 🚀 Improvements in this Fork
* ✅ **Grafana 12.x Compatibility**: Fixed API authentication and schema changes introduced in recent versions.
* ✅ **Library Panels Fix**: Resolved the critical bug (present since Grafana 8.0.0) where Library Panels failed to restore correctly.
* ✅ **Unified Alerting**: Enhanced support for **Alert Rules**, **Contact Points**, and **Notification Policies** (v9.4.0 and up).
* ✅ **Updated Dependencies**: Modernized base images and Python libraries for improved security and stability.

## Supported components
* Folder
* Folder Permissions
* Library Elements (**Fixed!** Tested with Grafana 8.4.3 up to 11.x)
* Dashboard (contains Alert)
* Datasource
* Alert Channel (Legacy)
* Alert Rules (Supported in version 9.4.0 of Grafana and up.)
* Teams
* Team Members (Needs Basic Authentication (username and password, see [grafana doc](https://grafana.com/docs/grafana/latest/http_api/org/#admin-organizations-api))
    * You need to set `Admin's account and password` in `grafanaSettings.json`, or set the base64 encoded `admin account and password` in ENV `GRAFANA_BASIC_AUTH`. E.g `export GRAFANA_BASIC_AUTH=YWRtaW46YWRtaW4=`
    * Or Sets this ENV of the Grafana server `GF_USERS_ALLOW_ORG_CREATE=true`. see [grafana doc](https://grafana.com/docs/grafana/latest/http_api/org/#create-organization)
* Organization (Needs Basic Authentication (username and password, see [grafana doc](https://grafana.com/docs/grafana/latest/http_api/org/#admin-organizations-api))
    * You need to set `Admin's account and password` in `grafanaSettings.json`, or set the base64 encoded `admin account and password` in ENV `GRAFANA_BASIC_AUTH`. E.g `export GRAFANA_BASIC_AUTH=YWRtaW46YWRtaW4=`
    * Or Sets this ENV of the Grafana server `GF_USERS_ALLOW_ORG_CREATE=true`. see [grafana doc](https://grafana.com/docs/grafana/latest/http_api/org/#create-organization)
* User (Needs Basic Authentication (username and password, see [grafana doc](https://grafana.com/docs/grafana/latest/http_api/org/#admin-organizations-api))
    * You need to set `Admin's account and password` in `grafanaSettings.json`, or set the base64 encoded `admin account and password` in ENV `GRAFANA_BASIC_AUTH`. E.g `export GRAFANA_BASIC_AUTH=YWRtaW46YWRtaW4=`
    * Grafana's api doesn't provide user's password when backing up, so the `default_user_password` in `grafanaSettings.json`, or in ENV `DEFAULT_USER_PASSWORD`, E.g `export DEFAULT_USER_PASSWORD=supersecret` will be used when restoring. 
* Snapshots
* Dashboard Versions (only backup, no restore)
* Annotations

**NOTE** The only supported `orgId` right now is `1`, the default organization will be backed up only!

## Requirements
* Bash
* Python 3.x
* Access to a Grafana API server.
* A `Token` of an `Admin` role (Service Account token recommended for v9+).

## Configuration
There are three ways to setup the configuration:

1. Use `environment variables` to define the variables for connecting to a Grafana server.
2. Use `hard-coded settings` in `conf/grafanaSettings.json` (this is the default settings file if not specified otherwise).
3. Use `~/.grafana-backup.json` to define variables in json format.

### Example Config
* Copy [grafanaSettings.example.json](examples/grafanaSettings.example.json) and modify it for you to use, remove `azure`, `aws`, `gcp`, `influxdb` blocks (but keep the ones you used).
* Check out the [examples](examples) folder for more configuration details.

**NOTE** If you use `environment variables`, you need to add the following to your `.bashrc` or execute once before using the tool (please change variables according to your setup):

(`GRAFANA_HEADERS` is optional, use it if necessary. please see [#45](https://github.com/ysde/grafana-backup-tool/issues/45))

```bash
### Do not use a trailing slash on GRAFANA_URL
export GRAFANA_URL=[http://some.host.org:3000](http://some.host.org:3000)
export GRAFANA_TOKEN=eyJrIjoidUhaU2ZQQndrWFN3RRVkUnVfrT56a1JoaG9KWFFObEgiLCJuIjoiYWRtaW4iLCJpZCI6MX0=

# GRAFANA_HEADERS is optional
export GRAFANA_HEADERS=Host:some.host.org
```

To create and obtain a `Token` for your Grafana server, please refer to the [official documentation](https://grafana.com/docs/grafana/latest/developers/http_api/auth/).

**NOTE** that you need to generate a `Token` with an `Admin` role for the backup to succeed, otherwise you will have potential permission issues.

## Installation
### Virtual environment (optional but recommended)
Create a virtualenv, you could using something like `pyenv` if you'd prefer:

```bash
virtualenv -p $(which python3) venv
source venv/bin/activate
```

### Installation using this repo
First clone this repo:

```bash
git clone [https://github.com/DuraCHYo/grafana-backup-tool.git](https://github.com/DuraCHYo/grafana-backup-tool.git)
cd grafana-backup-tool
```

Installation works best using `pip`:

```bash
pip install .
```

## How to Use
* First perform the **Configuration** and **Installation** sections as described above.
* Use the `grafana-backup save` command to backup all your folders, dashboards, datasources and alert channels to the `_OUTPUT_` subdirectory of the current directory.

***Example:***

```bash
$grafana-backup save$ tree _OUTPUT_
_OUTPUT_/
└── 202603242027.tar.gz
```

* Use the `grafana-backup restore <archive_file>` command with a path to a previous backup to restore everything.

**NOTE** this *may* result in data loss, by overwriting data on the server.

***Example:***

```bash
$ grafana-backup restore _OUTPUT_/202603242027.tar.gz
```

## Docker
### Docker Image available on [Docker Hub](https://hub.docker.com/r/dealfa/grafana-backup-tool) 
Replace variables below to use the Docker version of this tool:
* `{YOUR_GRAFANA_TOKEN}`: Your Grafana site `Token`.
* `{YOUR_GRAFANA_URL}`: Your Grafana site `URL`.
* `{YOUR_BACKUP_FOLDER_ON_THE_HOST}`: The `backup folder` on the Grafana host machine.

## Kubernetes
### Helm Chart is available from [v1.4.5 release](charts)
Check out the CronJob in [examples](examples) for a simple example of how grafana-backup-tool can be ran without Helm.

### Backup
If you decide to use a volume (-v) then you'll need to create the volume first with 1337 uid/gid ownership first, example:

```bash
mkdir /tmp/backup
sudo chown 1337:1337 /tmp/backup
```

```bash
docker run --user $(id -u):$(id -g) --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
           -e GRAFANA_URL={YOUR_GRAFANA_URL} \
           -e GRAFANA_ADMIN_ACCOUNT={YOUR_GRAFANA_ADMIN_ACCOUNT} \
           -e GRAFANA_ADMIN_PASSWORD={YOUR_GRAFANA_ADMIN_PASSWORD} \
           -e VERIFY_SSL={True/False} \
           -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
           DuraCHYo/docker-grafana-backup-tool save
```

***S3 Example:*** Set S3 configurations in `-e` or `grafanaSettings.json` ([example](https://github.com/DuraCHYo/grafana-backup-tool/blob/master/examples/grafanaSettings.example.json))

```bash
           -e AWS_S3_BUCKET_NAME="my-backups-bucket" \
           -e AWS_S3_BUCKET_KEY="grafana-backup-folder" \
           -e AWS_DEFAULT_REGION="us-east-1" \
           -e AWS_ACCESS_KEY_ID="secret" \
           -e AWS_SECRET_ACCESS_KEY="secret" \
```

***Azure Example:*** Set Azure configurations in `-e` or `grafanaSettings.json`

```bash
           -e AZURE_STORAGE_CONTAINER_NAME="azure-storage-container-name" \
           -e AZURE_STORAGE_CONNECTION_STRING="azure-storage-connection-string"
```

***GCS Example:*** Set GCS configurations in `-e` or `grafanaSettings.json`

```bash
           -e GCS_BUCKET_NAME="backups-bucket-name" \
           -e GCS_BUCKET_PATH="grafana-backup-folder" \
           -e GCLOUD_PROJECT="gcp-project-name" \
           -e GOOGLE_APPLICATION_CREDENTIALS="credential-file-path"
```

### Restore

```bash
docker run --user $(id -u):$(id -g) --rm --name grafana-backup-tool \
           -e GRAFANA_TOKEN={YOUR_GRAFANA_TOKEN} \
           -e GRAFANA_URL={YOUR_URL} \
           -e GRAFANA_ADMIN_ACCOUNT={YOUR_GRAFANA_ADMIN_ACCOUNT} \
           -e GRAFANA_ADMIN_PASSWORD={YOUR_GRAFANA_ADMIN_PASSWORD} \
           -e VERIFY_SSL={True/False} \
           -e RESTORE="true" \
           -e ARCHIVE_FILE={THE_ARCHIVED_FILE_NAME} \
           -v {YOUR_BACKUP_FOLDER_ON_THE_HOST}:/opt/grafana-backup-tool/_OUTPUT_  \
           DuraCHYo/docker-grafana-backup-tool
```

### Contribution
Docker-compose is available in `tests` dir. It uses grafana and minio to test putting backup in S3.
Also, for simple debug you can run TUI script:

```bash
cd ./tests && PYTHONPATH=.. python3 grafana_backup_tui.py
```

### Building
You can build the docker image simply by executing `make` in the root of this repo. The image will get tagged as `DuraCHYo/docker-grafana-backup-tool`.

### Monitoring
InfluxDB support has been added. In order to monitor successful backups with InfluxDB simply configure `grafana-backup` InfluxDB settings using this [examples](examples) configuration. Or if you prefer to use environment variables you can instead set `INFLUXDB_HOST`, `INFLUXDB_PORT`, `INFLUXDB_MEASUREMENT`, `INFLUXDB_USERNAME` and `INFLUXDB_PASSWORD`.

---

## 💡 Ideas for Improvement
* **GitOps Workflow (Unpacked Mode)**: Add a `--no-archive` flag to save dashboards as raw JSON files in a directory tree. This allows users to commit changes directly to a Git repository and track version history via `git diff`.
* **Multi-Organization Support**: Extend the tool to automatically iterate through all Organizations using the `/api/orgs` endpoint, rather than being limited to `orgId: 1`.
* **Selective Component Restore**: Implement flags like `--only-dashboards` or `--folders "Production"` to allow granular restoration without overwriting the entire Grafana instance.
* **Modern CLI Framework**: Migrate from `docopt` to `Typer` or `Click` for a more user-friendly CLI with auto-completion and better error handling.
* **Full Unified Alerting Support**: Deepen integration with Grafana 11+ Contact Points, Mute Timings, and Notification Policies which are currently partially covered.
* **Automated Compatibility Testing**: Setup GitHub Actions to run integration tests against multiple Grafana versions (using Docker containers) for every PR.
```
```