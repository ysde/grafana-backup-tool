import requests, json, re
from grafanaSettings import *
from commons import *

def health_check():
    url = GRAFANA_URL + '/api/health'
    print("grafana health: {0}".format(url))
    return send_grafana_get(url)

def search_dashboard(page, limit):
    url = GRAFANA_URL + '/api/search/?type=dash-db&limit={0}&page={1}'.format(limit, page)
    print("search dashboard in grafana: {0}".format(url))
    return send_grafana_get(url)

def get_dashboard(board_uri):
    url = GRAFANA_URL + "/api/dashboards/{0}".format(board_uri)
    print("query dashboard uri: {0}".format(url))
    (status_code, content) = send_grafana_get(url)
    return (status_code, content)

def search_alert_channels():
    url = GRAFANA_URL + '/api/alert-notifications'
    print("search alert channels in grafana: {0}".format(url))
    return send_grafana_get(url)

def create_alert_channel(payload):
    return send_grafana_post(GRAFANA_URL + '/api/alert-notifications', payload)
    

def delete_dashboard(board_uri):
    r = requests.delete(GRAFANA_URL + "/api/dashboards/db/{0}".format(board_uri), headers=HTTP_POST_HEADERS)
    return int(status_code)

def create_dashboard(payload):
    return send_grafana_post(GRAFANA_URL + '/api/dashboards/db', payload)

def search_datasource():
    print("search datasources in grafana:")
    return send_grafana_get(GRAFANA_URL + '/api/datasources')

def create_datasource(payload):
    return send_grafana_post(GRAFANA_URL + '/api/datasources', payload)

def search_folders():
    print("search folder in grafana:")
    return send_grafana_get(GRAFANA_URL + '/api/search/?type=dash-folder')

def get_folder(uid):
    (status_code, content) = send_grafana_get(GRAFANA_URL + "/api/folders/{0}".format(uid))
    print("query folder:{0}, status:{1}".format(uid, status_code))
    return (status_code, content)

def get_folder_id_from_old_folder_url(folder_url):
    if folder_url != "":
        # Get folder uid
        matches = re.search('dashboards\/[A-Za-z0-9]{1}\/(.*)\/.*', folder_url)
        uid = matches.group(1)

        response = get_folder(uid)
        if isinstance(response[1],dict):
            folder_data = response[1] 
        else:
            folder_data = json.loads(response[1])
        return folder_data['id']
    return 0

def create_folder(payload):
    return send_grafana_post(GRAFANA_URL + '/api/folders', payload)

def send_grafana_get(url):
    r = requests.get(url, headers=HTTP_GET_HEADERS, verify=VERIFY_SSL)
    if DEBUG:
        log_response(r)
    return (r.status_code, r.json())

def send_grafana_post(url, json_payload):
    r = requests.post(url, headers=HTTP_POST_HEADERS, data=json_payload, verify=VERIFY_SSL)
    if DEBUG:
        log_response(r)
    return (r.status_code, r.json())
