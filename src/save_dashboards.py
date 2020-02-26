import argparse
from dashboardApi import *
from commons import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save dashboards')
args = parser.parse_args()

folder_path = args.path

log_file = 'dashboards_{0}.txt'.format(datetime.today().strftime('%Y%m%d%H%M'))

def get_all_dashboards_in_grafana(page, limit=SEARCH_API_LIMIT):
    (status, content) = search_dashboard(page, limit)
    if status == 200:
        dashboards = content
        print("There are {0} dashboards:".format(len(dashboards)))
        for board in dashboards:
            print('name: {}'.format(to_python2_and_3_compatible_string(board['title'])))
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


def get_indivisual_dashboard_setting_and_save(dashboards):
    file_path = folder_path + '/' + log_file
    if dashboards:
        with open(u"{0}".format(file_path) , 'w') as f:
            for board in dashboards:
                (status, content) = get_dashboard(board['uri'])
                if status == 200:
                    save_dashboard_setting(
                        to_python2_and_3_compatible_string(board['title']), 
                        board['uid'], 
                        content
                    )
                    f.write('{}\t{}\n'.format(board['uid'], to_python2_and_3_compatible_string(board['title'])))

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
        get_indivisual_dashboard_setting_and_save(dashboards)
        print_horizontal_line()
    
def save_dashboards():
    dashboards = get_all_dashboards_in_grafana(1)
    print_horizontal_line()
    get_indivisual_dashboard_setting_and_save(dashboards)
    print_horizontal_line()

(status, resp) = health_check()
if status == 200:
    is_api_support_page_param = left_ver_newer_than_right_ver(resp['version'], "6.2.0")
    if is_api_support_page_param:
        save_dashboards_above_Ver6_2()
    else:
        save_dashboards()
else:
    print("server status is not ok: {0}".format(resp))
