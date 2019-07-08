import argparse
from dashboardApi import *
from commons import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save folders')
args = parser.parse_args()

folder_path = args.path
log_file = 'folders_{0}.txt'.format(datetime.today().strftime('%Y%m%d%H%M'))

def get_all_folders_in_grafana():
    status_and_content_of_all_folders = search_folders()
    status = status_and_content_of_all_folders[0]
    content = status_and_content_of_all_folders[1]
    if status == 200:
        folders = content
        print("There are {0} folders:".format(len(content)))
        for folder in folders:
            print("name: {0}".format(to_python2_and_3_compatible_string(folder['title'])))
        return folders
    else:
        print("get folders failed, status: {0}, msg: {1}".format(status, content))
        return []


def save_folder_setting(folder_name, file_name, folder_settings):
    file_path = folder_path + '/' + file_name + '.folder'
    with open(file_path , 'w') as f:
        f.write(json.dumps(folder_settings))
    print("folder:{0} are saved to {1}".format(folder_name, file_path))


def get_indivisual_folder_setting_and_save(folders):
    for folder in folders:
        status_code_and_content = get_folder(folder['uid'])
        if status_code_and_content[0] == 200:
            save_folder_setting(
                to_python2_and_3_compatible_string(folder['title']), 
                folder['uid'], 
                status_code_and_content[1]
            )
            file_path = folder_path + '/' + log_file
            with open(u"{0}".format(file_path) , 'w+') as f:
                f.write('{}\t{}'.format(folder['uid'], to_python2_and_3_compatible_string(folder['title'])))

folders = get_all_folders_in_grafana()
print_horizontal_line()
get_indivisual_folder_setting_and_save(folders)
print_horizontal_line()

