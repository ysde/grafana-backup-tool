from dashboardApi import *

file_path = '/tmp/datasources'

with open(file_path, 'r') as f:
    data = f.read()

datasources = json.loads(data)
for datasource in datasources:
    create_datasource(json.dumps(datasource))
    
