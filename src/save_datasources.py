import argparse
from dashboardApi import *
from commons import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save datasources')
args = parser.parse_args()

folder_path = args.path
log_file = 'datasources_{0}.txt'.format(datetime.today().strftime('%Y%m%d%H%M'))


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
        print("query datasource failed, status: {}, msg: {}".format(status_code_and_content[0], status_code_and_content[1]))


datasources = get_all_datasources_and_save()
print_horizontal_line()

