import json
from grafana_backup.dashboardApi import get_folder_id_from_old_folder_url, create_dashboard


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    content = json.loads(data)
    content['dashboard']['id'] = None

    payload = {
        'dashboard': content['dashboard'],
        'folderId': get_folder_id_from_old_folder_url(content['meta']['folderUrl']),
        'overwrite': True
    }

    result = create_dashboard(json.dumps(payload), grafana_url, http_post_headers, verify_ssl, debug)
    print("create response status: {0}, msg: {1}".format(result[0], result[1]))
