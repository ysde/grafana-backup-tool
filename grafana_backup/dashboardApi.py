import requests, json, re
from grafana_backup.commons import log_response


def health_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/health'.format(grafana_url)
    print("grafana health: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def auth_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/auth/keys'.format(grafana_url)
    print("grafana auth check: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def search_dashboard(page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/search/?type=dash-db&limit={1}&page={2}'.format(grafana_url, limit, page)
    print("search dashboard in grafana: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def get_dashboard(board_uri, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/dashboards/{1}'.format(grafana_url, board_uri)
    print("query dashboard uri: {0}".format(url))
    (status_code, content) = send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)
    return (status_code, content)


def search_alert_channels(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    url = '{0}/api/alert-notifications'.format(grafana_url)
    print("search alert channels in grafana: {0}".format(url))
    return send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug)


def create_alert_channel(payload, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    return send_grafana_post('{0}/api/alert-notifications'.format(grafana_url), payload, http_post_headers, verify_ssl, client_cert, debug)


def delete_dashboard(board_uri, grafana_url, http_post_headers):
    r = requests.delete('{0}/api/dashboards/db/{1}'.format(grafana_url, board_uri), headers=http_post_headers)
    return int(r.status_code)


def create_dashboard(payload, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    return send_grafana_post('{0}/api/dashboards/db'.format(grafana_url), payload, http_post_headers, verify_ssl, client_cert, debug)


def search_datasource(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    print("search datasources in grafana:")
    return send_grafana_get('{0}/api/datasources'.format(grafana_url), http_get_headers, verify_ssl, client_cert, debug)


def create_datasource(payload, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    return send_grafana_post('{0}/api/datasources'.format(grafana_url), payload, http_post_headers, verify_ssl, client_cert, debug)


def search_folders(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    print("search folder in grafana:")
    return send_grafana_get('{0}/api/search/?type=dash-folder'.format(grafana_url), http_get_headers, verify_ssl, client_cert, debug)


def get_folder(uid, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = send_grafana_get('{0}/api/folders/{1}'.format(grafana_url, uid), http_get_headers, verify_ssl, client_cert, debug)
    print("query folder:{0}, status:{1}".format(uid, status_code))
    return (status_code, content)


def get_folder_id_from_old_folder_url(folder_url, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    if folder_url != "":
        # Get folder uid
        matches = re.search('dashboards\/[A-Za-z0-9]{1}\/(.*)\/.*', folder_url)
        uid = matches.group(1)

        response = get_folder(uid, grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        if isinstance(response[1],dict):
            folder_data = response[1]
        else:
            folder_data = json.loads(response[1])
        return folder_data['id']
    return 0


def create_folder(payload, grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    return send_grafana_post('{0}/api/folders'.format(grafana_url), payload, http_post_headers, verify_ssl, client_cert, debug)


def send_grafana_get(url, http_get_headers, verify_ssl, client_cert, debug):
    r = requests.get(url, headers=http_get_headers, verify=verify_ssl, cert=client_cert)
    if debug:
        log_response(r)
    return (r.status_code, r.json())


def send_grafana_post(url, json_payload, http_post_headers, verify_ssl, client_cert, debug):
    r = requests.post(url, headers=http_post_headers, data=json_payload, verify=verify_ssl, cert=client_cert)
    if debug:
        log_response(r)
    return (r.status_code, r.json())
