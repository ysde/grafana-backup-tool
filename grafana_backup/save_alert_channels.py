import os
import json
from grafana_backup.dashboardApi import import_grafana_settings, search_alert_channels
from grafana_backup.commons import to_python2_and_3_compatible_string, print_horizontal_line


settings_dict = import_grafana_settings("grafanaSettings")
globals().update(settings_dict)  # To be able to use the settings here, we need to update the globals of this module

module_name = "alert_channels"
folder_path = '{0}/{1}/{2}'.format(BACKUP_DIR, module_name, timestamp)
log_file = '{0}_{0}.txt'.format(module_name, timestamp)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    alert_channels = get_all_alert_channels_in_grafana()
    get_individual_alert_channel_and_save(alert_channels)
    print_horizontal_line()


def get_all_alert_channels_in_grafana():
    (status, content) = search_alert_channels()
    if status == 200:
        channels = content
        print("There are {0} channels:".format(len(channels)))
        for channel in channels:
            print("name: {0}".format(to_python2_and_3_compatible_string(channel['name'])))
        return channels
    else:
        print("query alert channels failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_alert_channel(channel_name, file_name, alert_channel_setting):
    file_path = folder_path + '/' + str(file_name) + '.alert_channel'
    with open(file_path, 'w') as f:
        f.write(json.dumps(alert_channel_setting))
    print("alert_channel:{0} is saved to {1}".format(channel_name, file_path))


def get_individual_alert_channel_and_save(channels):
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
                    channel
                )
                f.write('{0}\t{1}\n'.format(to_python2_and_3_compatible_string(str(channel_identifier)),
                                            to_python2_and_3_compatible_string(channel['name'])))
