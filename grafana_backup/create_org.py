import json
from grafana_backup.dashboardApi import create_org, update_org


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
        org_id = content["id"]

        if (org_id == 1):
            result = update_org(org_id, json.dumps(content), grafana_url, http_post_headers_basic_auth, verify_ssl, client_cert, debug)
            print('update org "{0}" response status: {1}, msg: {2} \n'.format(content.get('name', ''), result[0], result[1]))
        else:
            result = create_org(json.dumps(content), grafana_url, http_post_headers_basic_auth, verify_ssl, client_cert, debug)
            print('create org "{0}" response status: {1}, msg: {2} \n'.format(content.get('name', ''), result[0], result[1]))
    else:
        print('[ERROR] Restoring organizations needs to set GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')
