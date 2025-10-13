import os
import boto3
import requests
import logging
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

grafanaUrl = os.getenv("GRAFANA_URL", "http://localhost:3000")
grafanaSAUrl = f"{grafanaUrl}/api/serviceaccounts"
grafanaSATokenUrl = f"{grafanaSAUrl}/{{}}/tokens"

HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def grafana_auth():
    user = os.getenv("GRAFANA_ADMIN_USER")
    password = os.getenv("GRAFANA_ADMIN_PASSWORD")
    if not user or not password:
        raise ValueError("Missing GRAFANA_ADMIN_USER or GRAFANA_ADMIN_PASSWORD")
    return HTTPBasicAuth(user, password)


def create_service_account(auth):
    payload = {"name": "grafana-backup-tool", "role": "Admin", "isDisabled": False}
    response = requests.post(
        grafanaSAUrl,
        headers=HEADERS,
        auth=auth,
        json=payload,
        timeout=30,
    )
    if response.ok:
        data = response.json()
        logging.info("Service account created: %s", data)
        return data["id"]
    else:
        logging.error(
            "Failed to create service account [%s]: %s",
            response.status_code,
            response.text,
        )
        raise RuntimeError("Grafana service account creation failed")


def create_service_account_token(auth, account_id):
    payload = {"name": "grafana"}
    response = requests.post(
        grafanaSATokenUrl.format(account_id),
        headers=HEADERS,
        auth=auth,
        json=payload,
        timeout=30,
    )
    if response.ok:
        data = response.json()
        logging.info("Service account token created: %s", data)
        return data
    else:
        logging.error(
            "Failed to create service account token [%s]: %s",
            response.status_code,
            response.text,
        )
        raise RuntimeError("Grafana service account token creation failed")


def init_grafana():
    try:
        auth = grafana_auth()
        account_id = create_service_account(auth)
        token = create_service_account_token(auth, account_id)
        return {"account_id": account_id, "token": token}
    except Exception as e:
        logging.exception("Grafana initialization error")
        return None


def create_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_ACCESS_KEY"),
        region_name=os.getenv("MINIO_DEFAULT_REGION"),
    )

    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        logging.warning("S3_BUCKET_NAME is not set")
        return None

    try:
        s3.create_bucket(Bucket=bucket_name)
        logging.info("Bucket '%s' created successfully", bucket_name)
        return bucket_name
    except Exception as e:
        logging.exception("Error creating bucket")
        return None


if __name__ == "__main__":
    init_grafana()
    create_bucket()
