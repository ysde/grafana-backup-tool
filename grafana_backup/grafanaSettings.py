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
    backup_dir = config.get('general', {}).get('backup_dir', '_OUTPUT_')

    GRAFANA_URL = os.getenv('GRAFANA_URL', grafana_url)
    TOKEN = os.getenv('GRAFANA_TOKEN', grafana_token)
    SEARCH_API_LIMIT = os.getenv('SEARCH_API_LIMIT', grafana_search_api_limit)

    DEBUG = os.getenv('DEBUG', debug)
    if isinstance(DEBUG, str):
        DEBUG = json.loads(DEBUG.lower()) # convert environment variable string to bool

    VERIFY_SSL = os.getenv('VERIFY_SSL', verify_ssl)
    if isinstance(VERIFY_SSL, str):
        VERIFY_SSL = json.loads(VERIFY_SSL.lower()) # convert environment variable string to bool

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
    config_dict['BACKUP_DIR'] = BACKUP_DIR
    config_dict['EXTRA_HEADERS'] = EXTRA_HEADERS
    config_dict['HTTP_GET_HEADERS'] = HTTP_GET_HEADERS
    config_dict['HTTP_POST_HEADERS'] = HTTP_POST_HEADERS
    config_dict['TIMESTAMP'] = TIMESTAMP

    return config_dict
