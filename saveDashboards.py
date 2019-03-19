import argparse
from dashboardApi import *
from commons import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save dashboards')
args = parser.parse_args()

folder_path = args.path

log_file = 'dashboards_{0}.txt'.format(datetime.today().strftime('%Y%m%d%H%M'))

def get_all_dashboards_in_grafana():
    content_of_all_dashboards = search_dashboard()
    dashboards = json.loads(content_of_all_dashboards)
    print("There are {0} dashboards:".format(len(dashboards)))
    for board in dashboards:
        print('name: {}'.format(board['title']))
    return dashboards


def save_dashboard_setting(dashboard_name, file_name, dashboard_settings):
    file_path = folder_path + '/' + file_name + '.dashboard'
    with open(u"{0}".format(file_path) , 'w') as f:
        f.write(dashboard_settings)
    print("dashboard: {0} -> saved to: {1}".format(dashboard_name, file_path))


def get_indivisual_dashboard_setting_and_save(dashboards):
    for board in dashboards:
        status_code_and_content = get_dashboard(board['uri'])
        if status_code_and_content[0] == 200:
            save_dashboard_setting(board['title'], board['uid'], status_code_and_content[1])
            file_path = folder_path + '/' + log_file
            with open(u"{0}".format(file_path) , 'w+') as f:
                f.write('{}\t{}'.format(board['uid'], board['title']))

dashboards = get_all_dashboards_in_grafana()
print_horizontal_line()
get_indivisual_dashboard_setting_and_save(dashboards)
print_horizontal_line()

