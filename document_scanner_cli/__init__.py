"""Document Scanner CLI — Document management from your terminal."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("document-scanner-cli")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
