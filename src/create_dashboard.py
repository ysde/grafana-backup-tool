import json, argparse
from dashboardApi import import_grafana_settings, get_folder_id_from_old_folder_url, create_dashboard

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of datasources\' setting')
parser.add_argument('conf_filename', default="grafanaSettings", help='The settings file name in the conf directory'
                                                                     ' (for example: the server name we want to backup/restore)')
args = parser.parse_args()

file_path = args.path
import_grafana_settings(args.conf_filename)

with open(file_path, 'r') as f:
    data = f.read()

content = json.loads(data)
content['dashboard']['id'] = None

payload = {
    'dashboard': content['dashboard'],
    'folderId': get_folder_id_from_old_folder_url(content['meta']['folderUrl']),
    'overwrite': True
}

result = create_dashboard(json.dumps(payload))

print("create response status: {0}, msg: {1}".format(result[0], result[1]))
