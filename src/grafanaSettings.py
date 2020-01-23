import os

GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3000')
TOKEN = os.getenv('GRAFANA_TOKEN', 'eyJrIjoiSkQ5NkdvWllHdnVNdlVhWUV3Tm5LSGc4NG53UFdSTjQiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')

if 'GRAFANA_HEADERS' in os.environ:
    EXTRA_HEADERS = dict(h.split(':') for h in os.getenv('GRAFANA_HEADERS').split(','))
else:
    EXTRA_HEADERS = {}

HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN, **EXTRA_HEADERS}
HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json', **EXTRA_HEADERS}
SEARCH_API_LIMIT = 5000
DEBUG = True
VERIFY_SSL = False
