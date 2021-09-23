import json
from grafana_backup.dashboardApi import create_user, add_user_to_org


def main(args, settings, file_path):
    """
    Cannot get user's password, use default password instead
    """
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers_basic_auth = settings.get('HTTP_POST_HEADERS_BASIC_AUTH')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    default_password = settings.get('default_password', '00000000')
    if http_post_headers_basic_auth:
        with open(file_path, 'r') as f:
            data = f.read()

        user = json.loads(data)
        user.update({'password': default_password})

        result = create_user(json.dumps(user), grafana_url, http_post_headers_basic_auth, verify_ssl, client_cert, debug)
        print('create user "{0}" response status: {1}, msg: {2} \n'.format(user.get('login', ''), result[0], result[1]))

        if result[0] == 200:
            for org in user.get('orgs', []):
                org_payload = {
                    "loginOrEmail": user.get('login', 'email'),
                    "role": org.get('role', 'Viewer')
                }
                result = add_user_to_org(org.get('orgId'), json.dumps(org_payload), grafana_url, http_post_headers_basic_auth, verify_ssl, client_cert, debug)
                print('add user "{0}" to org: {1} response status: {2}, msg: {3}'.format(user.get('login', ''), org.get('name', ''), result[0], result[1]))
    else:
        print('[ERROR] Restoring users needs to set GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')
