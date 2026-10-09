<div align="center">
  <img src=".readme/logo.png" alt="Document Scanner CLI" width="360"><br><br>
</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Install](https://img.shields.io/badge/install-curl%20%7C%20bash-3775a9.svg)](#install)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#)

-----------------

**Document Scanner CLI** (`document-scanner`) is a standalone Python command-line client for the
[Document Scanner](../README.md) platform — AHL's self-hosted, developer-first document-processing
service for camera-based scanning, image enhancement, and document management.

The CLI drives the same REST API the web and mobile apps use: authenticate once, then scan documents
from the terminal, list and manage stored documents, trigger and inspect sync, read platform status
and usage metrics, and diagnose your local setup. It is built on `click`, `httpx`, and `rich`.

## Install

```bash
curl -fsSL https://downloads.documentscanner.app/cli/install.sh | bash   # or from a clone of this repo: pip install -e .
document-scanner doctor                    # checks Python, config, API connectivity, auth, completion
```

## Authentication

```bash
document-scanner login                     # interactive wizard
# or non-interactively:
document-scanner login --key <YOUR_API_KEY> --url https://<your-document-scanner-host>
```

- Config is stored at `~/.document_scanner/config.yaml`.
- Environment overrides: `DOCUMENT_SCANNER_API_KEY`, `DOCUMENT_SCANNER_API_URL`.
- Get an API key from the Document Scanner developer console in the web app; point `--url` at your deployment's API base (the backend serves on port `8006` in the default AHL stack).

## Commands

| Command | Description |
|---|---|
| `login` | Authenticate and store your API key |
| `scanner` | Manage document scanning — initialize a scan (`--path`, `--type`) and check scan status |
| `documents` | Manage documents — `list` (`--limit`, `--status`, `--quiet`), `get <id>`, `delete <id>` |
| `sync` | Manage synchronization — status, trigger a manual sync, view/adjust settings |
| `status` | Show system status and recent activity |
| `metrics` | Show usage metrics |
| `doctor` | Diagnose connection and configuration issues |
| `completion` | Generate a shell completion script |

## Example

```bash
# Authenticate, scan a file, then list recent documents
document-scanner login
document-scanner scanner init --path ./contract.jpg --type pdf
document-scanner documents list --limit 10 --status completed
```

## Documentation & resources

- **Usage / walkthrough** → [`../docs/CLI_USER_GUIDE.md`](../docs/CLI_USER_GUIDE.md)
- **Every command & flag** → [`../docs/CLI_COMMAND_REFERENCE.md`](../docs/CLI_COMMAND_REFERENCE.md)
- **Version history** → [`../docs/CHANGELOG.md`](../docs/CHANGELOG.md) (CLI section)
- **Platform root** → [`../README.md`](../README.md) · **API** → [`../docs/API_REFERENCE.md`](../docs/API_REFERENCE.md)

## License

This project is licensed under the MIT License.
