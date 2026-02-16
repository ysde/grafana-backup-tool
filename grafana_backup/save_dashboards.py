import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from grafana_backup.dashboardApi import search_dashboard, get_dashboard
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, save_json


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    limit = settings.get('SEARCH_API_LIMIT')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')
    uid_support = settings.get('DASHBOARD_UID_SUPPORT')
    uid_dashboard_slug_suffix = settings.get('UID_DASHBOARD_SLUG_SUFFIX')
    paging_support = settings.get('PAGING_SUPPORT')

    folder_path = '{0}/dashboards/{1}'.format(backup_dir, timestamp)
    log_file = 'dashboards_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if paging_support:
        save_dashboards_above_Ver6_2(folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, uid_dashboard_slug_suffix)
    else:
        save_dashboards(folder_path, log_file, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, uid_dashboard_slug_suffix)


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


def save_dashboard_setting(dashboard_name, file_name, dashboard_settings, folder_path, pretty_print):
    file_path = save_json(file_name, dashboard_settings, folder_path, 'dashboard', pretty_print)
    print("dashboard: {0} -> saved to: {1}".format(dashboard_name, file_path))


def fetch_single_dashboard(board, grafana_url, http_get_headers, verify_ssl, client_cert, debug, uid_support):
    """Helper function to fetch a single dashboard - used for parallel execution"""
    if uid_support:
        board_uri = "uid/{0}".format(board['uid'])
    else:
        board_uri = board['uri']
    
    (status, content) = get_dashboard(board_uri, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    return (status, content, board_uri, board)


def get_individual_dashboard_setting_and_save(dashboards, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, slug_suffix):
    file_path = folder_path + '/' + log_file
    if not dashboards:
        return
    
    # Use ThreadPoolExecutor to fetch dashboards in parallel
    # Default max_workers=None uses min(32, (os.cpu_count() or 1) + 4) threads
    # This can be adjusted if needed to avoid overwhelming the API
    max_workers = min(10, len(dashboards))  # Limit to 10 concurrent requests to avoid throttling
    
    dashboard_results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all dashboard fetch tasks
        future_to_board = {
            executor.submit(
                fetch_single_dashboard,
                board,
                grafana_url,
                http_get_headers,
                verify_ssl,
                client_cert,
                debug,
                uid_support
            ): board for board in dashboards
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_board):
            try:
                status, content, board_uri, board = future.result()
                if status == 200:
                    dashboard_results.append((board_uri, content, board))
                else:
                    print("Failed to fetch dashboard {0}, status: {1}".format(board_uri, status))
            except Exception as exc:
                board = future_to_board[future]
                board_uri = "uid/{0}".format(board['uid']) if uid_support else board['uri']
                print("Dashboard {0} generated an exception: {1}".format(board_uri, exc))
    
    # Write results to file and save dashboard settings
    with open(u"{0}".format(file_path), 'w') as f:
        for board_uri, content, board in dashboard_results:
            file_name = build_filename(board_uri, content, uid_support, slug_suffix)
            save_dashboard_setting(
                to_python2_and_3_compatible_string(board['title']),
                file_name,
                content,
                folder_path,
                pretty_print
            )
            f.write('{0}\t{1}\n'.format(board_uri, to_python2_and_3_compatible_string(board['title'])))


def build_filename(board_uri, content, uid_support, slug_suffix):
    file_name = board_uri
    if not uid_support:
        return file_name
    if not slug_suffix:
        return file_name
    slug = content.get("meta", {}).get("slug")
    suffix = "" if slug is None else "-" + slug
    file_name = "{0}{1}".format(board_uri, suffix)
    return file_name


def save_dashboards_above_Ver6_2(folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, slug_suffix):
    limit = 5000  # limit is 5000 above V6.2+
    current_page = 1
    while True:
        dashboards = get_all_dashboards_in_grafana(current_page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
        print_horizontal_line()
        if len(dashboards) == 0:
            break
        else:
            current_page += 1
        get_individual_dashboard_setting_and_save(dashboards, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, slug_suffix)
        print_horizontal_line()


def save_dashboards(folder_path, log_file, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, slug_suffix):
    current_page = 1
    dashboards = get_all_dashboards_in_grafana(current_page, limit, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    print_horizontal_line()
    get_individual_dashboard_setting_and_save(dashboards, folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print, uid_support, slug_suffix)
    print_horizontal_line()