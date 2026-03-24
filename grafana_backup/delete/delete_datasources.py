from grafana_backup.dashboardApi import search_datasource, delete_datasource_by_uid, delete_datasource_by_id
from grafana_backup.commons import print_horizontal_line


def main(args, settings):
    debug = settings.get('DEBUG')
    verify_ssl = settings.get('VERIFY_SSL')
    grafana_url = settings.get('GRAFANA_URL')
    client_cert = settings.get('CLIENT_CERT')
    uid_support = settings.get('DATASOURCE_UID_SUPPORT')
    pretty_print = settings.get('PRETTY_PRINT')
    http_get_headers = settings.get('HTTP_POST_HEADERS')

    get_all_datasources_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
    print_horizontal_line()


def get_all_datasources_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    status_code_and_content = search_datasource(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status_code_and_content[0] == 200:
        datasources = status_code_and_content[1]
        print("There are {0} datasources:".format(len(datasources)))
        for datasource in datasources:
            print(datasource)
            if uid_support:
                status = delete_datasource_by_uid(datasource['uid'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
            else:
                status = delete_datasource_by_id(datasource['id'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)

            if status == 200:
                print("datasource:{0} is deleted".format(datasource['name']))
            else:
                print("deleting of datasource {0} failed with: {1}".format(datasource['name'], status))
    else:
        print("query datasource failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                      status_code_and_content[1]))
