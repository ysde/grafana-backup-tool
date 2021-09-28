import os
import sys
from docopt import docopt
from grafana_backup.constants import (PKG_NAME, PKG_VERSION, JSON_CONFIG_PATH)
from grafana_backup.grafanaSettings import main as conf
from grafana_backup.make_users_viewers import main as make_users_viewers
from grafana_backup.restore_user_permissions import main as restore_user_permissions

docstring = """
{0} {1}

Usage:
    grafana-backup makeusersviewers [--config=<filename>]
    grafana-backup restoreusers <users_filename> [--config=<filename>]
    grafana-backup -h | --help
    grafana-backup --version

Options:
    -h --help                                                       Show this help message and exit
    --version                                                       Get version information and exit
    --config=<filename>                                             Override default configuration path
""".format(PKG_NAME, PKG_VERSION)

args = docopt(docstring, version='{0} {1}'.format(PKG_NAME, PKG_VERSION))


def main():
    arg_config = args.get('--config', False)
    default_config = '{0}/conf/grafanaSettings.json'.format(os.path.dirname(__file__))

    if arg_config:
        settings = conf(arg_config)
    elif os.path.isfile(JSON_CONFIG_PATH):
        settings = conf(JSON_CONFIG_PATH)
    elif os.path.isfile(default_config):
        settings = conf(default_config)

    if args.get('makeusersviewers', None):
        make_users_viewers(args, settings)
        sys.exit()
    elif args.get('restoreusers', None):
        restore_user_permissions(args, settings)
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
