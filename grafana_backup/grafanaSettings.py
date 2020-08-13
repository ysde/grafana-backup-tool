from grafana_backup.commons import load_config
from datetime import datetime
import os, json


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
    aws_s3_bucket_name = config.get('aws', {}).get('s3_bucket_name', '')
    aws_s3_bucket_key = config.get('aws', {}).get('s3_bucket_key', '')
    aws_default_region = config.get('aws', {}).get('default_region', '')
    aws_access_key_id = config.get('aws', {}).get('access_key_id', '')
    aws_secret_access_key = config.get('aws', {}).get('secret_access_key', '')

    GRAFANA_URL = os.getenv('GRAFANA_URL', grafana_url)
    TOKEN = os.getenv('GRAFANA_TOKEN', grafana_token)
    SEARCH_API_LIMIT = os.getenv('SEARCH_API_LIMIT', grafana_search_api_limit)

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', aws_s3_bucket_name)
    AWS_S3_BUCKET_KEY = os.getenv('AWS_S3_BUCKET_KEY', aws_s3_bucket_key)
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', aws_default_region)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', aws_access_key_id)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', aws_secret_access_key)

    DEBUG = os.getenv('DEBUG', debug)
    if isinstance(DEBUG, str):
        DEBUG = json.loads(DEBUG.lower()) # convert environment variable string to bool

    VERIFY_SSL = os.getenv('VERIFY_SSL', verify_ssl)
    if isinstance(VERIFY_SSL, str):
        VERIFY_SSL = json.loads(VERIFY_SSL.lower()) # convert environment variable string to bool

    CLIENT_CERT = os.getenv('CLIENT_CERT', client_cert)

    BACKUP_DIR = os.getenv('BACKUP_DIR', backup_dir)

    EXTRA_HEADERS = dict(h.split(':') for h in os.getenv('GRAFANA_HEADERS', '').split(',') if 'GRAFANA_HEADERS' in os.environ)

    HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
    HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}

    for k,v in EXTRA_HEADERS.items():
        HTTP_GET_HEADERS.update({k: v})
        HTTP_POST_HEADERS.update({k: v})

    TIMESTAMP = datetime.today().strftime('%Y%m%d%H%M')

    config_dict['GRAFANA_URL'] = GRAFANA_URL
    config_dict['TOKEN'] = TOKEN
    config_dict['SEARCH_API_LIMIT'] = SEARCH_API_LIMIT
    config_dict['DEBUG'] = DEBUG
    config_dict['VERIFY_SSL'] = VERIFY_SSL
    config_dict['CLIENT_CERT'] = CLIENT_CERT
    config_dict['BACKUP_DIR'] = BACKUP_DIR
    config_dict['EXTRA_HEADERS'] = EXTRA_HEADERS
    config_dict['HTTP_GET_HEADERS'] = HTTP_GET_HEADERS
    config_dict['HTTP_POST_HEADERS'] = HTTP_POST_HEADERS
    config_dict['TIMESTAMP'] = TIMESTAMP
    config_dict['AWS_S3_BUCKET_NAME'] = AWS_S3_BUCKET_NAME
    config_dict['AWS_S3_BUCKET_KEY'] = AWS_S3_BUCKET_KEY
    config_dict['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION
    config_dict['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    config_dict['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    return config_dict
