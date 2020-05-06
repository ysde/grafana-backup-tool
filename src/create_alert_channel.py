import json, argparse
from dashboardApi import import_grafana_settings, create_alert_channel

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='the path of backup file of alert channels')
parser.add_argument('conf_filename', default="grafanaSettings", help='The settings file name in the conf directory'
                                                                     ' (for example: the server name we want to backup/restore)')
args = parser.parse_args()

file_path = args.path
import_grafana_settings(args.conf_filename)

with open(file_path, 'r') as f:
    data = f.read()

alert_channel = json.loads(data)
result = create_alert_channel(json.dumps(alert_channel))
print("create alert_channel: {0}, status: {1}, msg: {2}".format(alert_channel['name'], result[0], result[1]))
