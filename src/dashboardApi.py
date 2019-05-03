import requests, json, re
from grafanaSettings import *
from commons import *

def search_dashboard():
    print("search dashboard in grafana:")
    return send_grafana_get(grafana_url + '/api/search/?type=dash-db&limit={0}'.format(search_api_limit))
    

def get_dashboard(board_uri):
    (status_code, content) = send_grafana_get(grafana_url + "/api/dashboards/{0}".format(board_uri))
    print("query dashboard uri: {0}, status: {1}".format(board_uri, status_code))
    return (status_code, content)

def delete_dashboard(board_uri):
    r = requests.delete(grafana_url + "/api/dashboards/db/{0}".format(board_uri), headers=http_post_headers)
    return int(status_code)

def create_dashboard(payload):
    return send_grafana_post(grafana_url + '/api/dashboards/db', payload)

def search_datasource():
    print("search datasources in grafana:")
    return send_grafana_get(grafana_url + '/api/datasources')

def create_datasource(payload):
    return send_grafana_post(grafana_url + '/api/datasources', payload)

def search_folders():
    print("search folder in grafana:")
    return send_grafana_get(grafana_url + '/api/search/?type=dash-folder')

def get_folder(uid):
    (status_code, content) = send_grafana_get(grafana_url + "/api/folders/{0}".format(uid))
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
    return send_grafana_post(grafana_url + '/api/folders', payload)

def send_grafana_get(url):
    r = requests.get(url, headers=http_get_headers, verify=verifySSL)
    if debug:
        log_response(r)
    return (r.status_code, r.json())

def send_grafana_post(url, json_payload):
    r = requests.post(url, headers=http_post_headers, data=json_payload, verify=verifySSL)
    if debug:
        log_response(r)
    return (r.status_code, r.json())
