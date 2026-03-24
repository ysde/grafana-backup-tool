import os
import json
from grafana_backup.dashboardApi import search_folders, get_folder, get_folder_permissions
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, save_json


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')
    uid_support = settings.get('DASHBOARD_UID_SUPPORT')

    folder_path = '{0}/folders/{1}'.format(backup_dir, timestamp)
    log_file = 'folders_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    folders = get_all_folders_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    print_horizontal_line()
    get_individual_folder_setting_and_save(folders, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
    print_horizontal_line()


def get_all_folders_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    status_and_content_of_all_folders = search_folders(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    status = status_and_content_of_all_folders[0]
    content = status_and_content_of_all_folders[1]
    if status == 200:
        folders = content
        print("There are {0} folders:".format(len(content)))
        for folder in folders:
            print("name: {0}".format(to_python2_and_3_compatible_string(folder['title'])))
        return folders
    else:
        print("get folders failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_folder_setting(folder_name, file_name, folder_settings, folder_permissions, folder_path, pretty_print):
    file_path = save_json(file_name, folder_settings, folder_path, 'folder', pretty_print)
    print("folder:{0} are saved to {1}".format(folder_name, file_path))
    # NOTICE: The 'folder_permission' file extension had the 's' removed to work with the magical dict logic in restore.py...
    file_path = save_json(file_name,  folder_permissions, folder_path, 'folder_permission', pretty_print)
    print("folder permissions:{0} are saved to {1}".format(folder_name, file_path))


def get_individual_folder_setting_and_save(folders, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    file_path = folder_path + '/' + log_file
    with open(u"{0}".format(file_path), 'w+') as f:
        for folder in folders:
            if uid_support:
                folder_uri = "uid/{0}".format(folder['uid'])
            else:
                folder_uri = folder['uri']

            (status_folder_settings, content_folder_settings) = get_folder(folder['uid'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
            (status_folder_permissions, content_folder_permissions) = get_folder_permissions(folder['uid'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)

            if status_folder_settings == 200 and status_folder_permissions == 200:
                save_folder_setting(
                    to_python2_and_3_compatible_string(folder['title']),
                    folder_uri,
                    content_folder_settings,
                    content_folder_permissions,
                    folder_path,
                    pretty_print
                )
                f.write('{0}\t{1}\n'.format(folder_uri, to_python2_and_3_compatible_string(folder['title'])))
