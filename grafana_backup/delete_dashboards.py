from grafana_backup.dashboardApi import search_dashboard, delete_dashboard_by_uid, delete_dashboard_by_slug
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    limit = settings.get('SEARCH_API_LIMIT')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')
    uid_support = settings.get('DASHBOARD_UID_SUPPORT')
    paging_support = settings.get('PAGING_SUPPORT')

    if paging_support:
        delete_dashboards_above_Ver6_2(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
    else:
        delete_dashboards(limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)


def get_all_dashboards_in_grafana(page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_dashboard(page,
                                         limit,
                                         grafana_url,
                                         http_get_headers,
                                         verify_ssl, client_cert,
                                         debug)
    if status == 200:
        dashboards = content
        print("There are {0} dashboards:".format(len(dashboards)))
        for board in dashboards:
            print('name: {0}'.format(to_python2_and_3_compatible_string(board['title'])))
        return dashboards
    else:
        print("get dashboards failed, status: {0}, msg: {1}".format(status, content))
        return []


def get_individual_dashboard_and_delete(dashboards, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    if dashboards:
        for board in dashboards:
            if uid_support:
                status = delete_dashboard_by_uid(board['uid'], grafana_url, http_get_headers)
            else:
                status = delete_dashboard_by_slug(board['slug'], grafana_url, http_get_headers)

            if status == 200:
                print("deleted dashboard {0}".format(board['title']))
            else:
                print("got {0} when trying to delete board {1}".format(status, board['title']))


def delete_dashboards_above_Ver6_2(grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    limit = 5000  # limit is 5000 above V6.2+
    current_page = 1
    while True:
        dashboards = get_all_dashboards_in_grafana(current_page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
        print_horizontal_line()
        if len(dashboards) == 0:
            break
        else:
            current_page += 1
        get_individual_dashboard_and_delete(dashboards, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
        print_horizontal_line()


def delete_dashboards(limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support):
    current_page = 1
    dashboards = get_all_dashboards_in_grafana(current_page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    print_horizontal_line()
    get_individual_dashboard_and_delete(dashboards, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support)
    print_horizontal_line()
