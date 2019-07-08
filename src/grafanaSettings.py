import os

GRAFANA_URL = os.getenv('GRAFANA_URL', 'http://localhost:3000')
TOKEN = os.getenv('GRAFANA_TOKEN', 'eyJrIjoiSkQ5NkdvWllHdnVNdlVhWUV3Tm5LSGc4NG53UFdSTjQiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')
HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}
SEARCH_API_LIMIT = 10000
DEBUG = True
VERIFY_SSL = False
