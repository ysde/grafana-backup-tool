import json
from grafana_backup.dashboardApi import import_grafana_settings, create_alert_channel


def main(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    alert_channel = json.loads(data)
    result = create_alert_channel(json.dumps(alert_channel))
    print("create alert_channel: {0}, status: {1}, msg: {2}".format(alert_channel['name'], result[0], result[1]))
