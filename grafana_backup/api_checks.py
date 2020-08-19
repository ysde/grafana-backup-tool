from grafana_backup.dashboardApi import health_check, auth_check


def main(settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    (status, json_resp) = health_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if not status == 200:
        return (status, json_resp, None)

    api_version = json_resp['version']

    (status, json_resp) = auth_check(grafana_url, http_get_headers, verify_ssl, client_cert, debug)

    return (status, json_resp, api_version)
