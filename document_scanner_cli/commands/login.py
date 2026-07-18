"""document-scanner login — authenticate and store API key."""

import click
from rich.panel import Panel
from document_scanner_cli.config import save_config, load_config, get_api_url
from document_scanner_cli.api import DocumentScannerClient, APIError
from document_scanner_cli.output import get_console
from document_scanner_cli.exit_codes import EXIT_VALIDATION


@click.command()
@click.option("--key", default=None, help="Your Document Scanner API key (skips wizard)")
@click.option("--url", default=None, help="API URL (default: http://localhost:8004)")
@click.pass_context
def login(ctx, key: str, url: str):
    """Authenticate with the Document Scanner platform.

    \b
    Examples:
        document-scanner login                     # interactive wizard
        document-scanner login --key ds_abc123  # non-interactive
    """
    console = get_console(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not key and ci_mode:
        click.echo("✗ --key is required in CI mode: document-scanner login --key <key>", err=True)
        raise SystemExit(EXIT_VALIDATION)

    if not key:
        click.echo()
        click.echo("  Welcome to Document Scanner!")
        click.echo()
        click.echo("  To get your API key:")
        click.echo("    1. Go to your Document Scanner instance /account")
        click.echo("    2. Click the Developer tab")
        click.echo("    3. Copy your API key")
        click.echo()
        key = click.prompt("  API Key", hide_input=True)
        if not url:
            use_custom = click.confirm("  Use a custom API URL?", default=False)
            if use_custom:
                url = click.prompt("  API URL", default="http://localhost:8004")

    key = key.strip()
    config = load_config()
    config["api_key"] = key
    if url:
        config["api_url"] = url.strip()
    save_config(config)

    api_url = url or get_api_url()
    click.echo(f"✓ API key saved to ~/.document_scanner/config.yaml")
    click.echo(f"  API URL: {api_url}")

    try:
        client = DocumentScannerClient(api_key=key, api_url=api_url)
        doc_list = client.list_documents()
        console.print(Panel(
            f"✓ Authenticated — {len(doc_list)} document(s) found\n\n"
            "  [dim]document-scanner documents list[/dim]         list your documents\n"
            "  [dim]document-scanner scanner init[/dim]            scan documents\n"
            "  [dim]document-scanner metrics dashboard[/dim]  view dashboard",
            title="Connected",
            border_style="green",
            expand=False,
        ))
    except Exception as e:
        click.echo(f"⚠ Key saved but verification failed: {e}", err=True)
        click.echo("  Check your key and try again: document-scanner login", err=True)
