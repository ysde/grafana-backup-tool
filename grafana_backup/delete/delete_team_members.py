from grafana_backup.dashboardApi import search_teams, delete_team_member, search_team_members
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    teams = get_all_teams_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert,
                                                           debug)
    get_individual_team_member_and_delete(teams, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                              client_cert, debug)
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


def get_individual_team_member_and_delete(teams, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                              client_cert, debug):
    if teams:
        for team in teams:
            for team_member in get_team_members_in_grafana(team['id'], grafana_url, http_get_headers, verify_ssl,
                                                           client_cert, debug):
                status = delete_team_member(team_member['userId'], team_member['teamId'], grafana_url, http_get_headers, verify_ssl,
                                                client_cert, debug)
                team_member_name = to_python2_and_3_compatible_string(team_member['name'])
                if status == 200:
                    print("team member:{0} is deleted".format(team_member_name))
                else:
                    print("deleting team member {0} failed with {1}".format(team_member_name, status))
