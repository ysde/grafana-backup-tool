import os
from grafana_backup.dashboardApi import search_users, get_user_org, get_user
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, save_json


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    limit = settings.get('SEARCH_API_LIMIT')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers_basic_auth = settings.get('HTTP_GET_HEADERS_BASIC_AUTH')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    if http_get_headers_basic_auth:
        folder_path = '{0}/users/{1}'.format(backup_dir, timestamp)
        log_file = 'users_{0}.txt'.format(timestamp)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_users(folder_path, log_file, limit, grafana_url, http_get_headers_basic_auth, verify_ssl, client_cert, debug, pretty_print)
    else:
        print('[ERROR] Backing up users needs to set ENV GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')
        print_horizontal_line()


def get_all_users(page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_users(page,
                                     limit,
                                     grafana_url,
                                     http_get_headers,
                                     verify_ssl,
                                     client_cert,
                                     debug)
    if status == 200:
        users = content
        print("There are {0} users:".format(len(users)))
        for user in users:
            print('name: {0}'.format(to_python2_and_3_compatible_string(user['name'])))
        return users
    else:
        print("get users failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_user_info(user_name, file_name, user_data, folder_path, pretty_print):
    file_path = save_json(file_name, user_data, folder_path, 'user', pretty_print)
    print("user: {0} -> saved to: {1}".format(user_name, file_path))


def get_individual_user_and_save(users, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert,
                                 debug, pretty_print):
    file_path = folder_path + '/' + log_file
    if users:
        with open(u"{0}".format(file_path), 'w') as f:
            for user in users:
                (status, content) = get_user(user['id'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
                if status == 200:
                    user.update(content)

                (status, content) = get_user_org(user['id'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
                if status == 200:
                    user.update({'orgs': content})

                save_user_info(
                    to_python2_and_3_compatible_string(user['name']),
                    str(user['id']),
                    user,
                    folder_path,
                    pretty_print
                )
                f.write('{0}\t{1}\n'.format(user['id'], to_python2_and_3_compatible_string(user['name'])))


def save_users(folder_path, log_file, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    current_page = 1
    users = get_all_users(current_page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    print_horizontal_line()
    get_individual_user_and_save(users, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert,
                                 debug, pretty_print)
    print_horizontal_line()
