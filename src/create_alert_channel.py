import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='the path of backup file of alert channels')
args = parser.parse_args()

file_path = args.path
with open(file_path, 'r') as f:
    data = f.read()

alert_channel = json.loads(data)
result = create_alert_channel(json.dumps(alert_channel))
print("create alert_channel: {0}, status: {1}, msg: {2}".format(alert_channel['name'], result[0], result[1]))
