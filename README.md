# Osmosis

An experimental Stable Diffusion frontend.

> This project is **not production ready!** For a more actively developed and advanced project, check out [InvokeAI](https://github.com/invoke-ai/InvokeAI) :p

## Features

- [x] Diffusers models
- [ ] CoreML models (macOS)
- [ ] Checkpoint file models
- [x] [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) upscaling
- [ ] [GFPGAN](https://github.com/TencentARC/GFPGAN) face restoration
- [x] Structured metadata according to https://github.com/invoke-ai/InvokeAI/issues/266
- [ ] Gallery view
- [ ] Image to image
- [ ] Training with [LoRA](https://huggingface.co/docs/diffusers/training/lora) / [Textual Inversion](https://huggingface.co/docs/diffusers/training/text_inversion) / [Dreambooth](https://huggingface.co/docs/diffusers/training/dreambooth)

## Installation

Osmosis is a CLI distributed as [a package on PyPI](https://pypi.org/project/osmosis/).

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
