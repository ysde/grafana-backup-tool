import json
from grafana_backup.dashboardApi import import_grafana_settings, get_folder_id_from_old_folder_url, create_dashboard


def main(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    content = json.loads(data)
    content['dashboard']['id'] = None

    payload = {
        'dashboard': content['dashboard'],
        'folderId': get_folder_id_from_old_folder_url(content['meta']['folderUrl']),
        'overwrite': True
    }

    result = create_dashboard(json.dumps(payload))
    print("create response status: {0}, msg: {1}".format(result[0], result[1]))
