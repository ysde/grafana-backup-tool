import requests, json, re
import importlib
from commons import log_response, to_python2_and_3_compatible_string


def import_grafana_settings(settings_file_name):
    # On import, load the correct grafana settings from the 'conf' module/directory
    conf_module_name = "conf"
    mdl = importlib.import_module('{0}.{1}'.format(to_python2_and_3_compatible_string(str(conf_module_name)),
                                                   to_python2_and_3_compatible_string(str(settings_file_name))))

    # is there an __all__?  if so respect it
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        # otherwise we import all names that don't begin with _
        names = [x for x in mdl.__dict__ if not x.startswith("_")]

    # now update the globals of this module
    settings_dict = {k: getattr(mdl, k) for k in names}
    globals().update(settings_dict)

    return settings_dict

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
