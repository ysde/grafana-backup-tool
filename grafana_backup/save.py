from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
#from grafana_backup.save_folders import main as save_folders
#from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.archive import main as archive


def main(args, settings):
    save_dashboards(args, settings)
    save_datasources(args, settings)
    #save_folders()
    #save_alert_channels()
    archive(args, settings)
