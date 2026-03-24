import json
from grafana_backup.commons import to_python2_and_3_compatible_string
from grafana_backup.dashboardApi import get_folder_id, create_dashboard


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    content = json.loads(data)
    content['dashboard']['id'] = None

    payload = {
        'dashboard': content['dashboard'],
        'folderId': get_folder_id(content, grafana_url, http_post_headers, verify_ssl, client_cert, debug),
        'overwrite': True
    }

    result = create_dashboard(json.dumps(payload), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    dashboard_title = to_python2_and_3_compatible_string(content['dashboard'].get('title', ''))
    print("create dashboard {0} response status: {1}, msg: {2} \n".format(dashboard_title, result[0], result[1]))
