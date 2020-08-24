import json
from grafana_backup.dashboardApi import get_folder_id_from_old_folder_url, create_org


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    basic_auth = settings.get('GRAFANA_BASIC_AUTH')
    if basic_auth:
        http_post_headers.update({'Authorization': 'Basic {0}'.format(basic_auth)})

        with open(file_path, 'r') as f:
            data = f.read()

        content = json.loads(data)

        result = create_org(json.dumps(content), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        print('create org "{0}" response status: {0}, msg: {1} \n'.format(content.get('name', ''), result[0], result[1]))
    else:
        print('[ERROR] Restoring organizations needs to set GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')
