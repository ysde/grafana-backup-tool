from grafana_backup.api_checks import main as api_checks
from grafana_backup.save_alert_rules import main as save_alert_rules
from grafana_backup.save_dashboards import main as save_dashboards
from grafana_backup.save_datasources import main as save_datasources
from grafana_backup.save_folders import main as save_folders
from grafana_backup.save_alert_channels import main as save_alert_channels
from grafana_backup.save_snapshots import main as save_snapshots
from grafana_backup.save_dashboard_versions import main as save_dashboard_versions
from grafana_backup.save_annotations import main as save_annotations
from grafana_backup.archive import main as archive
from grafana_backup.s3_upload import main as s3_upload
from grafana_backup.influx import main as influx
from grafana_backup.save_orgs import main as save_orgs
from grafana_backup.save_users import main as save_users
from grafana_backup.save_library_elements import main as save_library_elements
from grafana_backup.save_teams import main as save_teams
from grafana_backup.save_team_members import main as save_team_members
from grafana_backup.azure_storage_upload import main as azure_storage_upload
from grafana_backup.gcs_upload import main as gcs_upload
import sys


def main(args, settings):
    arg_components = args.get('--components', False)
    arg_no_archive = args.get('--no-archive', False)

    backup_functions = {'dashboards': save_dashboards,
                        'datasources': save_datasources,
                        'folders': save_folders,
                        'alert-channels': save_alert_channels,
                        'organizations': save_orgs,
                        'users': save_users,
                        'snapshots': save_snapshots,
                        'versions': save_dashboard_versions, # left for backwards compatibility
                        'dashboard-versions': save_dashboard_versions,
                        'annotations': save_annotations,
                        'library-elements': save_library_elements,
                        'teams': save_teams,
                        'team-members': save_team_members,
                        'alert-rules': save_alert_rules}

    (status, json_resp, dashboard_uid_support, datasource_uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        print("server status is not ok: {0}".format(json_resp))
        sys.exit(1)

    settings.update({'DASHBOARD_UID_SUPPORT': dashboard_uid_support})
    settings.update({'DATASOURCE_UID_SUPPORT': datasource_uid_support})
    settings.update({'PAGING_SUPPORT': paging_support})

    if arg_components:
        arg_components_list = arg_components.replace("_", "-").split(',')

        # Backup only the components that provided via an argument
        for backup_function in arg_components_list:
            backup_functions[backup_function](args, settings)
    else:
        # Backup every component
        for backup_function in backup_functions.keys():
            backup_functions[backup_function](args, settings)

    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    azure_storage_container_name = settings.get('AZURE_STORAGE_CONTAINER_NAME')
    gcs_bucket_name = settings.get('GCS_BUCKET_NAME')
    influxdb_host = settings.get('INFLUXDB_HOST')

    if not arg_no_archive:
        archive(args, settings)

    if aws_s3_bucket_name:
        print('Upload archives to S3:')
        s3_upload(args, settings)

    if azure_storage_container_name:
        print('Upload archives to Azure Storage:')
        azure_storage_upload(args, settings)

    if gcs_bucket_name:
        print('Upload archives to GCS:')
        gcs_upload(args, settings)

    if influxdb_host:
        influx(args, settings)
