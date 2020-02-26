import argparse
from dashboardApi import *
from commons import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save alert channels')
args = parser.parse_args()

folder_path = args.path
log_file = 'alert_channels_{0}.txt'.format(datetime.today().strftime('%Y%m%d%H%M'))

def get_all_alert_channels_in_grafana():
    (status, content) = search_alert_channels()
    if status == 200:
        channels = content
        print("There are {0} channels:".format(len(channels)))
        for channel in channels:
            print("name: {}".format(to_python2_and_3_compatible_string(channel['name'])))
        return channels
    else:
        print("query alert channels failed, status: {}, msg: {}".format(status, content))
        return []
    
def save_alert_channel(channel_name, file_name, alert_channel_setting):
    file_path = folder_path + '/' + str(file_name) + '.alert_channel'
    with open(file_path, 'w') as f:
        f.write(json.dumps(alert_channel_setting))
    print("alert_channel:{0} is saved to {1}".format(channel_name, file_path))

def get_indivisual_alert_channel_and_save(channels):
    file_path = folder_path + '/' + log_file
    if channels:
        with open(u"{0}".format(file_path) , 'w') as f:
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
                f.write('{}\t{}\n'.format(to_python2_and_3_compatible_string(str(channel_identifier)), to_python2_and_3_compatible_string(channel['name'])))


alert_channels = get_all_alert_channels_in_grafana()
get_indivisual_alert_channel_and_save(alert_channels)
print_horizontal_line()
