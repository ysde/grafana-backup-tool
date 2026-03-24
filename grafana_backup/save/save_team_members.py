import os
from grafana_backup.dashboardApi import search_teams, search_team_members
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

    folderpath = '{0}/team_members/{1}'.format(backup_dir, timestamp)
    log_file = 'teams_{0}.txt'.format(timestamp)

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    teams = get_all_teams_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    get_individual_team_members_and_save(teams, folderpath, log_file, pretty_print, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
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


def get_team_members_in_grafana(team_id, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_team_members(team_id, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status == 200:
        team_members = content
        print("There are {0} team members in team {1}:".format(len(team_members), team_id))
        for team_member in team_members:
            print("name: {0}".format(to_python2_and_3_compatible_string(team_member['name'])))
        return team_members
    else:
        print("query team members failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_team_member(team_member, file_name, alert_channel_setting, folder_path, pretty_print):
    file_path = save_json(file_name, alert_channel_setting, folder_path, 'team_member', pretty_print)
    print("team:{0} is saved to {1}".format(team_member, file_path))


def get_individual_team_members_and_save(teams, folder_path, log_file, pretty_print, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    file_path = folder_path + '/' + log_file
    if teams:
        with open(u"{0}".format(file_path), 'w') as f:
            for team in teams:
                for team_member in get_team_members_in_grafana(team['id'], grafana_url, http_get_headers, verify_ssl,
                                                               client_cert, debug):
                    team_member_identifier = "{0}_{1}".format(team_member['userId'], team_member['teamId'])

                    save_team_member(
                        to_python2_and_3_compatible_string(team['name']),
                        to_python2_and_3_compatible_string(str(team_member_identifier)),
                        team_member,
                        folder_path,
                        pretty_print
                    )
                    f.write('{0}\t{1}\n'.format(to_python2_and_3_compatible_string(str(team_member_identifier)),
                                                to_python2_and_3_compatible_string(team['name'])))
