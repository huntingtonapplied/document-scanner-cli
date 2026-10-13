"""document-scanner metrics — view metrics and dashboard."""

import click
from document_scanner_cli.api import DocumentScannerClient, AuthError, APIError
from document_scanner_cli.output import get_console, is_json, print_json
from document_scanner_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def metrics(ctx):
    """View metrics and dashboard."""
    pass


@metrics.command("dashboard")
@click.pass_context
def metrics_dashboard(ctx):
    """Get dashboard summary."""
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
        data = client.get_dashboard()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    console.print("[bold]Dashboard Summary[/bold]")
    console.print(f"  Total Documents: {data.get('total_documents', 'N/A')}")
    console.print(f"  Processed: {data.get('processed', 'N/A')}")
    console.print(f"  Pending: {data.get('pending', 'N/A')}")


@metrics.command("counts")
@click.pass_context
def metrics_counts(ctx):
    """Get platform counts."""
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
        data = client.get_metrics_counts()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    console.print("[bold]Platform Counts[/bold]")
    console.print(f"  Users: {data.get('users', 'N/A')}")
    console.print(f"  Documents: {data.get('documents', 'N/A')}")


@metrics.command("documents")
@click.pass_context
def metrics_documents(ctx):
    """Get document metrics."""
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
        data = client.get_metrics_documents()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    console.print("[bold]Document Metrics[/bold]")
    console.print(f"  Total: {data.get('total', 'N/A')}")
    console.print(f"  By Status: {data.get('by_status', {})}")
