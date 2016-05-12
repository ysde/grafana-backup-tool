import argparse
from dashboardApi import *
from commons import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of dashboards\' setting')
args = parser.parse_args()

file_path = args.path

def get_all_dashboards_in_grafana():
    content_of_all_dashboards = search_dashboard()
    dashboards = json.loads(content_of_all_dashboards)
    print "There are {0} dashboards:".format(len(dashboards))
    for board in dashboards:
        print board['title']
    return dashboards

def get_indivisual_dashboard_setting_and_concat_to_string(dashboards):
    dashboard_settings = "[{0}]"
    tmp = ""
    for board in dashboards:
        status_code_and_content = get_dashboard(board['uri'])
        if status_code_and_content[0] == 200:
            tmp += status_code_and_content[1] + ","
    tmp = tmp[:-1]
    dashboard_settings = dashboard_settings.format(tmp)
    return dashboard_settings

def save_dashboards_settings(dashboard_settings):
    with open(file_path, 'w') as f:
        f.write(dashboard_settings)
    print "dashboards are saved to {0}".format(file_path)
    
dashboards = get_all_dashboards_in_grafana()
print_horizontal_line()
dashboard_settings = get_indivisual_dashboard_setting_and_concat_to_string(dashboards)
print_horizontal_line()
save_dashboards_settings(dashboard_settings)



