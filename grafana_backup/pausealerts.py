import os
import sys
from grafana_backup.commons import save_json
from grafana_backup.api_checks import main as api_checks
from grafana_backup.dashboardApi import search_alerts, pause_alert


def main(args, settings):
    (status, json_resp, uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        print("server status is not ok: {0}".format(json_resp))
        sys.exit(1)

    settings.update({'UID_SUPPORT': uid_support})
    settings.update({'PAGING_SUPPORT': paging_support})

    debug = settings.get('DEBUG')
    timestamp = settings.get('TIMESTAMP')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    grafana_url = settings.get('GRAFANA_URL')
    pretty_print = settings.get('PRETTY_PRINT')
    http_get_headers = settings.get('HTTP_POST_HEADERS')

    folder_path = 'alert_status/{0}'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    alerts = get_all_alerts(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    file_path = save_json("alerts.json", alerts, folder_path, 'alerts', pretty_print)
    print("alerts have been saved to {0}".format(file_path))

    for alert in alerts:
        (status, content) = pause_alert(alert['id'], grafana_url, http_get_headers, verify_ssl, client_cert, debug)
        if status != 200:
            print("pausing of alert {0} failed with {1}".format(alert['name'], status))


def get_all_alerts(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status_code, content) = search_alerts(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status_code == 200:
        return content
    else:
        print("got status {0} when trying to get alerts".format(status_code))
        exit(1)
