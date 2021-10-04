import base64
import json
import os
from datetime import datetime
from grafana_backup.commons import load_config


def main(config_path):
    # Load config from optional configuration file located at ~/.grafana-backup.json
    # or load defaults from example config stored in grafanaSettings.json
    # environment variables can override settings as well and are top of the hierarchy

    config_dict = {}

    config = load_config(config_path)

    grafana_url = config.get('grafana', {}).get('url', '')
    grafana_token = config.get('grafana', {}).get('token', '')
    grafana_search_api_limit = config.get('grafana', {}).get('search_api_limit', 5000)

    debug = config.get('general', {}).get('debug', True)
    verify_ssl = config.get('general', {}).get('verify_ssl', False)
    client_cert = config.get('general', {}).get('client_cert', None)
    backup_dir = config.get('general', {}).get('backup_dir', '_OUTPUT_')
    backup_file_format = config.get('general', {}).get('backup_file_format', '%Y%m%d%H%M')
    pretty_print = config.get('general', {}).get('pretty_print', False)

    # Cloud storage settings - AWS
    aws_s3_bucket_name = config.get('aws', {}).get('s3_bucket_name', '')
    aws_s3_bucket_key = config.get('aws', {}).get('s3_bucket_key', '')
    aws_default_region = config.get('aws', {}).get('default_region', '')
    aws_access_key_id = config.get('aws', {}).get('access_key_id', '')
    aws_secret_access_key = config.get('aws', {}).get('secret_access_key', '')
    aws_endpoint_url = config.get('aws', {}).get('endpoint_url', None)
    # Cloud storage settings - Azure
    azure_storage_container_name = config.get('azure', {}).get('container_name', '')
    azure_storage_connection_string = config.get('azure', {}).get('connection_string', '')
    # Cloud storage settings - GCP
    gcp_config = config.get('gcp', {})
    gcs_bucket_name = gcp_config.get('gcs_bucket_name', '')
    google_application_credentials = gcp_config.get('google_application_credentials', '')

    admin_account = config.get('grafana', {}).get('admin_account', '')
    admin_password = config.get('grafana', {}).get('admin_password', '')

    GRAFANA_URL = os.getenv('GRAFANA_URL', grafana_url)
    TOKEN = os.getenv('GRAFANA_TOKEN', grafana_token)
    SEARCH_API_LIMIT = os.getenv('SEARCH_API_LIMIT', grafana_search_api_limit)

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', aws_s3_bucket_name)
    AWS_S3_BUCKET_KEY = os.getenv('AWS_S3_BUCKET_KEY', aws_s3_bucket_key)
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', aws_default_region)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', aws_access_key_id)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', aws_secret_access_key)
    AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL', aws_endpoint_url)

    AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME', azure_storage_container_name)
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', azure_storage_connection_string)

    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', gcs_bucket_name)
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS') and google_application_credentials:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials

    ADMIN_ACCOUNT = os.getenv('GRAFANA_ADMIN_ACCOUNT', admin_account)
    ADMIN_PASSWORD = os.getenv('GRAFANA_ADMIN_PASSWORD', admin_password)
    GRAFANA_BASIC_AUTH = os.getenv('GRAFANA_BASIC_AUTH', None)

    DEBUG = os.getenv('DEBUG', debug)
    if isinstance(DEBUG, str):
        DEBUG = json.loads(DEBUG.lower())  # convert environment variable string to bool

    VERIFY_SSL = os.getenv('VERIFY_SSL', verify_ssl)
    if isinstance(VERIFY_SSL, str):
        VERIFY_SSL = json.loads(VERIFY_SSL.lower())  # convert environment variable string to bool

    CLIENT_CERT = os.getenv('CLIENT_CERT', client_cert)

    BACKUP_DIR = os.getenv('BACKUP_DIR', backup_dir)

    PRETTY_PRINT = os.getenv('PRETTY_PRINT', pretty_print)
    if isinstance(PRETTY_PRINT, str):
        PRETTY_PRINT = json.loads(PRETTY_PRINT.lower())  # convert environment variable string to bool

    EXTRA_HEADERS = dict(
        h.split(':') for h in os.getenv('GRAFANA_HEADERS', '').split(',') if 'GRAFANA_HEADERS' in os.environ)

    if TOKEN:
        HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
        HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}
    else:
        HTTP_GET_HEADERS = {}
        HTTP_POST_HEADERS = {'Content-Type': 'application/json'}

    for k, v in EXTRA_HEADERS.items():
        HTTP_GET_HEADERS.update({k: v})
        HTTP_POST_HEADERS.update({k: v})

    TIMESTAMP = datetime.today().strftime(backup_file_format)

    config_dict['GRAFANA_URL'] = GRAFANA_URL
    config_dict['GRAFANA_ADMIN_ACCOUNT'] = ADMIN_ACCOUNT
    config_dict['GRAFANA_ADMIN_PASSWORD'] = ADMIN_PASSWORD

    if not GRAFANA_BASIC_AUTH and (ADMIN_ACCOUNT and ADMIN_PASSWORD):
        GRAFANA_BASIC_AUTH = base64.b64encode(
            "{0}:{1}".format(ADMIN_ACCOUNT, ADMIN_PASSWORD).encode('utf8')
        ).decode('utf8')

    if GRAFANA_BASIC_AUTH:
        HTTP_GET_HEADERS_BASIC_AUTH = HTTP_GET_HEADERS.copy()
        HTTP_GET_HEADERS_BASIC_AUTH.update({'Authorization': 'Basic {0}'.format(GRAFANA_BASIC_AUTH)})
        HTTP_POST_HEADERS_BASIC_AUTH = HTTP_POST_HEADERS.copy()
        HTTP_POST_HEADERS_BASIC_AUTH.update({'Authorization': 'Basic {0}'.format(GRAFANA_BASIC_AUTH)})
    else:
        HTTP_GET_HEADERS_BASIC_AUTH = None
        HTTP_POST_HEADERS_BASIC_AUTH = None

    config_dict['TOKEN'] = TOKEN
    config_dict['SEARCH_API_LIMIT'] = SEARCH_API_LIMIT
    config_dict['DEBUG'] = DEBUG
    config_dict['VERIFY_SSL'] = VERIFY_SSL
    config_dict['CLIENT_CERT'] = CLIENT_CERT
    config_dict['BACKUP_DIR'] = BACKUP_DIR
    config_dict['PRETTY_PRINT'] = PRETTY_PRINT
    config_dict['EXTRA_HEADERS'] = EXTRA_HEADERS
    config_dict['HTTP_GET_HEADERS'] = HTTP_GET_HEADERS
    config_dict['HTTP_POST_HEADERS'] = HTTP_POST_HEADERS
    config_dict['HTTP_GET_HEADERS_BASIC_AUTH'] = HTTP_GET_HEADERS_BASIC_AUTH
    config_dict['HTTP_POST_HEADERS_BASIC_AUTH'] = HTTP_POST_HEADERS_BASIC_AUTH
    config_dict['TIMESTAMP'] = TIMESTAMP
    config_dict['AWS_S3_BUCKET_NAME'] = AWS_S3_BUCKET_NAME
    config_dict['AWS_S3_BUCKET_KEY'] = AWS_S3_BUCKET_KEY
    config_dict['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION
    config_dict['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    config_dict['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    config_dict['AWS_ENDPOINT_URL'] = AWS_ENDPOINT_URL
    config_dict['AZURE_STORAGE_CONTAINER_NAME'] = AZURE_STORAGE_CONTAINER_NAME
    config_dict['AZURE_STORAGE_CONNECTION_STRING'] = AZURE_STORAGE_CONNECTION_STRING
    config_dict['GCS_BUCKET_NAME'] = GCS_BUCKET_NAME

    return config_dict
