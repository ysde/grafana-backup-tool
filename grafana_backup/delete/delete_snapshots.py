from grafana_backup.dashboardApi import search_snapshot, delete_snapshot
from grafana_backup.commons import print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    get_all_snapshots_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print)
    print_horizontal_line()


def get_all_snapshots_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    status_code_and_content = search_snapshot(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status_code_and_content[0] == 200:
        snapshots = status_code_and_content[1]
        print("There are {0} snapshots:".format(len(snapshots)))
        for snapshot in snapshots:
            print(snapshot)
            status = delete_snapshot(snapshot['key'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)

            if status == 200:
                print("deleted snapshot {0}".format(snapshot['name']))
            else:
                print("failed to delete snapshot {0}, with {1}".format(snapshot['name'], status))

    else:
        print("query snapshot failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                    status_code_and_content[1]))
