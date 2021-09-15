import os
import time
from grafana_backup.dashboardApi import search_annotations
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

    folder_path = '{0}/annotations/{1}'.format(backup_dir, timestamp)
    'annotations_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    get_all_annotations_and_save(folder_path, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print)
    print_horizontal_line()


def save_annotation(file_name, annotation_setting, folder_path, pretty_print):
    file_path = save_json(file_name, annotation_setting, folder_path, 'annotation', pretty_print)
    print("annotation: {0} is saved to {1}".format(file_name, file_path))


def get_all_annotations_and_save(folder_path, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    now = int(round(time.time() * 1000))
    one_month_in_ms = 31 * 24 * 60 * 60 * 1000

    ts_to = now
    ts_from = now - one_month_in_ms
    thirteen_months_retention = (now - (13 * one_month_in_ms))

    while ts_from > thirteen_months_retention:
        status_code_and_content = search_annotations(grafana_url, ts_from, ts_to, http_get_headers, verify_ssl, client_cert, debug)
        if status_code_and_content[0] == 200:
            annotations_batch = status_code_and_content[1]
            print("There are {0} annotations:".format(len(annotations_batch)))
            for annotation in annotations_batch:
                print(annotation)
                save_annotation(str(annotation['id']), annotation, folder_path, pretty_print)
        else:
            print("query annotation failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                          status_code_and_content[1]))

        ts_to = ts_from
        ts_from = ts_from - one_month_in_ms
