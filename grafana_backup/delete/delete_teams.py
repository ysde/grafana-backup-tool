from grafana_backup.dashboardApi import search_teams
from grafana_backup.dashboardApi import delete_team
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
    get_individual_team_and_delete(teams, pretty_print, grafana_url, http_get_headers, verify_ssl,
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


def get_individual_team_and_delete(teams, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                              client_cert, debug):
    if teams:
        for team in teams:
            status = delete_team(team['id'], grafana_url, http_get_headers, verify_ssl,
                                            client_cert, debug)
            team_name = to_python2_and_3_compatible_string(team['name'])
            if status == 200:
                print("team:{0} is deleted".format(team_name))
            else:
                print("deleting team {0} failed with {1}".format(team_name, status))
