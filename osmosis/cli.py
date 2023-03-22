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
@click.option(
    "--show-step-latents",
    is_flag=True,
    help="Show in-progress images during generation",
)
@click.option(
    "--safety-checker",
    is_flag=True,
    help="Turn on the safety checker (filtered images will be black, will increase VRAM usage)",
)
@click.option(
    "--model-cpu-offload",
    is_flag=True,
    help="Offloads all models to CPU using accelerate, reducing memory usage with a low impact on performance",
)
@click.option(
    "--sequential-cpu-offload",
    is_flag=True,
    help="Offloads all models to CPU and load on a submodule basis for each, reducing more memory usage but with a larger performance impact",
)
@click.option(
    "--experimental-torch-compile",
    is_flag=True,
    help="Use Pytorch 2.0 compilation optimization",
)
def main(
    port: int = 26538,
    data_dir: str | None = None,
    show_step_latents=None,
    safety_checker=None,
    model_cpu_offload=None,
    sequential_cpu_offload=None,
    experimental_torch_compile=None,
):
    """Osmosis is an experimental Stable Diffusion web frontend."""
    Config.DATA_DIR = data_dir or Config.DATA_DIR

    if show_step_latents is not None:
        Config.SHOW_STEP_LATENTS = show_step_latents
    if experimental_torch_compile is not None:
        Config.EXPERIMENTAL_TORCH_COMPILE = experimental_torch_compile
    if model_cpu_offload is not None:
        Config.MODEL_CPU_OFFLOAD = model_cpu_offload
    if sequential_cpu_offload is not None:
        Config.SEQUENTIAL_CPU_OFFLOAD = sequential_cpu_offload
    if safety_checker is not None:
        Config.SAFETY_CHECKER = safety_checker

    server = OsmosisServer(port=port)
    server.start()


if __name__ == "__main__":
    main()
