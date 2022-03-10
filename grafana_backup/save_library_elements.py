import os
from grafana_backup.dashboardApi import search_library_elements
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

    folder_path = '{0}/library-elements/{1}'.format(backup_dir, timestamp)
    log_file = 'library_elements_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    library_elements = get_all_library_elements_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    get_individual_library_elements_and_save(library_elements, folder_path, log_file, pretty_print)
    print_horizontal_line()


def get_all_library_elements_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_library_elements(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status == 200:
        library_elements = content['result']['elements']
        print("There are {0} library element:".format(len(library_elements)))
        for library_element in library_elements:
            print("name: {0}".format(to_python2_and_3_compatible_string(library_element['name'])))
        return library_elements
    else:
        print("query library elements failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_library_element(channel_name, file_name, alert_channel_setting, folder_path, pretty_print):
    file_path = save_json(file_name, alert_channel_setting, folder_path, 'library_element', pretty_print)
    print("library_element:{0} is saved to {1}".format(channel_name, file_path))


def get_individual_library_elements_and_save(library_elements, folder_path, log_file, pretty_print):
    file_path = folder_path + '/' + log_file
    if library_elements:
        with open(u"{0}".format(file_path), 'w') as f:
            for library_element in library_elements:
                if 'uid' in library_element:
                    library_element_identifier = library_element['uid']
                else:
                    library_element_identifier = library_element['id']

                save_library_element(
                    to_python2_and_3_compatible_string(library_element['name']),
                    to_python2_and_3_compatible_string(str(library_element_identifier)),
                    library_element,
                    folder_path,
                    pretty_print
                )
                f.write('{0}\t{1}\n'.format(to_python2_and_3_compatible_string(str(library_element_identifier)),
                                            to_python2_and_3_compatible_string(library_element['name'])))

