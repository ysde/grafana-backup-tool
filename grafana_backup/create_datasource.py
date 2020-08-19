import json
from grafana_backup.dashboardApi import create_datasource


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    datasource = json.loads(data)
    result = create_datasource(json.dumps(datasource), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
    print("create datasource: {0}, status: {1}, msg: {2}".format(datasource['name'], result[0], result[1]))
