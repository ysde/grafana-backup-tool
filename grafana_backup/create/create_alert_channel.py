import json
from grafana_backup.dashboardApi import create_alert_channel


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    alert_channel = json.loads(data)
    result = create_alert_channel(json.dumps(alert_channel), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    print("create alert_channel: {0}, status: {1}, msg: {2}".format(alert_channel['name'], result[0], result[1]))
