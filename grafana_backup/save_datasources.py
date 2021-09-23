import os
from grafana_backup.dashboardApi import search_datasource
from grafana_backup.commons import print_horizontal_line, save_json


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    folder_path = '{0}/datasources/{1}'.format(backup_dir, timestamp)
    'datasources_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    get_all_datasources_and_save(folder_path, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print)
    print_horizontal_line()


def save_datasource(file_name, datasource_setting, folder_path, pretty_print):
    file_path = save_json(file_name, datasource_setting, folder_path, 'datasource', pretty_print)
    print("datasource:{0} is saved to {1}".format(file_name, file_path))


def get_all_datasources_and_save(folder_path, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    status_code_and_content = search_datasource(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status_code_and_content[0] == 200:
        datasources = status_code_and_content[1]
        print("There are {0} datasources:".format(len(datasources)))
        for datasource in datasources:
            print(datasource)
            save_datasource(datasource['name'], datasource, folder_path, pretty_print)
    else:
        print("query datasource failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                      status_code_and_content[1]))
