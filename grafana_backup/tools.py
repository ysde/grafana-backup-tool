from grafana_backup.constants import (PKG_NAME, PKG_VERSION)
from grafana_backup.pause_alerts import main as pause_alerts
from grafana_backup.unpause_alerts import main as unpause_alerts
from grafana_backup.make_users_viewers import main as make_users_viewers
from grafana_backup.restore_user_permissions import main as restore_user_permissions
from docopt import docopt
import sys


def main(precommand_args, settings):

    docstring = """
{0} {1}

Usage:
    grafana-backup tools pause-alerts [--config=<filename>]
    grafana-backup tools unpause-alerts <alerts_filename> [--config=<filename>]
    grafana-backup tools make-users-viewers [--config=<filename>]
    grafana-backup tools restore-users <users_filename> [--config=<filename>]
    grafana-backup tools [-h | --help]

Options:
    -h --help                               Show this help message and exit
    --version                               Get version information and exit
    --config=<filename>                     Override default configuration path
    """.format(PKG_NAME, PKG_VERSION)

    args = docopt(docstring, help=False,
                  version='{0} {1}'.format(PKG_NAME, PKG_VERSION))

    combined_args = precommand_args.copy()
    combined_args.update(args)

    if args.get('pause-alerts', None):
        pause_alerts(combined_args, settings)
        sys.exit()
    elif args.get('unpause-alerts', None):
        unpause_alerts(combined_args, settings)
        sys.exit()
    elif args.get('make-users-viewers', None):
        make_users_viewers(args, settings)
        sys.exit()
    elif args.get('restore-users', None):
        restore_user_permissions(args, settings)
        sys.exit()
    elif args.get('--help', None):
        print(docstring)
        sys.exit()
    else:
        print(docstring)
        sys.exit()
