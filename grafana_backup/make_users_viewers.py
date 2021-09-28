import os
import sys
from grafana_backup.commons import save_json
from grafana_backup.api_checks import main as api_checks
from grafana_backup.dashboardApi import set_user_role, get_users


def main(args, settings):
    (status, json_resp, uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        print("server status is not ok: {0}".format(json_resp))
        sys.exit(1)

    settings.update({'UID_SUPPORT': uid_support})
    settings.update({'PAGING_SUPPORT': paging_support})

    debug = settings.get('DEBUG')
    timestamp = settings.get('TIMESTAMP')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    grafana_url = settings.get('GRAFANA_URL')
    pretty_print = settings.get('PRETTY_PRINT')
    http_post_headers = settings.get('HTTP_POST_HEADERS')

    folder_path = 'user_permissions/{0}'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    users = get_all_users(grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    file_path = save_json("users.json", users, folder_path, 'users', pretty_print)
    print("users have been saved to {0}".format(file_path))

    for user in users:
        if user['role'] != 'Admin':
            (status, content) = set_user_role(user['userId'], 'Viewer', grafana_url, http_post_headers, verify_ssl, client_cert, debug)
            print("changed user {0} to Viewer".format(user['login']))

            if status != 200:
                print("changing role of user {0} failed with {1}".format(user['login'], status))


def get_all_users(grafana_url, http_post_headers, verify_ssl, client_cert, debug):
    (status_code, content) = get_users(grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    if status_code == 200:
        return content
    else:
        print("got status {0} when trying to get users".format(status_code))
        exit(1)
