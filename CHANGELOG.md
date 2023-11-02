# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [1.4.2] - 2023-11-01

### Added
- enable aws s3 role assumption (use default providers chain) by @DerekTBrown in #245

### Changed
- chore: organize s3 utils by @DerekTBrown in #245

### Removed

# [1.4.1] - 2023-09-21

### Added

### Changed
- add missing argument http_get_headers #242 #243

### Removed

# [1.4.0] - 2023-09-20

### Added
- add contact points and notifcation policy backup functionalities by @ysde in #238
- added http headers to get_grafana_version request by @Mar8x in #239 

### Changed
- added py3-packaging to slim docker image, reported by @tasiotas in #241 :tada:

### Removed

# [1.3.3] - 2023-07-27

### Added

### Changed
- verify-ssl: only convert if string contains bool by @chriz-active in #234
- Validate version using regex in get_grafana_version by @acjohnson in #232 

### Removed

# [1.3.2] - 2023-07-19

### Added

### Changed
- fix versions/dashboard_versions hiccup by @chriz-active in #229
- hide_version-config: add version as config/env var by @chriz-active in #228
- Expose BACKUP_FILE_FORMAT to env by @vindex10 in #223
- add slug suffix for uid dashboards by @vindex10 in #222
- allow disabling auth check by @vindex10 in #221

### Removed
- [cicd] github-actions Python 2.7 support is no longer available #230

# [1.3.1] - 2023-05-31

### Added

### Changed
- import StringIO and pass data through StringIO read by @Keimille in #173
- Pass verify_ssl to get_grafana_version method by @yg265 in #207
- Update alert-rules key to match convention set in cli.py by @relaytheurgency in #208
- add the x-disable-provenance header for create_alert_rule by @yg265 in #211
- Perform upsert of alert rules by @mt3593 in #217

### Removed

# [1.3.0] - 2023-04-12

### Added

### Changed
- Only support alert rules if grafana is above version 9.4.0 by @mt3593 in #205

### Removed

# [1.2.6] - 2023-04-12

### Added

### Changed
- Add alert rules to backup by @mt3593 in #201
- Fix restoring library elements that have more than one folder by @antifuchs in #199
- Fixed GCP bucket upload example in readme by @IldarGalikov in #200
- Create a more compact docker image (remove dev packages from image) by @lavirott in #196

### Removed

# [1.2.5] - 2023-02-21

### Added

### Changed
- Backup, restore, and delete teams, team-members, and library-elements by @nileger in #181

### Removed

# [1.2.4] - 2022-08-04

### Added
- #190 InfluxDB Support
- #184 (feat): enable/disable api health check not supported by amazon managed grafana

### Changed
- #176 fix `folder_uid` when dashboard has no folder #175
- #183 Change the docker image in README.md examples
- #186 Require only necessary permissions when saving backup to GCS bucket

### Removed

# [1.2.3] - 2022-01-30

### Added

### Changed
- #174 Fixed ValueError when auth not properly configured

### Removed

# [1.2.2] - 2021-11-30

### Added

### Changed
- #158 added uid_support to datasource backups

### Removed

# [1.2.1] - 2021-10-15

### Added

### Changed
- 42755ef moved pause and unpause alerts to tools subcommand
- af51467 fixes #140 and ensures folder_permissions are restored

### Removed
- 30a937f removed unused restore_from_dir function

# [1.2.0] - 2021-10-11
- Publish to PyPi

### Added

### Changed
- cli changes are coming in 1.2.x which will introduce breaking arg parsing changes

### Removed

# [1.1.10] - 2021-10-04

### Added
- #150 Option to pause and unpause alerts
- #140 Add folder permissions backup
- #148 Option to save and restore snapshots
- #148 Option to save dashboard versions (restore isn't really possible with the API)
- #148 Option to save and restore annotations

### Changed

### Removed

# [1.1.9] - 2021-06-27

### Added
- c6b6f68 Create python-publish.yml
- #100 GCS support 

### Changed
- #92 better error message when the user specifies a bad S3 key
- #135 Update main organization instead of creating a new one  
- #133 Creating the docker container without these packages didn't work
- #139 windows env var fix

### Removed

# [1.1.8] - 2021-04-14

### Added

### Changed
- #124 fixed #123
- #121 multi arch docker support
- #127 add azure storage support

### Removed

# [1.1.7] - 2021-01-13

### Added

### Changed
- #123 fixed Crash on save_folders.py

### Removed

# [1.1.6] - 2020-12-28

### Added

### Changed
- #94 Key Error in api_checks.py (ensure compat with hide_version Grafana setting)
- #117 replace api version check with specific feature checks

### Removed

# [1.1.5] - 2020-12-13

### Added

### Changed
- #104 added python2 support to restore functions
- #105 add configuration attribute to set backup file name
- #112 changed restore_functions to ordered dict
- #113 [Fixed] Dashboards with same name in different folders not restored

### Removed
- #110 remove useless cleanup method within tempfile

# [1.1.4] - 2020-10-25

### Added

### Changed
- #102 add AWS_ENDPOINT_URL config option

### Removed

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
