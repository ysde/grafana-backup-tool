from grafana_backup.dashboardApi import search_folders, delete_folder
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')
    uid_support = settings.get('DASHBOARD_UID_SUPPORT')

    folders = get_all_folders_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    print_horizontal_line()
    get_individual_folder_setting_and_save(folders, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
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


def get_individual_folder_setting_and_save(folders, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    for folder in folders:
        status = delete_folder(folder['uid'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)

        if status == 200:
            print("deleted folder {0}".format(folder))
        else:
            print("failed to delete folder {0} with {1}".format(folder, status))
