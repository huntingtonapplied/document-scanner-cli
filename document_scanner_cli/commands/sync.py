"""document-scanner sync — manage synchronization."""

import click
from document_scanner_cli.api import DocumentScannerClient, AuthError, APIError
from document_scanner_cli.output import get_console, is_json, print_json
from document_scanner_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def sync(ctx):
    """Manage synchronization."""
    pass


@sync.command("status")
@click.pass_context
def sync_status(ctx):
    """Get sync status."""
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
        status = client.get_sync_status()
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
    console.print("[bold]Sync Status[/bold]")
    console.print(f"  Status: {status.get('status', '')}")
    console.print(f"  Last Sync: {status.get('last_sync', 'N/A')}")


@sync.command("trigger")
@click.pass_context
def sync_trigger(ctx):
    """Trigger a manual sync."""
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
        result = client.trigger_sync()
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
    console.print("✓ Sync triggered")


@sync.command("settings")
@click.pass_context
def sync_settings(ctx):
    """Get sync settings."""
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
        settings = client.get_sync_settings()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(settings)
        return

    console = get_console(ctx)
    console.print("[bold]Sync Settings[/bold]")
    console.print(f"  Auto Sync: {settings.get('auto_sync', False)}")
    console.print(f"  Interval: {settings.get('interval', 'N/A')}")
