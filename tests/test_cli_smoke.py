from click.testing import CliRunner


def test_help_works():
    from document_scanner_cli.main import cli

    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_version_works():
    from document_scanner_cli.main import cli

    result = CliRunner().invoke(cli, ["--version"])
    assert result.exit_code == 0
