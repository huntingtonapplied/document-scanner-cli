"""Shell completion for Document Scanner CLI."""

import click


@click.command()
@click.argument("shell", required=False, type=click.Choice(["bash", "zsh", "fish"], case_sensitive=False))
@click.pass_context
def completion(ctx, shell):
    """Generate shell completion script.

    \b
    Examples:
        document-scanner completion bash > ~/.bashrc
        document-scanner completion zsh >> ~/.zshrc
        document-scanner completion fish > ~/.config/fish/config.fish
    """
    if shell is None:
        import os
        shell = _detect_shell()

    if shell == "bash":
        click.echo("eval \"$(_DOCUMENT_SCANNER_COMPLETE=bash_source document-scanner)\"")
    elif shell == "zsh":
        click.echo("eval \"$(_DOCUMENT_SCANNER_COMPLETE=zsh_source document-scanner)\"")
    elif shell == "fish":
        click.echo("eval (env _DOCUMENT_SCANNER_COMPLETE=fish_source document-scanner)")


def _detect_shell():
    import os
    shell = os.path.basename(os.getenv("SHELL", ""))
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    return "bash"
