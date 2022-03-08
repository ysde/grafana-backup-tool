from grafana_backup.dashboardApi import search_library_elements
from grafana_backup.dashboardApi import delete_library_element
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    library_elements = get_all_library_elements_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert,
                                                           debug)
    get_individual_library_element_and_delete(library_elements, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                              client_cert, debug)
    print_horizontal_line()


def get_all_library_elements_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_library_elements(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status == 200:
        library_elements = content['result']['elements']
        print("There are {0} library elements:".format(len(library_elements)))
        for library_element in library_elements:
            print("name: {0}".format(to_python2_and_3_compatible_string(library_element['name'])))
        return library_elements
    else:
        print("query library elements failed, status: {0}, msg: {1}".format(status, content))
        return []


def get_individual_library_element_and_delete(library_elements, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                              client_cert, debug):
    if library_elements:
        for library_element in library_elements:
            status = delete_library_element(library_element['uid'], grafana_url, http_get_headers, verify_ssl,
                                            client_cert, debug)
            library_element_name = to_python2_and_3_compatible_string(library_element['name'])
            if status == 200:
                print("library_element:{0} is deleted".format(library_element_name))
            else:
                print("deleting library_element {0} failed with {1}".format(library_element_name, status))
