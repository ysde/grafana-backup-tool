import json
from grafana_backup.dashboardApi import import_grafana_settings, create_datasource


def main(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    datasource = json.loads(data)
    result = create_datasource(json.dumps(datasource))
    print("create datasource: {0}, status: {1}, msg: {2}".format(datasource['name'], result[0], result[1]))
