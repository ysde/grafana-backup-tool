from glob import glob
import os, tarfile, shutil


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    archive_file = '{0}/{1}.tar.gz'.format(backup_dir, timestamp)
    backup_files = list()

    for folder_name in ['folders', 'datasources', 'dashboards', 'alert_channels', 'organizations', 'users', 'snapshots',
                        'dashboard_versions', 'annotations', 'library-elements', 'teams', 'team_members', 'alert_rules']:
        backup_path = '{0}/{1}/{2}'.format(backup_dir, folder_name, timestamp)

        for file_path in glob(backup_path):
            print('backup {0} at: {1}'.format(folder_name, file_path))
            backup_files.append(file_path)

    if os.path.exists(archive_file):
        os.remove(archive_file)

    with tarfile.open(archive_file, "w:gz") as tar:
        for file_path in backup_files:
            tar.add(file_path)
            shutil.rmtree(os.path.abspath(os.path.join(file_path, os.pardir)))
    tar.close()
    print('\ncreated archive at: {0}'.format(archive_file))
