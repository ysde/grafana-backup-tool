import requests, json, re
from grafanaSettings import *
from commons import *

def search_dashboard():
    print("search dashboard in grafana:")
    r = send_grafana_get(grafana_url + '/api/search/?type=dash-db&limit={0}'.format(search_api_limit))
    return (r.status_code, r.content.decode('utf8'))

def get_dashboard(board_uri):
    r = send_grafana_get(grafana_url + "/api/dashboards/{0}".format(board_uri))
    status_code = r.status_code
    content = r.content.decode('utf8')
    print("query dashboard uri: {0}, status: {1}".format(board_uri, status_code))
    return (status_code, content)

def delete_dashboard(board_uri):
    r = requests.delete(grafana_url + "/api/dashboards/db/{0}".format(board_uri), headers=http_post_headers)
    return int(status_code)

def create_dashboard(payload):
    r = send_grafana_post(grafana_url + '/api/dashboards/db', payload)
    return (r.status_code, r.content.decode('utf8'))

def search_datasource():
    print("search datasources in grafana:")
    r = send_grafana_get(grafana_url + '/api/datasources')
    return (r.status_code, r.content.decode('utf8'))

def create_datasource(payload):
    r = send_grafana_post(grafana_url + '/api/datasources', payload)
    return (r.status_code, r.content.decode('utf8'))

def search_folders():
    print("search folder in grafana:")
    r = send_grafana_get(grafana_url + '/api/search/?type=dash-folder')
    return (r.status_code, r.content.decode('utf8'))

def get_folder(uid):
    r = send_grafana_get(grafana_url + "/api/folders/{0}".format(uid))
    status_code = r.status_code
    content = r.content.decode('utf8')
    print("query folder:{0}, status:{1}".format(uid, status_code))
    return (status_code, content)

def get_folder_id_from_old_folder_url(folder_url):
    if folder_url != "":
        # Get folder uid
        matches = re.search('dashboards\/[A-Za-z0-9]{1}\/(.*)\/.*', folder_url)
        uid = matches.group(1)

        response = get_folder(uid)
        folder_data = json.loads(response[1])

        return folder_data['id']

    return 0

def create_folder(payload):
    r = send_grafana_post(grafana_url + '/api/folders', payload)
    status_code = r.status_code
    return (r.status_code, r.content.decode('utf8'))

def send_grafana_get(url):
    r = requests.get(url, headers=http_get_headers)
    if debug:
        log_response(r)
    return r

def send_grafana_post(url, json_payload):
    r = requests.post(url, headers=http_post_headers, data=json_payload)
    if debug:
        log_response(r)
    return r
