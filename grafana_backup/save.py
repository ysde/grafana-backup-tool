from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
from grafana_backup.save_folders import main as save_folders
from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.archive import main as archive


def main(args, settings):
    arg_config = args.get('--components', False)
    if arg_config:
        arg_config_list = arg_config.split(',')

    if not arg_config or "dashboards" in arg_config_list:
        save_dashboards(args, settings)
    if not arg_config or "datasources" in arg_config_list:
        save_datasources(args, settings)
    if not arg_config or "folders" in arg_config_list:
        save_folders(args, settings)
    if not arg_config or "alert-channels" in arg_config_list:
        save_alert_channels(args, settings)

    archive(args, settings)
