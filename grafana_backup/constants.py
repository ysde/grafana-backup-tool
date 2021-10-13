import os


if os.name == "nt":
    homedir = os.environ["HOMEPATH"]
else:
    homedir = os.environ["HOME"]

PKG_NAME = "grafana-backup"
<<<<<<< HEAD
PKG_VERSION = "1.2.2"
=======
PKG_VERSION = "1.1.11"
>>>>>>> update versions
JSON_CONFIG_PATH = "{0}/.grafana-backup.json".format(homedir)
