import json
import urllib.parse

from grafana_backup.dashboardApi import create_team_member, get_user_by_email_or_username


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    http_get_headers_basic_auth = settings.get('HTTP_GET_HEADERS_BASIC_AUTH')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    if http_get_headers_basic_auth:
        with open(file_path, 'r') as f:
            data = f.read()

        team_member = json.loads(data)
        # A Team-Membership is a connection between a user and a team. However, userIds are not unique across Grafana
        # instances. Therefore, we need to first find the user id by the email.
        user_id = get_user_by_email_or_username(urllib.parse.quote(team_member['email']), grafana_url,
                                                http_get_headers_basic_auth, verify_ssl, client_cert, debug)
        if 200 != user_id[0]:
            user_id = get_user_by_email_or_username(urllib.parse.quote(team_member['name']), grafana_url,
                                                    http_get_headers_basic_auth, verify_ssl, client_cert, debug)

        if 200 != user_id[0]:
            return

        user = json.dumps({"userId": user_id[1]['id']})
        result = create_team_member(user, team_member['teamId'], grafana_url, http_post_headers, verify_ssl,
                                        client_cert, debug)
        print("create team member: {0}, status: {1}, msg: {2}".format(team_member['name'], result[0], result[1]))
    else:
        print('[ERROR] Restoring team members needs to set GRAFANA_ADMIN_ACCOUNT and GRAFANA_ADMIN_PASSWORD first. \n')