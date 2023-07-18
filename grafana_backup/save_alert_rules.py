import os
from grafana_backup.dashboardApi import search_alert_rules, get_alert_rule, get_grafana_version
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line, save_json
from packaging import version


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')
    folder_path = '{0}/alert_rules/{1}'.format(backup_dir, timestamp)
    log_file = 'alert_rules_{0}.txt'.format(timestamp)
    grafana_version_string = settings.get('GRAFANA_VERSION')
    if grafana_version_string:
      grafana_version = version.parse(grafana_version_string)

    try:
        grafana_version = get_grafana_version(grafana_url, verify_ssl)
    except KeyError as error:
        if not grafana_version:
            raise Exception("Grafana version is not set.") from error

    minimum_version = version.parse('9.4.0')

    if minimum_version <= grafana_version:

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_alert_rules(folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print)
    else:
        print("Unable to save alert rules, requires Grafana version {0} or above. Current version is {1}".format(minimum_version, grafana_version))


def get_all_alert_rules_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_alert_rules(grafana_url,
                                           http_get_headers,
                                           verify_ssl, client_cert,
                                           debug)
    if status == 200:
        alert_rules = content
        print("There are {0} alert rules:".format(len(alert_rules)))
        for alert_rule in alert_rules:
            print('name: {0}'.format(to_python2_and_3_compatible_string(alert_rule['title'])))
        return alert_rules
    else:
        raise Exception("Failed to get alert rules, status: {0}, msg: {1}".format(status, content))


def save_alert_rules(folder_path, log_file, grafana_url, http_get_headers, verify_ssl, client_cert, debug, pretty_print):
    alert_rules = get_all_alert_rules_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    for alert_rule in alert_rules:
        print_horizontal_line()
        print(alert_rule)
        file_path = save_json(alert_rule['uid'],
                              alert_rule,
                              folder_path,
                              'alert_rule',
                              pretty_print)
        print("alert_rule: {0} -> saved to: {1}"
              .format(to_python2_and_3_compatible_string(alert_rule['title']),
                      file_path))
        print_horizontal_line()
