import json
from grafana_backup.dashboardApi import update_folder_permissions


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    folder_permissions = json.loads(data)
    if folder_permissions:
        result = update_folder_permissions(folder_permissions, grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        print("update folder permissions {0}, status: {1}, msg: {2}\n".format(folder_permissions[0].get('title', ''), result[0], result[1]))
