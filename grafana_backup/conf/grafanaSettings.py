from grafana_backup.commons import load_config
from grafana_backup.constants import CONFIG_PATH
from pathlib import Path
from datetime import datetime
import os, json


if Path(CONFIG_PATH).is_file():
    config = load_config(CONFIG_PATH)
else:
    config = load_config('{0}/grafana-backup.example.yml'.format(os.path.dirname(__file__)))

grafana_url = config.get('grafana', {}).get('url', 'http://localhost:3000')
grafana_token = config.get('grafana', {}).get('token', 'eyJrIjoiSkQ5NkdvWllHdnVNdlVhWUV3Tm5LSGc4NG53UFdSTjQiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')
grafana_search_api_limit = config.get('grafana', {}).get('search_api_limit', 5000)

debug = config.get('main', {}).get('debug', True)
verify_ssl = config.get('main', {}).get('verify_ssl', False)
backup_dir = config.get('main', {}).get('backup_dir', '_OUTPUT_')

GRAFANA_URL = os.getenv('GRAFANA_URL', grafana_url)
TOKEN = os.getenv('GRAFANA_TOKEN', grafana_token)
SEARCH_API_LIMIT = os.getenv('SEARCH_API_LIMIT', grafana_search_api_limit)

DEBUG = os.getenv('DEBUG', debug)
if isinstance(DEBUG, str):
    DEBUG = json.loads(DEBUG.lower())

VERIFY_SSL = os.getenv('VERIFY_SSL', verify_ssl)
if isinstance(VERIFY_SSL, str):
    VERIFY_SSL = json.loads(VERIFY_SSL.lower())

BACKUP_DIR = os.getenv('BACKUP_DIR', backup_dir)

EXTRA_HEADERS = dict(h.split(':') for h in os.getenv('GRAFANA_HEADERS', '').split(',') if 'GRAFANA_HEADERS' in os.environ)

HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}

for k,v in EXTRA_HEADERS.items():
    HTTP_GET_HEADERS.update({k: v})
    HTTP_POST_HEADERS.update({k: v})

timestamp = datetime.today().strftime('%Y%m%d%H%M')
