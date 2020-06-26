import os
import json
from grafana_backup.dashboardApi import import_grafana_settings, search_dashboard, get_dashboard, health_check
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, left_ver_newer_than_right_ver


settings_dict = import_grafana_settings("grafanaSettings")
globals().update(settings_dict)  # To be able to use the settings here, we need to update the globals of this module

module_name = "dashboards"
folder_path = '{0}/{1}/{2}'.format(BACKUP_DIR, module_name, timestamp)
log_file = '{0}_{1}.txt'.format(module_name, timestamp)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    (status, resp) = health_check()
    if status == 200:
        is_api_support_page_param = left_ver_newer_than_right_ver(resp['version'], "6.2.0")
        if is_api_support_page_param:
            save_dashboards_above_Ver6_2()
        else:
            save_dashboards()
    else:
        print("server status is not ok: {0}".format(resp))


def get_all_dashboards_in_grafana(page, limit=SEARCH_API_LIMIT):
    (status, content) = search_dashboard(page, limit)
    if status == 200:
        dashboards = content
        print("There are {0} dashboards:".format(len(dashboards)))
        for board in dashboards:
            print('name: {0}'.format(to_python2_and_3_compatible_string(board['title'])))
        return dashboards
    else:
        print("get dashboards failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_dashboard_setting(dashboard_name, file_name, dashboard_settings):
    file_path = folder_path + '/' + file_name + '.dashboard'
    print(dashboard_settings)
    with open(u"{0}".format(file_path), 'w') as f:
        f.write(json.dumps(dashboard_settings))
    print("dashboard: {0} -> saved to: {1}".format(dashboard_name, file_path))


def get_individual_dashboard_setting_and_save(dashboards):
    file_path = folder_path + '/' + log_file
    if dashboards:
        with open(u"{0}".format(file_path), 'w') as f:
            for board in dashboards:
                (status, content) = get_dashboard(board['uri'])
                if status == 200:
                    save_dashboard_setting(
                        to_python2_and_3_compatible_string(board['title']), 
                        board['uid'], 
                        content
                    )
                    f.write('{0}\t{1}\n'.format(board['uid'], to_python2_and_3_compatible_string(board['title'])))


def save_dashboards_above_Ver6_2():
    limit = 5000 # limit is 5000 above V6.2+
    current_page = 1
    while True:
        dashboards = get_all_dashboards_in_grafana(current_page, limit)
        print_horizontal_line()
        if len(dashboards) == 0:
            break
        else:
            current_page += 1
        get_individual_dashboard_setting_and_save(dashboards)
        print_horizontal_line()


def save_dashboards():
    dashboards = get_all_dashboards_in_grafana(1)
    print_horizontal_line()
    get_individual_dashboard_setting_and_save(dashboards)
    print_horizontal_line()
