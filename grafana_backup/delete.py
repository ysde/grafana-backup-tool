from grafana_backup.api_checks import main as api_checks
from grafana_backup.delete_dashboards import main as delete_dashboards
from grafana_backup.delete_datasources import main as delete_datasources
from grafana_backup.delete_library_elements import main as delete_library_elements
from grafana_backup.delete_folders import main as delete_folders
from grafana_backup.delete_alert_channels import main as delete_alert_channels
from grafana_backup.delete_snapshots import main as delete_snapshots
from grafana_backup.delete_annotations import main as delete_annotations
from grafana_backup.delete_team_members import main as delete_team_members
import sys


def main(args, settings):
    arg_components = args.get('--components', False)

    # By default, teams should not be deleted. Sinces teams don't have unique ids across instances, they would be
    # recreated with different ids, therefore loosing references to folder permissions and team members.
    delete_functions = {'dashboards': delete_dashboards,
                        'datasources': delete_datasources,
                        'folders': delete_folders,
                        'alert-channels': delete_alert_channels,
                        'snapshots': delete_snapshots,
                        'annotations': delete_annotations,
                        'library-elements': delete_library_elements,
                        'team-members': delete_team_members}

    (status, json_resp, dashboard_uid_support, datasource_uid_support, paging_support) = api_checks(settings)

    # Do not continue if API is unavailable or token is not valid
    if not status == 200:
        print("server status is not ok: {0}".format(json_resp))
        sys.exit(1)

    settings.update({'DASHBOARD_UID_SUPPORT': dashboard_uid_support})
    settings.update({'DATASOURCE_UID_SUPPORT': datasource_uid_support})
    settings.update({'PAGING_SUPPORT': paging_support})

    if arg_components:
        arg_components_list = arg_components.split(',')

        # Delete only the components that provided via an argument
        for delete_function in arg_components_list:
            delete_functions[delete_function](args, settings)
    else:
        # delete every component
        for delete_function in delete_functions.keys():
            delete_functions[delete_function](args, settings)
