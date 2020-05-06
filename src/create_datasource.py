import json, argparse
from dashboardApi import import_grafana_settings, create_datasource

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path to save datasource setting')
parser.add_argument('conf_filename', default="grafanaSettings", help='The settings file name in the conf directory'
                                                                     ' (for example: the server name we want to backup/restore)')
args = parser.parse_args()

file_path = args.path
import_grafana_settings(args.conf_filename)

with open(file_path, 'r') as f:
    data = f.read()

datasource = json.loads(data)
result = create_datasource(json.dumps(datasource))
print("create datasource: {0}, status: {1}, msg: {2}".format(datasource['name'], result[0], result[1]))
