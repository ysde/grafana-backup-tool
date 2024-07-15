import json
from grafana_backup.dashboardApi import create_contact_point, get_grafana_version, search_contact_points, update_contact_point
from packaging import version


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    grafana_version_string = settings.get('GRAFANA_VERSION')
    if grafana_version_string:
        grafana_version = version.parse(grafana_version_string)
    else:
        try:
            grafana_version = get_grafana_version(grafana_url, verify_ssl, http_get_headers)
        except KeyError as error:
            if not grafana_version:
                raise Exception("Grafana version is not set.") from error

    minimum_version = version.parse('9.4.0')

    if minimum_version <= grafana_version:
        with open(file_path, 'r') as f:
            data = f.read()

        result = search_contact_points(grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        status_code = result[0]
        existing_contact_points = []
        if status_code == 200:
            # Successfully received list of contact points.
            # Append contact points to list of existing contact points
            for ecp in result[1]:
                existing_contact_points.append(ecp["uid"])

        contact_points = json.loads(data)
        for cp in contact_points:
            if cp["uid"] in existing_contact_points:
                print("Contact point {0} already exists, updating".format(cp["uid"]))
                result = update_contact_point(cp["uid"], json.dumps(cp), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
                if result[0] == 202:
                    print("Successfully updated contact point")
                else:
                    print("[ERROR] Contact point {0} failed to update. Return code:{1} - {2}".format(cp["uid"], result[0], result[1]))
            else:
                print("Contact point {0} does not exist, creating".format(cp["uid"]))
                result = create_contact_point(json.dumps(cp), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
                if result[0] == 202:
                    print("Successfully create contact point")
                else:
                    print("[ERROR] Contact point {0} failed to create. Retufn code:{1} - {2}".format(cp["uid"], result[0], result[1]))
    else:
        print("Unable to create contact points, requires Grafana version {0} or above. Current version is {1}".format(minimum_version, grafana_version))
