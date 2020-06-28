# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2020-06-27

### Added
- add setup.py
- add Makefile (docker build)
- add grafana-backup.example.yml
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
  - replaced backup_grafana.sh with "save" command
  - replaced restore_grafana.sh with "restore" command
- refactored variable passing
  - removed global variable passing in favor of positional arguments
  - all code lives inside functions now, no need for globalized code
- refactored grafanaSettings module
  - grafanaSettings can now be parameterized via an external yaml config file (~/.grafana-backup.yml)

### Removed
- delete Pipenv
- delete docker_entry.sh
- delete backup_grafana.sh
- delete restore_grafana.sh 
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
