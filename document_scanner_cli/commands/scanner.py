"""document-scanner scanner — manage document scanning."""

import click
from document_scanner_cli.api import DocumentScannerClient, AuthError, APIError
from document_scanner_cli.output import get_console, is_json, print_json
from document_scanner_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def scanner(ctx):
    """Manage document scanning."""
    pass


@scanner.command("init")
@click.option("--path", required=True, help="Path to document or directory to scan")
@click.option("--type", default="pdf", help="Document type (pdf, image, etc.)")
@click.pass_context
def scanner_init(ctx, path, type):
    """Initialize a document scan."""
    json_mode = is_json(ctx)

    try:
        client = DocumentScannerClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    data = {"path": path, "type": type}

    try:
        result = client.init_scan(data)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(result)
        return

    console = get_console(ctx)
    console.print(f"[bold]Scan Initialized[/bold]")
    console.print(f"  Scan ID: {result.get('scan_id', '')}")
    console.print(f"  Status: {result.get('status', '')}")


@scanner.command("status")
@click.argument("scan_id")
@click.pass_context
def scanner_status(ctx, scan_id):
    """Get scan status."""
    json_mode = is_json(ctx)

    try:
        client = DocumentScannerClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        status = client.get_scan_status(scan_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(status)
        return

    console = get_console(ctx)
    console.print(f"[bold]Scan Status[/bold]")
    console.print(f"  Scan ID: {scan_id}")
    console.print(f"  Status: {status.get('status', '')}")
    console.print(f"  Progress: {status.get('progress', 0)}%")
