from grafana_backup.constants import (PKG_NAME, PKG_VERSION, CONFIG_PATH)
from grafana_backup.save import main as save
from grafana_backup.restore import main as restore
from docopt import docopt
import sys

docstring = """
{0} {1}

Usage:
    grafana-backup -h, --help
    grafana-backup [--version] [--config] [--url] [--token]
    grafana-backup save [--verbose]
    grafana-backup restore <archive_file> [--verbose]

Options:
    -h, --help                               Show this help message and exit
    --config                                 Override default configuration path (currently set to {2})
    --url                                    Override grafana url stored in configuration file
    --token                                  Override grafana api token stored in configuration file
    --version                                Get version information and exit

    --verbose                                Display verbose output for command
""".format(PKG_NAME, PKG_VERSION, CONFIG_PATH)

args = docopt(docstring, version='{0} {1}'.format(PKG_NAME, PKG_VERSION))


def main():

    arg_verbose = args.get('--verbose', None)
    arg_url = args.get('--url', None)
    arg_token = args.get('--token', None)

    if args.get('save', None):
        save(args)
        sys.exit()
    elif args.get('restore', None):
        restore(args)
        sys.exit()
    else:
        print(docstring)
        sys.exit()


if __name__ == '__main__':
    main()
