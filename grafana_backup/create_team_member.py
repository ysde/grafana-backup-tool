import json
from grafana_backup.dashboardApi import create_team_member


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    team_member = json.loads(data)
    user = json.dumps({"userId": team_member['userId']})
    result = create_team_member(user, team_member['teamId'], grafana_url, http_post_headers, verify_ssl,
                                    client_cert, debug)
    print("create team member: {0}, status: {1}, msg: {2}".format(team_member['name'], result[0], result[1]))
