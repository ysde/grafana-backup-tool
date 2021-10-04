import sys
import json
from grafana_backup.api_checks import main as api_checks
from grafana_backup.dashboardApi import set_user_role


def main(args, settings):
    users_file = args.get('<users_filename>', None)
    print("got users_file {0}".format(users_file))

    (status, json_resp, uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        sys.exit(1)

    debug = settings.get('DEBUG')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')

    with open(users_file, 'r') as f:
        data = f.read()

    users = json.loads(data)
    print(users)

    for user in users:
        if user['role'] == 'Editor':
            (status, content) = set_user_role(user['userId'], 'Editor', grafana_url, http_post_headers, verify_ssl, client_cert, debug)
            print("changed user {0} to Editor".format(user['login']))

            if status != 200:
                print("changing role of user {0} failed with {1}".format(user['login'], status))
