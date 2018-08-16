import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of folder\' setting')
args = parser.parse_args()

file_path = args.path

with open(file_path, 'r') as f:
    data = f.read()

folder = json.loads(data)
create_folder(json.dumps(folder['dashboard']))
