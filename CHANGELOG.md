# Changelog

All notable changes to the Document Scanner CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Pre-1.0 policy:** Minor versions (0.x) may include breaking changes.

## [0.1.3] - 2026-10-14

### Fixed
- The update check no longer queries PyPI. `document-scanner-cli` is not published there and the PyPI name may belong to an unrelated project, so the old check could report a stranger's version and suggest installing it. It now reads the latest GitHub release of huntingtonapplied/document-scanner-cli and suggests `pip install --upgrade git+https://github.com/huntingtonapplied/document-scanner-cli`, only when that release is newer.

## [0.1.2] - 2026-10-13

### Changed
- README: describes the hosted service accurately (it is not self-hosted) and links the product site.

## [0.1.0] - 2026-07-18

### Added
- Initial public release — a thin client for the hosted Document Scanner API.
- Commands: `login`, `documents`, `scanner`, `sync`, `metrics`, `status`,
  `doctor`, `completion`.
- `install.sh` for binary download + install.
