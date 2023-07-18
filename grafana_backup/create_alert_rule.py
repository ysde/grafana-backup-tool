import json
from grafana_backup.dashboardApi import get_alert_rule, create_alert_rule, update_alert_rule, get_grafana_version
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

    with open(file_path, 'r') as f:
        data = f.read()

    try:
        grafana_version = get_grafana_version(grafana_url, verify_ssl)
    except KeyError as error:
        if not grafana_version:
            raise Exception("Grafana version is not set.") from error

    minimum_version = version.parse('9.4.0')

    if minimum_version <= grafana_version:
        alert_rule = json.loads(data)
        del alert_rule['id']
        uid = alert_rule['uid']
        get_response= get_alert_rule(uid, grafana_url, http_get_headers, verify_ssl, client_cert, debug)
        status_code=get_response[0]
        print("Got a code: {0}", status_code)
        if status_code == 404:
           http_post_headers['x-disable-provenance']='*'
           result = create_alert_rule(json.dumps(alert_rule), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        else:
           result = update_alert_rule(alert_rule['uid'], json.dumps(alert_rule), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        print("create alert rule: {0}, status: {1}, msg: {2}".format(alert_rule['title'], result[0], result[1]))
    else:
        print("Unable to create alert rules, requires Grafana version {0} or above. Current version is {1}".format(minimum_version, grafana_version))
