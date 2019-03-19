import json, sys, re, argparse
from dashboardApi import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='file path saved of folder\' setting')
args = parser.parse_args()

file_path = args.path

with open(file_path, 'r') as f:
    data = f.read()

folder = json.loads(data)
result = create_folder(json.dumps(folder))
print("create result status: {0}, msg: {1}".format(result[0], result[1]))
