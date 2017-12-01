import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path to save datasource setting')
args = parser.parse_args()

file_path = args.path
print(file_path)
with open(file_path, 'r') as f:
    data = f.read()

datasource = json.loads(data)
print("create datasource: {0}".format(datasource['name']))
create_datasource(json.dumps(datasource))
