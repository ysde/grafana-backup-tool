import os
from grafana_backup.dashboardApi import search_teams
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, save_json


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    folder_path = '{0}/teams/{1}'.format(backup_dir, timestamp)
    log_file = 'teams_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    teams = get_all_teams_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    get_individual_teams_and_save(teams, folder_path, log_file, pretty_print)
    print_horizontal_line()


def get_all_teams_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_teams(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status == 200:
        teams = content['teams']
        print("There are {0} teams:".format(len(teams)))
        for team in teams:
            print("name: {0}".format(to_python2_and_3_compatible_string(team['name'])))
        return teams
    else:
        print("query teams failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_team(channel_name, file_name, alert_channel_setting, folder_path, pretty_print):
    file_path = save_json(file_name, alert_channel_setting, folder_path, 'team', pretty_print)
    print("team:{0} is saved to {1}".format(channel_name, file_path))


def get_individual_teams_and_save(teams, folder_path, log_file, pretty_print):
    file_path = folder_path + '/' + log_file
    if teams:
        with open(u"{0}".format(file_path), 'w') as f:
            for team in teams:
                if 'uid' in team:
                    team_identifier = team['uid']
                else:
                    team_identifier = team['id']

                save_team(
                    to_python2_and_3_compatible_string(team['name']),
                    to_python2_and_3_compatible_string(str(team_identifier)),
                    team,
                    folder_path,
                    pretty_print
                )
                f.write('{0}\t{1}\n'.format(to_python2_and_3_compatible_string(str(team_identifier)),
                                            to_python2_and_3_compatible_string(team['name'])))

