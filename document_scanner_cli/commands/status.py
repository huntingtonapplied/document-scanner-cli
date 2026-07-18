"""document-scanner status — show system status."""

import click
from rich.panel import Panel
from document_scanner_cli.api import DocumentScannerClient, AuthError, APIError
from document_scanner_cli.output import get_console, is_json, print_json
from document_scanner_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.command()
@click.pass_context
def status(ctx):
    """Show Document Scanner system status and recent activity."""
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
        docs = client.list_documents(params={"limit": 5})
        sync_status = client.get_sync_status()
        metrics = client.get_dashboard()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({
            "documents": docs[:5] if docs else [],
            "sync_status": sync_status,
            "metrics": metrics,
        })
        return

    console = get_console(ctx)

    # Documents summary
    if docs:
        click.echo(f"\nDocuments ({len(docs)} recent):")
        for d in docs[:5]:
            click.echo(f"  • {d.get('name', 'Unknown')} — {d.get('status', 'unknown')}")

    # Sync status
    if sync_status:
        click.echo(f"\nSync Status:")
        click.echo(f"  Status: {sync_status.get('status', 'N/A')}")

    # Dashboard metrics
    if metrics:
        click.echo(f"\nDashboard:")
        click.echo(f"  Total Documents: {metrics.get('total_documents', 'N/A')}")
