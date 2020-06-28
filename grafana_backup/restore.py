from grafana_backup.create_folder import main as create_folder
#from grafana_backup.create_datasource import main as create_datasource
#from grafana_backup.create_dashboard import main as create_dashboard
#from grafana_backup.create_alert_channel import main as create_alert_channel
from glob import glob
import tarfile, tempfile


def main(args, settings):
    archive_file = args.get('<archive_file>', None)

    try:
        tarfile.is_tarfile(archive_file)
    except IOError as e:
        print(str(e))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tar = tarfile.open(archive_file, 'r')
        tar.extractall(tmpdir)
        tar.close()
        for ext in ['folder', 'datasource', 'dashboard', 'alert_channel']:
            for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext), recursive=True): 
                if ext == 'folder':
                    print('restoring folder: {0}'.format(file_path))
                    create_folder(args, settings, file_path)
                if ext == 'datasource':
                    print('restoring datasource: {0}'.format(file_path))
                    #create_datasource(args, settings, file_path)
                if ext == 'dashboard':
                    print('restoring dashboard: {0}'.format(file_path))
                    #create_dashboard(args, settings, file_path)
                if ext == 'alert_channel':
                    print('restoring alert_channel: {0}'.format(file_path))
                    #create_alert_channel(args, settings, file_path)
