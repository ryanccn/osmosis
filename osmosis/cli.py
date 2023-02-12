from osmosis.backend.server import OsmosisServer
from osmosis.backend.config import Config
from osmosis.backend.utils import fix_torch_funcs_mps

import click

import sys
import os

if sys.platform == "darwin":
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


fix_torch_funcs_mps()


@click.command()
@click.option("-p", "--port", default=26538, help="Port to use for the web app")
@click.option(
    "-d",
    "--data_dir",
    default=None,
    help="Data directory for storing outputs",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, writable=True),
)
def main(port: int = 26538, data_dir: str | None = None):
    """Osmosis is an experimental Stable Diffusion web frontend."""
    Config.DATA_DIR = data_dir or Config.DATA_DIR

    server = OsmosisServer(port=port)
    server.start()


if __name__ == "__main__":
    main()
