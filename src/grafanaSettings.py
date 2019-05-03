import os

grafana_url = os.getenv('GRAFANA_URL', 'http://localhost:3000')
token = os.getenv('GRAFANA_TOKEN', 'eyJrIjoidUhaU2ZQQndrWFN3RTVkUnVOQkRka1JoaG9KWFFObEgiLCJuIjoiYWRtaW4iLCJpZCI6MX0=')
http_get_headers = {'Authorization': 'Bearer ' + token}
http_post_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
search_api_limit = 100000
debug = True
verifySSL = False
