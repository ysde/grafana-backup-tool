from grafana_backup.dashboardApi import import_grafana_settings
from glob import glob
import tarfile, shutil


settings_dict = import_grafana_settings("grafanaSettings")
globals().update(settings_dict)  # To be able to use the settings here, we need to update the globals of this module

def main():
    archive_file = '{0}/{1}.tar.gz'.format(BACKUP_DIR, timestamp)
    backup_files = list()

    for folder in ['folders', 'datasources', 'dashboards', 'alert_channels']:
        backup_path = '{0}/{1}/{2}'.format(BACKUP_DIR, folder, timestamp)

        for file_path in glob(backup_path):
            backup_files.append(file_path)

    with tarfile.open(archive_file, "x:gz") as tar:
        for file_path in backup_files:
            tar.add(file_path)
            shutil.rmtree(file_path)
    tar.close()
    print('created archive: {0}'.format(archive_file))
