import sys
import json
from grafana_backup.api_checks import main as api_checks
from grafana_backup.dashboardApi import unpause_alert


def main(args, settings):
    alerts_file = args.get('<alerts_filename>', None)
    print("got alerts_file {0}".format(alerts_file))

    (status, json_resp, uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        sys.exit(1)

    debug = settings.get('DEBUG')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')

    with open(alerts_file, 'r') as f:
        data = f.read()

    alerts = json.loads(data)
    print(alerts)

    for alert in alerts:
        if alert['state'] != 'paused':
            result = unpause_alert(alert['id'], grafana_url, http_post_headers, verify_ssl, client_cert, debug)
            if result[0] != 200:
                print("failed to unpause alert: {0} - {1} with {2}".format(alert['id'], alert['name'], result[0]))
            print("unpausing alert: {0} - {1} with previous state: {2}".format(alert['id'], alert['name'], result[0]))
        else:
            print("keeping alert {0} - {1} paused".format(alert['id'], alert['name']))
