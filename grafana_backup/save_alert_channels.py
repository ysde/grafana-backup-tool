import os
import json
from grafana_backup.dashboardApi import search_alert_channels
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')
    grafana_url = settings.get('GRAFANA_URL')
    http_get_headers = settings.get('HTTP_GET_HEADERS')
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    folder_path = '{0}/alert_channels/{1}'.format(backup_dir, timestamp)
    log_file = 'alert_channels_{0}.txt'.format(timestamp)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    alert_channels = get_all_alert_channels_in_grafana(grafana_url, http_get_headers, verify_ssl, client_cert, debug)
    get_individual_alert_channel_and_save(alert_channels, folder_path, log_file)
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


def save_alert_channel(channel_name, file_name, alert_channel_setting, folder_path):
    file_path = folder_path + '/' + str(file_name) + '.alert_channel'
    with open(file_path, 'w') as f:
        f.write(json.dumps(alert_channel_setting))
    print("alert_channel:{0} is saved to {1}".format(channel_name, file_path))


def get_individual_alert_channel_and_save(channels, folder_path, log_file):
    file_path = folder_path + '/' + log_file
    if channels:
        with open(u"{0}".format(file_path), 'w') as f:
            for channel in channels:
                if 'uid' in channel:
                    channel_identifier = channel['uid']
                else:
                    channel_identifier = channel['id']
                    
                save_alert_channel(
                    to_python2_and_3_compatible_string(channel['name']),
                    to_python2_and_3_compatible_string(str(channel_identifier)),
                    channel,
                    folder_path
                )
                f.write('{0}\t{1}\n'.format(to_python2_and_3_compatible_string(str(channel_identifier)),
                                            to_python2_and_3_compatible_string(channel['name'])))
