import argparse
from dashboardApi import *
from commons import *

parser = argparse.ArgumentParser()
parser.add_argument('path',  help='folder path to save folders')
args = parser.parse_args()

folder_path = args.path

def get_all_folders_in_grafana():
    content_of_all_folders = search_folders()
    folders = json.loads(content_of_all_folders)
    print "There are {0} folders:".format(len(folders))
    for board in folders:
        print board['title']
    return folders


def save_folder_setting(file_name, folder_settings):
    file_path = folder_path + '/' + file_name + '.folder'
    with open(file_path , 'w') as f:
        f.write(folder_settings)
    print "folder:{0} are saved to {1}".format(file_name, file_path)


def get_indivisual_folder_setting_and_save(folders):
    for board in folders:
        status_code_and_content = get_folder(board['uri'])
        if status_code_and_content[0] == 200:
            save_folder_setting(board['title'], status_code_and_content[1])

folders = get_all_folders_in_grafana()
print_horizontal_line()
folder_settings = get_indivisual_folder_setting_and_save(folders)
print_horizontal_line()

