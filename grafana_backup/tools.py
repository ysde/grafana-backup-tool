from grafana_backup.constants import (PKG_NAME, PKG_VERSION, JSON_CONFIG_PATH)
from grafana_backup.pause_alerts import main as pause_alerts
from grafana_backup.unpause_alerts import main as unpause_alerts
from docopt import docopt
import sys


def main(args, settings):

    precommand_args = args

    docstring = """
    {0} {1}

    Usage:
        grafana-backup tools pause-alerts [--config=<filename>]
        grafana-backup tools unpause-alerts [--config=<filename>] <alerts_filename>
        grafana-backup tools -h | --help

    Options:
        -h --help                               Show this help message and exit
        --version                               Get version information and exit
    """.format(PKG_NAME, PKG_VERSION)

    args = docopt(docstring, version='{0} {1}'.format(PKG_NAME, PKG_VERSION))

    combined_args = precommand_args.copy()
    combined_args.update(args) 

    if args.get('pause-alerts', None):
        pause_alerts(combined_args, settings)
        sys.exit()
    elif args.get('unpause-alerts', None):
        unpause_alerts(combined_args, settings)
        sys.exit()
    else:
        print(docstring)
        sys.exit()
