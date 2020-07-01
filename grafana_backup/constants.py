import os


PKG_NAME = 'grafana-backup'
PKG_VERSION = '1.0.0'
YAML_CONFIG_PATH = '{0}/.grafana-backup.yml'.format(os.environ['HOME'])
JSON_CONFIG_PATH = '{0}/.grafana-backup.json'.format(os.environ['HOME'])
