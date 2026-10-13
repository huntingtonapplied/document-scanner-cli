"""document-scanner documents — manage documents."""

import click
from rich.table import Table
from document_scanner_cli.api import DocumentScannerClient, AuthError, APIError
from document_scanner_cli.output import get_console, is_json, print_json
from document_scanner_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def documents(ctx):
    """Manage documents."""
    pass


@documents.command("list")
@click.option("--limit", "-n", default=20, show_default=True, help="Max results to return")
@click.option("--status", "-s", default=None, help="Filter by status")
@click.option("--quiet", "-q", is_flag=True, help="Print only document IDs")
@click.pass_context
def documents_list(ctx, limit, status, quiet):
    """List documents."""
    json_mode = is_json(ctx)

    try:
        client = DocumentScannerClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    params = {"limit": limit} if limit != 20 else {}
    if status:
        params["status"] = status

    try:
        doc_list = client.list_documents(params=params)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(doc_list)
        return

    if not doc_list:
        click.echo("No documents found.")
        return

    if quiet:
        for d in doc_list:
            click.echo(d.get("id", ""))
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Status", min_width=12)
    table.add_column("ID", style="dim")

    for d in doc_list:
        table.add_row(
            d.get("name", "Unknown")[:36],
            d.get("status", "unknown"),
            d.get("id", "")[:8],
        )

    console.print(table)


@documents.command("get")
@click.argument("document_id")
@click.pass_context
def documents_get(ctx, document_id):
    """Get details of a specific document."""
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
        doc = client.get_document(document_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(doc)
        return

    console = get_console(ctx)
    console.print(f"[bold]{doc.get('name', 'Unknown')}[/bold]")
    console.print(f"  ID: {doc.get('id', '')}")
    console.print(f"  Status: {doc.get('status', '')}")


@documents.command("delete")
@click.argument("document_id")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt")
@click.pass_context
def documents_delete(ctx, document_id, yes):
    """Delete a document."""
    json_mode = is_json(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not yes and not ci_mode:
        click.confirm(f"Delete document {document_id}? This cannot be undone.", abort=True)

    try:
        client = DocumentScannerClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        client.delete_document(document_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({"deleted": document_id})
    else:
        click.echo(f"✓ Deleted document {document_id}")
