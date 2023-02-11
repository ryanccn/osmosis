# Osmosis

An experimental Stable Diffusion web frontend.

> **Warning**
> This project is **not production ready!** For a more actively developed and advanced project, check out [InvokeAI](https://github.com/invoke-ai/InvokeAI) :p

## Features

- [x] [Diffusers](https://huggingface.co/docs/diffusers/index) models
- [ ] [CoreML models](https://github.com/apple/ml-stable-diffusion) (macOS)
- [ ] Checkpoint / [Safetensors](https://huggingface.co/docs/safetensors/index) file models
- [x] [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) upscaling
- [ ] [GFPGAN](https://github.com/TencentARC/GFPGAN) face restoration
- [x] Structured metadata according to https://github.com/invoke-ai/InvokeAI/issues/266
- [ ] Gallery view
- [ ] [Image to image](https://huggingface.co/docs/diffusers/using-diffusers/img2img)
- [ ] [Inpainting](https://huggingface.co/docs/diffusers/using-diffusers/inpaint) / outpainting
- [ ] Training with [LoRA](https://huggingface.co/docs/diffusers/training/lora) / [Textual Inversion](https://huggingface.co/docs/diffusers/training/text_inversion) / [Dreambooth](https://huggingface.co/docs/diffusers/training/dreambooth)
- [ ] [xFormers](https://github.com/facebookresearch/xformers) optimization
- [x] [Apple Silicon](https://huggingface.co/docs/diffusers/optimization/mps) optimization

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

## Running

```
$ osmosis
```

is all you need.
