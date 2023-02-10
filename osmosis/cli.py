from .backend.server import OsmosisServer
from .backend.config import Config
from .backend.utils import fix_torch_funcs_mps

import typer

import sys
import os

if sys.platform == "darwin":
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


fix_torch_funcs_mps()


def main(
    port: int = 26538, data_dir: str | None = None, outputs_dir: str | None = None
):
    Config.DATA_DIR = data_dir or Config.DATA_DIR
    Config.OUTPUTS_DIR = outputs_dir or Config.OUTPUTS_DIR

    server = OsmosisServer(port=port)
    server.start()


def cli():
    typer.run(main)


if __name__ == "__main__":
    cli()
