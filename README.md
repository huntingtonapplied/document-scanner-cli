# Document Scanner CLI

`document-scanner` — a standalone Python command-line client for the Document Scanner API
(`login`, `documents`, `scanner`, `sync`, `metrics`, `status`, `doctor`, `completion`).

## Install

```bash
pip install document-scanner-cli      # or, from source: cd cli && pip install -e .
document-scanner doctor               # checks Python, config, API connectivity, auth, completion
```

Config lives at `~/.document_scanner/config.yaml`; key env vars: `DOCUMENT_SCANNER_API_KEY`,
`DOCUMENT_SCANNER_API_URL`.

Canonical documentation:
- **Usage / walkthrough** → [`../docs/CLI_USER_GUIDE.md`](../docs/CLI_USER_GUIDE.md)
- **Every command & flag** → [`../docs/CLI_COMMAND_REFERENCE.md`](../docs/CLI_COMMAND_REFERENCE.md)
- **Version history** → [`../docs/CHANGELOG.md`](../docs/CHANGELOG.md) (CLI section)
