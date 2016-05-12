import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of datasources\' setting')
args = parser.parse_args()

file_path = args.path

with open(file_path, 'r') as f:
    data = f.read()

dashboards = json.loads(data)

for board in dashboards:
    board['dashboard']['id'] = None
    update_or_create_dashboard(json.dumps(board))

