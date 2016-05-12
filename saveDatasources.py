import argparse
from dashboardApi import *
from commons import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of datasources\' setting')
args = parser.parse_args()

file_path = args.path

def get_all_datasources_in_grafana():
    content_of_datasources = search_datasource()
    datasources = json.loads(content_of_datasources)
    print "There are {0} datasources:".format(len(datasources))
    for datasource in datasources:
        print datasource['name']
    return datasources

def save_datasources(datasource_settings):
    with open(file_path, 'w') as f:
        f.write(json.dumps(datasource_settings))
        print "datasources are saved to {0}".format(file_path)

datasources = get_all_datasources_in_grafana()
print_horizontal_line()
save_datasources(datasources)

