from glob import glob
import tarfile, shutil


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    archive_file = '{0}/{1}.tar.gz'.format(backup_dir, timestamp)
    backup_files = list()

    for folder_name in ['folders', 'datasources', 'dashboards', 'alert_channels']:
        backup_path = '{0}/{1}/{2}'.format(backup_dir, folder_name, timestamp)

        for file_path in glob(backup_path):
            backup_files.append(file_path)

    with tarfile.open(archive_file, "x:gz") as tar:
        for file_path in backup_files:
            tar.add(file_path)
            shutil.rmtree(file_path)
    tar.close()
    print('created archive: {0}'.format(archive_file))
