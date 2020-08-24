# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [1.1.3] - 2020-08-24

### Added
- #57 Backup users, organizations

### Changed
- #83 Fix tarfile options for python2
- #64 Remove empty folders when backup file (.tar.gz) created.  


# [1.1.2] - 2020-08-14

### Added

### Changed
- #70 Fix parameters for get_folder_id_from_old_folder_url
- #74 Fixed Bug folders.txt does not contain all folders
- #75 Introduces the settings option client_cert
- #76 require api checks to succeed before save or restore
- #78 fixed issue #77 TypeError: health_check

### Removed

## [1.1.0] - 2020-07-28

### Added
- boto3 added to package dependencies
- environment variables and configuration for native AWS S3 support
- s3_upload.py
- s3_download.py

### Changed

### Removed

## [1.0.0] - 2020-07-23

### Added
- add setup.py
- add Makefile (docker build)
- add grafanaSettings.json
- add constants.py
- add archive.py

### Changed
- rename src directory -> grafana_backup
- refactor Dockerfile
  - switched to alpine base
  - use CMD instead of ENTRYPOINT
  - run as non-root user
- README.md updates
- implemented cli "console script" using docopt
  - added "save" command
  - added "restore" command
- refactored variable passing
  - removed global variable passing in favor of positional arguments
  - all code lives inside functions now, no need for globalized code
- refactored grafanaSettings module
  - grafanaSettings can now be parameterized via an external json config file (~/.grafana-backup.json)
- refactored backup/restore shell scripts
- individual components can be backed up and restored using console_script
- archiving of backup can now be skipped using --no-archive

### Removed
- delete Pipenv
- delete docker_entry.sh
- delete requirements.txt

## [0.1.0] - 2019-05-22
Initial release, tentative.

### Added
- this `CHANGELOG.md`
- `requirements.txt` and `Pipfile` for better packaging hygiene

### Changed
- reorganize code layout, move all python into `src/`
- update README.md to reflect changes

### Removed
- delete boilerplate `restore_SOMETHING.sh` scripts


[Unreleased]: https://github.com/ysde/grafana-backup-tool/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ysde/grafana-backup-tool/releases/tag/v0.1.0
