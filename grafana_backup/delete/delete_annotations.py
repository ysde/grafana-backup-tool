import time
from grafana_backup.dashboardApi import search_annotations, delete_annotation
from grafana_backup.commons import print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    get_all_annotations_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print)
    print_horizontal_line()


def get_all_annotations_and_delete(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    now = int(round(time.time() * 1000))
    one_month_in_ms = 31 * 24 * 60 * 60 * 1000

    ts_to = now
    ts_from = now - one_month_in_ms
    thirteen_months_retention = (now - (13 * one_month_in_ms))

    while ts_from > thirteen_months_retention:
        status_code_and_content = search_annotations(grafana_url, ts_from, ts_to, http_get_headers, verify_ssl, client_cert, debug)
        if status_code_and_content[0] == 200:
            annotations = status_code_and_content[1]
            print("There are {0} annotations:".format(len(annotations)))
            for annotation in annotations:
                status = delete_annotation(annotation['id'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
                if status == 200:
                    print("annotation:{0} is deleted".format(annotation['id']))
                else:
                    print("deleting of annotation {0} failed with: {1}".format(annotation['id'], status))
        else:
            print("query annotation failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                          status_code_and_content[1]))

        ts_to = ts_from
        ts_from = ts_from - one_month_in_ms
