import json, argparse
from dashboardApi import import_grafana_settings, create_folder

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of folder\' setting')
parser.add_argument('conf_filename', default="grafanaSettings", help='The settings file name in the conf directory'
                                                                     ' (for example: the server name we want to backup/restore)')
args = parser.parse_args()

file_path = args.path
import_grafana_settings(args.conf_filename)

with open(file_path, 'r') as f:
    data = f.read()

folder = json.loads(data)
result = create_folder(json.dumps(folder))
print("create result status: {0}, msg: {1}".format(result[0], result[1]))
