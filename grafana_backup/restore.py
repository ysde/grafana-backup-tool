from grafana_backup.create_folder import main as create_folder
from grafana_backup.create_datasource import main as create_datasource
from grafana_backup.create_dashboard import main as create_dashboard
from grafana_backup.create_alert_channel import main as create_alert_channel
from glob import glob
import tarfile, tempfile


def main(args, settings):
    archive_file = args.get('<archive_file>', None)
    arg_components = args.get('--components', False)

    try:
        tarfile.is_tarfile(archive_file)
    except IOError as e:
        print(str(e))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tar = tarfile.open(archive_file, 'r')
        tar.extractall(tmpdir)
        tar.close()

        restore_functions = { 'folder': create_folder,
                              'datasource': create_datasource,
                              'dashboard': create_dashboard,
                              'alert_channel': create_alert_channel }

        if arg_components:
            arg_components_list = arg_components.split(',')

            # Restore only the components that provided via an argument
            # but must also exist in extracted archive
            for ext in arg_components_list:
                for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext[:-1]), recursive=True):
                    print('restoring {0}: {1}'.format(ext, file_path))
                    restore_functions[ext[:-1]](args, settings, file_path)
        else:
            # Restore every component included in extracted archive
            for ext in restore_functions.keys():
                for file_path in glob('{0}/**/*.{1}'.format(tmpdir, ext), recursive=True):
                    print('restoring {0}: {1}'.format(ext, file_path))
                    restore_functions[ext](args, settings, file_path)
