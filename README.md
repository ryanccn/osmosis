# Osmosis

[![PyPI](https://img.shields.io/pypi/v/osmosis?style=flat-square)](https://pypi.org/project/osmosis/) [![License](https://img.shields.io/github/license/ryanccn/osmosis?style=flat-square)](https://github.com/ryanccn/osmosis/blob/main/LICENSE)

An experimental Stable Diffusion web frontend.

> **Warning**
> This project is **not production ready!** For a more actively developed and advanced project, check out [InvokeAI](https://github.com/invoke-ai/InvokeAI) :p

## Features

- [x] [Diffusers](https://huggingface.co/docs/diffusers/index) models
- [x] [CoreML models](https://github.com/apple/ml-stable-diffusion) (macOS)
- [x] Custom scheduler support
- [x] Half-precision (`fp16`) support for main models
- [ ] [Diffusers to CoreML model conversion](https://github.com/apple/ml-stable-diffusion#-converting-models-to-core-ml)
- [x] [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) upscaling
- [x] [GFPGAN](https://github.com/TencentARC/GFPGAN) face restoration
- [x] Structured metadata according to https://github.com/invoke-ai/InvokeAI/issues/266
- [x] Gallery view
- [ ] [Image to image](https://huggingface.co/docs/diffusers/using-diffusers/img2img)
- [ ] [Inpainting](https://huggingface.co/docs/diffusers/using-diffusers/inpaint) / outpainting
- [ ] Training with [LoRA](https://huggingface.co/docs/diffusers/training/lora) / [Textual Inversion](https://huggingface.co/docs/diffusers/training/text_inversion) / [Dreambooth](https://huggingface.co/docs/diffusers/training/dreambooth)
- [x] [xFormers](https://github.com/facebookresearch/xformers) optimization
- [x] [Apple Silicon](https://huggingface.co/docs/diffusers/optimization/mps) optimization
- [x] [PyTorch 2.0](https://huggingface.co/docs/diffusers/optimization/torch2.0) optimization
- [ ] Checkpoint / [Safetensors](https://huggingface.co/docs/safetensors/index) file models (_not planned_)

## System Requirements

- Ideally, a NVIDIA or Apple Silicon GPU
- At least 10 GB of RAM
- As much disk space as your models require
- A modern browser

## Installation

Osmosis is a web app distributed as [a package on PyPI](https://pypi.org/project/osmosis/).

Ideally, use [pipx](https://pypa.github.io/pipx/) to install Osmosis in its own isolated environment. First [install pipx](https://pypa.github.io/pipx/#install-pipx), then run

```bash
$ pipx install osmosis
```

to install. Alternatively, simple use `pip` to install globally:

```bash
$ pip install [--user] osmosis
```

### NVIDIA instructions

If you're on a NVIDIA GPU, replace `osmosis` in the install scripts with `osmosis[xformers]` to enable [xFormers](https://github.com/facebookresearch/xformers) optimization support. In addition, add `--pip-args "--extra-index-url https://download.pytorch.org/whl/cu117"` to the end to install a CUDA-enabled PyTorch build.

```bash
$ pipx install 'osmosis[xformers]' --pip-args "--extra-index-url https://download.pytorch.org/whl/cu117"

# or in pip:
$ pip install [--user] 'osmosis[xformers]' --extra-index-url https://download.pytorch.org/whl/cu117
```

### Linux / AMD instructions

If you're on Linux and using an AMD GPU, you can also use [ROCm](https://docs.amd.com/)-optimized PyTorch wheels on install.

```bash
$ pipx install osmosis --pip-args "--extra-index-url https://download.pytorch.org/whl/rocm5.2"

# or in pip:
$ pip install [--user] osmosis --extra-index-url https://download.pytorch.org/whl/rocm5.2
```

### Nix Instructions

If you are on macOS, Windows with WSL2, or Linux, you can use a the Nix flake to install osmosis for any gpu.

With `nix run`:

```bash
# for NVIDIA cards
$ nix run github.com:ryanccn/osmosis#osmosis-nvidia
# for AMD cards
$ nix run github.com:ryanccn/osmosis#osmosis-amd
# Apple silicion users can install either
```

As an overlay:

```bash
{
  pkgs,
  osmosis,
  ...
}: {
  nixpkgs.overlays = [osmosis.overlays.default];
  environment.systemPackages = with pkg; [osmos-nvidia];
}
```

## Running

```
$ osmosis
```

is all you need to start the web UI.
