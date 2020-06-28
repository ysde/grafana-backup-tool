from grafana_backup.constants import (PKG_NAME, PKG_VERSION, CONFIG_PATH)
from grafana_backup.save import main as save
from grafana_backup.restore import main as restore
from grafana_backup.conf.grafanaSettings import main as conf
from docopt import docopt
from pathlib import Path
import os, sys

docstring = """
{0} {1}

Usage:
    grafana-backup save [--config=<filename>]
    grafana-backup restore <archive_file> [--config=<filename>]
    grafana-backup [--config=<filename>]
    grafana-backup -h | --help
    grafana-backup --version

Options:
    -h --help                                Show this help message and exit
    --version                                Get version information and exit
    --config=<filename>                      Override default configuration path
""".format(PKG_NAME, PKG_VERSION)

args = docopt(docstring, version='{0} {1}'.format(PKG_NAME, PKG_VERSION))


def main():
    arg_config = args.get('--config', False)
    example_config = '{0}/conf/grafana-backup.example.yml'.format(os.path.dirname(__file__))

    if arg_config:
        settings = conf(arg_config)
    elif Path(CONFIG_PATH).is_file():
        settings = conf(CONFIG_PATH)
    elif Path(example_config).is_file():
        settings = conf(example_config)

    if args.get('save', None):
        save(args, settings)
        sys.exit()
    elif args.get('restore', None):
        restore(args, settings)
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
