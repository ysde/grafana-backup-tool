import json
import os
from grafana_backup.dashboardApi import create_folder


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    # get dirname with file_paths
    folder_dir = os.path.dirname(file_path)

    # get all files in dir
    all_files = [f for f in os.listdir(folder_dir) if f.endswith('.folder')]

    # first loop without parentUid
    for filename in all_files:
        with open(os.path.join(folder_dir, filename), 'r') as f:
            folder = json.load(f)

        if 'parentUid' not in folder or not folder.get('parentUid'):
            result = create_folder(json.dumps(folder), grafana_url, http_post_headers,
                                   verify_ssl, client_cert, debug)
            print("create folder {0}, status: {1}, msg: {2}\n".format(
                folder.get('title', ''), result[0], result[1]))

    # second loop with parentUid
    for filename in all_files:
        with open(os.path.join(folder_dir, filename), 'r') as f:
            folder = json.load(f)

        if 'parentUid' in folder and folder.get('parentUid'):
            result = create_folder(json.dumps(folder), grafana_url, http_post_headers,
                                   verify_ssl, client_cert, debug)
            print("create folder {0}, status: {1}, msg: {2}\n".format(
                folder.get('title', ''), result[0], result[1]))