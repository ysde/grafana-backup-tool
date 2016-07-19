import os

grafana_url = os.getenv('GRAFANA_URL', 'http://localhost:3000')
token = os.getenv('GRAFANA_TOKEN', '')
http_get_headers = {'Authorization': 'Bearer ' + token}
http_post_headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

