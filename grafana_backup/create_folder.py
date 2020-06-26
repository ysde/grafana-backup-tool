import json
from grafana_backup.dashboardApi import import_grafana_settings, create_folder


def main(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    folder = json.loads(data)
    result = create_folder(json.dumps(folder))
    print("create result status: {0}, msg: {1}".format(result[0], result[1]))
