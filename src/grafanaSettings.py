import os

GRAFANA_URL = os.getenv('GRAFANA_URL', 'https://grafana.dev-1.eu-west-1.infra.yager-development.com')
TOKEN = os.getenv('GRAFANA_TOKEN',
                  'eyJrIjoiN1lrTExOVDcycEVRWExMeUE5VHFZRng3TVh2MThOUVgiLCJuIjoidGVzdC10b29sLWJhY2t1cCIsImlkIjoxfQ==')
HTTP_GET_HEADERS = {'Authorization': 'Bearer ' + TOKEN}
HTTP_POST_HEADERS = {'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'}
SEARCH_API_LIMIT = 5000
DEBUG = True
VERIFY_SSL = True
