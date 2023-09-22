import json
from grafana_backup.dashboardApi import create_contact_point, get_grafana_version
from packaging import version


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    try:
        grafana_version = get_grafana_version(grafana_url, verify_ssl, http_get_headers)
    except KeyError as error:
        if not grafana_version:
            raise Exception("Grafana version is not set.") from error

    minimum_version = version.parse('9.4.0')

    if minimum_version <= grafana_version:
        with open(file_path, 'r') as f:
            data = f.read()

        contact_points = json.loads(data)
        for cp in contact_points:
            result = create_contact_point(json.dumps(
                cp), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
            print("create contact_point: {0}, status: {1}, msg: {2}".format(
                cp['name'], result[0], result[1]))
    else:
        print("Unable to create contact points, requires Grafana version {0} or above. Current version is {1}".format(
            minimum_version, grafana_version))
