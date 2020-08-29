import json
from grafana_backup.dashboardApi import get_folder_id_from_old_folder_url, create_org


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers_basic_auth = settings.get('HTTP_POST_HEADERS_BASIC_AUTH')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    if http_post_headers_basic_auth:
        with open(file_path, 'r') as f:
            data = f.read()

        content = json.loads(data)

        result = create_org(json.dumps(content), grafana_url, http_post_headers_basic_auth, verify_ssl, client_cert, debug)
        print('create org "{0}" response status: {1}, msg: {2} \n'.format(content.get('name', ''), result[0], result[1]))
    else:
        print('[ERROR] Restoring organizations needs to set GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')
