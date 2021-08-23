from grafana_backup.constants import (PKG_NAME, PKG_VERSION, JSON_CONFIG_PATH)
from grafana_backup.delete import main as delete
from grafana_backup.grafanaSettings import main as conf
from docopt import docopt
import os
import sys

docstring = """
{0} {1}

Usage:
    grafana-backup delete [--config=<filename>] [--components=<folders,dashboards,datasources,alert-channels,organizations,users,snapshots>]
    grafana-backup [--config=<filename>]
    grafana-backup -h | --help
    grafana-backup --version

Options:
    -h --help                                                       Show this help message and exit
    --version                                                       Get version information and exit
    --config=<filename>                                             Override default configuration path
    --components=<folders,dashboards,datasources,alert-channels,organizations,users,snapshots>    Comma separated list of individual components to delete
                                                                    rather than deleting all components by default
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

    if args.get('delete', None):
        delete(args, settings)
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
