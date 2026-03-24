import json
from grafana_backup.dashboardApi import create_team


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    team = json.loads(data)
    result = create_team(json.dumps(team), grafana_url, http_post_headers, verify_ssl,
                                    client_cert, debug)
    print("create teams: {0}, status: {1}, msg: {2}".format(team['name'], result[0], result[1]))
