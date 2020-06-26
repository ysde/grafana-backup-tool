import os
import json
from grafana_backup.dashboardApi import import_grafana_settings, search_datasource
from grafana_backup.commons import print_horizontal_line


settings_dict = import_grafana_settings("grafanaSettings")
globals().update(settings_dict)  # To be able to use the settings here, we need to update the globals of this module

module_name = "datasources"
folder_path = '{0}/{1}/{2}'.format(BACKUP_DIR, module_name, timestamp)
log_file = '{0}_{1}.txt'.format(module_name, timestamp)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    datasources = get_all_datasources_and_save()
    print_horizontal_line()

def save_datasource(file_name, datasource_setting):
    file_path = folder_path + '/' + file_name + '.datasource'
    with open(file_path, 'w') as f:
        f.write(json.dumps(datasource_setting))
        print("datasource:{0} is saved to {1}".format(file_name, file_path))

def get_all_datasources_and_save():
    status_code_and_content = search_datasource()
    if status_code_and_content[0] == 200:
        datasources = status_code_and_content[1]
        print("There are {0} datasources:".format(len(datasources)))
        for datasource in datasources:
            print(datasource)
            save_datasource(datasource['name'], datasource)
    else:
        print("query datasource failed, status: {0}, msg: {1}".format(status_code_and_content[0],
                                                                      status_code_and_content[1]))
