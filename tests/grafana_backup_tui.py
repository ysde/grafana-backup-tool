#!/usr/bin/env python3
import os
import json
import boto3
import subprocess
import tempfile
import logging
import requests
import questionary
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


OUTPUT_DIR = "../_OUTPUT_"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "grafana-backup")


# ---------------- GRAFANA UTILS ----------------
def grafana_auth():
    user = os.getenv("GRAFANA_ADMIN_USER")
    password = os.getenv("GRAFANA_ADMIN_PASSWORD")
    if not user or not password:
        raise ValueError("Missing GRAFANA_ADMIN_USER or GRAFANA_ADMIN_PASSWORD")
    return HTTPBasicAuth(user, password)


def create_service_account(auth):
    url = f"{GRAFANA_URL}/api/serviceaccounts"
    payload = {"name": "grafana-backup-tool", "role": "Admin", "isDisabled": False}
    r = requests.post(url, json=payload, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def create_service_account_token(auth, account_id):
    url = f"{GRAFANA_URL}/api/serviceaccounts/{account_id}/tokens"
    payload = {"name": "grafana"}
    r = requests.post(url, json=payload, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()["key"]


def ensure_s3_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        s3_access_key_id=os.getenv("MINIO_ACCESS_KEY_ID"),
        s3_secret_access_key=os.getenv("MINIO_SECRET_ACCESS_KEY"),
        region_name=os.getenv("MINIO_DEFAULT_REGION", "us-east-1"),
    )
    try:
        s3.create_bucket(Bucket=S3_BUCKET_NAME)
        logging.info("Bucket '%s' created successfully", S3_BUCKET_NAME)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        logging.info("Bucket '%s' already exists", S3_BUCKET_NAME)
    except Exception as e:
        logging.warning("Bucket create failed: %s", e)


def build_config(token):
    return {
        "grafana": {"url": GRAFANA_URL, "token": token, "verify_ssl": False},
        "providers": {
            "s3": {
                "bucket": S3_BUCKET_NAME,
                "endpoint_url": MINIO_ENDPOINT,
                "access_key": os.getenv("MINIO_ACCESS_KEY_ID"),
                "secret_key": os.getenv("MINIO_SECRET_ACCESS_KEY"),
                "region": os.getenv("MINIO_DEFAULT_REGION", "us-east-1"),
            }
        },
    }


def write_temp_config(config):
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    json.dump(config, tmp, indent=2)
    tmp.flush()
    tmp.close()
    return tmp.name


# ---------------- ACTIONS ----------------
def do_backup():
    logging.info("Starting Grafana backup...")
    auth = grafana_auth()
    account_id = create_service_account(auth)
    token = create_service_account_token(auth, account_id)
    ensure_s3_bucket()
    cfg_path = write_temp_config(build_config(token))
    try:
        subprocess.run(
            ["python", "-m", "grafana_backup.cli", "save", "--config", cfg_path],
            check=True,
        )
        logging.info("Backup completed successfully.")
    finally:
        os.remove(cfg_path)


def do_restore():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".tar.gz")]
    if not files:
        print("No backup archives found in _OUTPUT_.")
        return
    choice = questionary.select("Select backup to restore:", choices=files).ask()
    if not choice:
        return
    archive_path = os.path.join(OUTPUT_DIR, choice)
    auth = grafana_auth()
    account_id = create_service_account(auth)
    token = create_service_account_token(auth, account_id)
    cfg_path = write_temp_config(build_config(token))
    try:
        subprocess.run(
            [
                "python",
                "-m",
                "grafana_backup.cli",
                "restore",
                "--config",
                cfg_path,
                archive_path,
            ],
            check=True,
        )
        logging.info("Restore completed successfully.")
    finally:
        os.remove(cfg_path)


# ---------------- MAIN MENU ----------------
def main():
    while True:
        action = questionary.select(
            "Grafana Backup Tool — choose action:",
            choices=[
                "📦 Make Backup",
                "♻️  Restore Backup",
                "🚪 Exit",
            ],
        ).ask()

        if action == "📦 Make Backup":
            do_backup()
        elif action == "♻️  Restore Backup":
            do_restore()
        else:
            break


if __name__ == "__main__":
    main()
