import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path to save datasource setting')
args = parser.parse_args()

file_path = args.path
with open(file_path, 'r') as f:
    data = f.read()

datasource = json.loads(data)
result = create_datasource(json.dumps(datasource))
print("create datasource: {0}, status: {1}, msg: {2}".format(datasource['name'], result[0], result[1]))
