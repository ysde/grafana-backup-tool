import json
from grafana_backup.dashboardApi import create_library_element, get_folder


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    # Library Elements can only be created referencing a folder id. However, this folder id is not unique across Grafana
    # instances. Therefore, we need to first find the folder id by the given folder uid.
    library_element = json.loads(data)
    folder_uid = library_element["meta"]["folderUid"]
    folder_id_response = get_folder(
        folder_uid, grafana_url, http_post_headers, verify_ssl, client_cert, debug
    )[1]
    if isinstance(folder_id_response, list):
        library_element["folderUid"] = folder_id_response[0]['uid']
    else:
        library_element["folderUid"] = folder_id_response['uid']
    result = create_library_element(
        json.dumps(library_element),
        grafana_url,
        http_post_headers,
        verify_ssl,
        client_cert,
        debug,
    )
    print(
        "create library_elements: {0}, status: {1}, msg: {2}".format(
            library_element["name"], result[0], result[1]
        )
    )
