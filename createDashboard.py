import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of datasources\' setting')
args = parser.parse_args()

file_path = args.path

with open(file_path, 'r') as f:
    data = f.read()

dashboard = json.loads(data)
dashboard['dashboard']['id'] = None

db = {'dashboard': dashboard['dashboard']}
update_or_create_dashboard(json.dumps(db))

