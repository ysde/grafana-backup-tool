from grafana_backup.dashboardApi import search_alert_channels
from grafana_backup.dashboardApi import delete_alert_channel_by_uid
from grafana_backup.dashboardApi import delete_alert_channel_by_id
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_POST_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')
    pretty_print = settings.get('PRETTY_PRINT')

    alert_channels = get_all_alert_channels_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    get_individual_alert_channel_and_delete(alert_channels, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                            client_cert, debug)
    print_horizontal_line()


def get_all_alert_channels_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug):
    (status, content) = search_alert_channels(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    if status == 200:
        channels = content
        print("There are {0} channels:".format(len(channels)))
        for channel in channels:
            print("name: {0}".format(to_python2_and_3_compatible_string(channel['name'])))
        return channels
    else:
        print("query alert channels failed, status: {0}, msg: {1}".format(status, content))
        return []


def get_individual_alert_channel_and_delete(channels, pretty_print, grafana_url, http_get_headers, verify_ssl,
                                            client_cert, debug):
    if channels:
        for channel in channels:
            status = 0

            if 'uid' in channel:
                status = delete_alert_channel_by_uid(channel['uid'], grafana_url, http_get_headers, verify_ssl,
                                                     client_cert, debug)
            else:
                status = delete_alert_channel_by_id(channel['id'], grafana_url, http_get_headers, verify_ssl,
                                                    client_cert, debug)

            channel_name = to_python2_and_3_compatible_string(channel['name'])
            if status == 200:
                print("alert_channel:{0} is deleted".format(channel_name))
            else:
                print("deleting alert_channel {0} failed with {1}".format(channel_name, status))
