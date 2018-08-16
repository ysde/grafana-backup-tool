import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of datasources\' setting')
args = parser.parse_args()

file_path = args.path

with open(file_path, 'r') as f:
    data = f.read()

content = json.loads(data)
content['dashboard']['id'] = None

payload = {
    'dashboard': content['dashboard'],
    'folderId': get_folder_id_from_old_folder_url(content['meta']['folderUrl']),
    'overwrite': True
}

create_dashboard(json.dumps(payload))
