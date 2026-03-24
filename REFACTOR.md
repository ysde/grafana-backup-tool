# 📊 Grafana Backup Tool (Modern Fork)

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Grafana Support](https://img.shields.io/badge/grafana-v12.x-orange.svg)](https://grafana.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python-based tool to backup and restore Grafana settings via API.  
This is a **maintained fork** of [ysde/grafana-backup-tool](https://github.com/ysde/grafana-backup-tool), updated for modern Grafana versions.

> [!IMPORTANT]
> **Why use this fork?** > Unlike the original tool, this version fully supports **Grafana 12.x** and fixes the critical bugs that has existed since Grafana 8.0.0.

---

## 📑 Table of Contents
- [📊 Grafana Backup Tool (Modern Fork)](#-grafana-backup-tool-modern-fork)
  - [📑 Table of Contents](#-table-of-contents)
  - [🚀 Quick Start](#-quick-start)
  - [✨ Key Improvements](#-key-improvements)
  - [📦 Supported Components](#-supported-components)
  - [⚙️ Configuration](#️-configuration)
    - [Core Variables](#core-variables)
  - [🛠 Installation](#-installation)
    - [Using Virtual Environment](#using-virtual-environment)
  - [🐳 Docker \& Kubernetes](#-docker--kubernetes)
    - [Docker](#docker)
    - [Kubernetes](#kubernetes)
  - [☁️ Cloud Storage](#️-cloud-storage)
    - [Amazon S3](#amazon-s3)
    - [Azure Blob Storage](#azure-blob-storage)
    - [Google Cloud Storage (GCS)](#google-cloud-storage-gcs)
    - [AIStor ex. MinIO](#aistor-ex-minio)
  - [💡 Future Ideas](#-future-ideas)
  - [🤝 Contribution](#-contribution)

---

## 🚀 Quick Start
If you just want to run a quick backup to a local folder:

```bash
export GRAFANA_URL=http://your-grafana:3000
export GRAFANA_TOKEN=your_admin_token
pip install .
grafana-backup save
```

---

## ✨ Key Improvements
* ✅ **Grafana 11.x Ready**: Fixed authentication and API schema changes.
* ✅ **Library Panels Fix**: Proper restoration of library elements (tested v8.4.3 to v11.x).
* ✅ **Unified Alerting**: Support for Alert Rules, Contact Points, and Policies (v9.4.0+).
* ✅ **Security Updates**: Modernized base Docker images and dependencies.

---

## 📦 Supported Components
| Component          | Backup | Restore | Notes                     |
| :----------------- | :----: | :-----: | :------------------------ |
| **Dashboards**     |   ✅    |    ✅    | Includes embedded alerts  |
| **Folders**        |   ✅    |    ✅    | Includes permissions      |
| **Library Panels** |   ✅    |    ✅    | **Fixed in this fork**    |
| **Datasources**    |   ✅    |    ✅    | -                         |
| **Alert Rules**    |   ✅    |    ✅    | v9.4.0+ required          |
| **Teams/Users**    |   ✅    |    ✅    | Requires Admin Basic Auth |
| **Snapshots**      |   ✅    |    ✅    | -                         |

---

## ⚙️ Configuration
You can configure the tool via `grafanaSettings.json` or **Environment Variables** (preferred).

### Core Variables
| Variable                 | Description                              | Required             |
| :----------------------- | :--------------------------------------- | :------------------- |
| `GRAFANA_URL`            | URL of your Grafana (no trailing slash)  | **Yes**              |
| `GRAFANA_TOKEN`          | Admin API Token or Service Account Token | **Yes**              |
| `GRAFANA_ADMIN_ACCOUNT`  | Admin username (for Teams/Users backup)  | No                   |
| `GRAFANA_ADMIN_PASSWORD` | Admin password                           | No                   |
| `VERIFY_SSL`             | Set to `False` for self-signed certs     | No (Default: `True`) |

> [!TIP]
> We highly recommend using a **Service Account Token** with Admin permissions.

---

## 🛠 Installation
### Using Virtual Environment
```bash
virtualenv -p $(which python3) venv
source venv/bin/activate
pip install .
```

---

## 🐳 Docker & Kubernetes
### Docker
```bash
docker run --rm --name grafana-backup-tool \
  -e GRAFANA_TOKEN="your_token" \
  -e GRAFANA_URL="http://grafana:3000" \
  -v /tmp/backup:/opt/grafana-backup-tool/_OUTPUT_ \
  dealfa/grafana-backup-tool:v1.5.0 grafana-backup save
```

### Kubernetes
- **Helm Chart**: Available in the `/charts` directory.
- **CronJob**: See [examples/cronjob.yaml](examples) for scheduled backups.

---

## ☁️ Cloud Storage
The tool supports versioned archives automatically uploaded to any S3-compatible storages such as:

### Amazon S3
```bash
-e AWS_S3_BUCKET_NAME="my-bucket" \
-e AWS_DEFAULT_REGION="us-east-1" \
-e AWS_ACCESS_KEY_ID="xxx" \
-e AWS_SECRET_ACCESS_KEY="yyy"
```

### Azure Blob Storage
```bash
-e AZURE_STORAGE_CONTAINER_NAME="my-container" \
-e AZURE_STORAGE_CONNECTION_STRING="my-connection-string"
```

### Google Cloud Storage (GCS)
```bash
-e GCS_BUCKET_NAME="my-bucket" \
-e GCLOUD_PROJECT="my-project" \
-e GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```
### [AIStor](https://github.com/minio/minio) ex. MinIO
```bash
-e 
```

---

## 💡 Future Ideas
1. **GitOps Mode**: Save dashboards as raw JSON (no archive) for easy Git tracking.
2. **Multi-Org Support**: Iterate through all organizations automatically.
3. **Selective Restore**: Restore only specific folders or dashboard UID patterns.
4. **Modern CLI**: Migration to `Typer` for better command-line experience.

---

## 🤝 Contribution
1. Clone the repo.
2. Run test stack: `cd tests && docker-compose up -d`.
3. Run TUI debug: `PYTHONPATH=.. python3 tests/grafana_backup_tui.py`.

---
*Maintained with ❤️ by DuraCHYo. Original tool by ysde.*