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
    content_of_all_folders = search_folders()
    folders = json.loads(content_of_all_folders)
    print("There are {0} folders:".format(len(folders)))
    for folder in folders:
        print(folder['title'])
    return folders


def save_folder_setting(folder_name, file_name, folder_settings):
    file_path = folder_path + '/' + file_name + '.folder'
    with open(file_path , 'w') as f:
        f.write(folder_settings)
    print("folder:{0} are saved to {1}".format(folder_name, file_path))


def get_indivisual_folder_setting_and_save(folders):
    for folder in folders:
        status_code_and_content = get_folder(folder['uid'])
        if status_code_and_content[0] == 200:
            save_folder_setting(folder['title'], folder['uid'], status_code_and_content[1])
            file_path = folder_path + '/' + log_file
            with open(u"{0}".format(file_path) , 'w+') as f:
                f.write('{}\t{}'.format(folder['uid'], folder['title']))

folders = get_all_folders_in_grafana()
print_horizontal_line()
get_indivisual_folder_setting_and_save(folders)
print_horizontal_line()

