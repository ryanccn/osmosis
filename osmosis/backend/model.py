from diffusers import StableDiffusionPipeline
from compel import Compel
from osmosis.backend.schedulers import schedulers
from osmosis.backend.restoration import RealESRGAN, GFPGAN

from flask_socketio import SocketIO

import torch
import numpy as np

from osmosis.backend.config import Config
from osmosis.backend.utils import auto_device
from osmosis import __version__

from diffusers.utils.import_utils import is_xformers_available

import eventlet
from threading import Event
import random
from rich import print

import psutil
import platform
import os
import sys
import gc


class StopRequestedException(Exception):
    pass


class OsmosisModel:
    def __init__(self, sio: SocketIO):
        self.type = None
        self.name = None

        self.diffusers_model = None
        self.coreml_model = None
        self.compel = None

        self.sio = sio

        self.stop_requested = Event()

        @self.sio.on("stop")
        def stop():
            self.stop_requested.set()

    def _unload_model(self):
        self.type = None
        self.name = None
        self.diffusers_model = None
        self.coreml_model = None
        self.compel = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    def load_diffusers(self, model_id: str, revision="main", half=False):
        self._unload_model()

        self.type = "diffusers"
        self.name = (
            model_id if not os.path.exists(model_id) else os.path.basename(model_id)
        )

        safety_checker_extra_args = (
            {} if Config.SAFETY_CHECKER else {"safety_checker": None}
        )

        self.diffusers_model = StableDiffusionPipeline.from_pretrained(
            model_id,
            revision=revision,
            torch_dtype=torch.float16 if half else torch.float32,
            **safety_checker_extra_args,
        )
        self._set_diffusers_options()

    def load_checkpoint(self, path: str, vae: str | None = None, half=False):
        self._unload_model()
        self.type = "diffusers"
        self.name = os.path.basename(path)

        from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
            load_pipeline_from_original_stable_diffusion_ckpt,
        )

        self.diffusers_model = load_pipeline_from_original_stable_diffusion_ckpt(
            path, from_safetensors=path.endswith(".safetensors")
        )
        if vae is not None:
            print("[yellow]Custom VAE is not yet supported![/yellow]")

        if not Config.SAFETY_CHECKER:
            self.diffusers_model.safety_checker = None

        self._set_diffusers_options()

    def _set_diffusers_options(self):
        low_vram = psutil.virtual_memory().total <= 16 * (2**30)

        if Config.EXPERIMENTAL_TORCH_COMPILE:
            if torch.cuda.is_available():
                self.diffusers_model.unet = torch.compile(self.diffusers_model.unet)
            else:
                print(
                    "[yellow]torch.compile() does not work without CUDA, skipping step[/yellow]",
                    file=sys.stderr,
                )

        if torch.backends.cudnn:
            torch.backends.cudnn.benchmark = True
        if torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True

        if Config.SEQUENTIAL_CPU_OFFLOAD:
            self.diffusers_model.enable_sequential_cpu_offload()
        elif Config.MODEL_CPU_OFFLOAD:
            self.diffusers_model.enable_model_cpu_offload()
        else:
            self.diffusers_model.to(auto_device())

        if is_xformers_available() and not Config.EXPERIMENTAL_TORCH_COMPILE:
            self.diffusers_model.enable_xformers_memory_efficient_attention()
        elif low_vram:
            self.diffusers_model.enable_attention_slicing()

        if low_vram:
            self.diffusers_model.enable_vae_tiling()

        self.compel = Compel(
            tokenizer=self.diffusers_model.tokenizer,
            text_encoder=self.diffusers_model.text_encoder,
        )

        if platform.system() == "Darwin":
            _ = self.diffusers_model("noop", num_inference_steps=1)

    def load_coreml(self, model_id, mlpackages_dir, scheduler=None):
        if platform.system() != "Darwin":
            raise NotImplementedError()

        from osmosis.backend.coreml.pipeline import (
            SCHEDULER_MAP,
            get_coreml_pipe,
        )

        self._unload_model()

        self.type = "coreml"
        self.name = model_id

        pytorch_pipe = StableDiffusionPipeline.from_pretrained(model_id)

        user_specified_scheduler = None
        if scheduler is not None:
            user_specified_scheduler = SCHEDULER_MAP[scheduler].from_config(
                pytorch_pipe.scheduler.config
            )

        coreml_pipe = get_coreml_pipe(
            pytorch_pipe=pytorch_pipe,
            mlpackages_dir=mlpackages_dir,
            model_version=model_id,
            compute_unit="ALL",
            scheduler_override=user_specified_scheduler,
        )

        self.coreml_model = coreml_pipe

    def check_if_stop(self):
        if self.stop_requested.is_set():
            raise StopRequestedException()

    def txt2img(self, data: dict):
        if self.type == None:
            return

        prompt = data["prompt"]
        negative_prompt = data.get("negative_prompt", None)
        steps = data.get("steps", 30)
        seed = data.get("seed", -1)
        width = data.get("width", 512)
        height = data.get("height", 512)
        scheduler_name = data.get("scheduler", "LMSDiscrete")
        scheduler = schedulers[scheduler_name]

        upscale = data.get("upscale", None)
        face_restoration = data.get("face_restoration", None)

        if not prompt:
            raise TypeError("No prompt provided!")

        if seed < 0:
            seed = random.randrange(0, np.iinfo(np.uint32).max)

        try:
            self.stop_requested.clear()

            if self.type == "diffusers":

                def diffusers_callback(
                    step: int, timestep: int, latents: torch.FloatTensor
                ):
                    self.check_if_stop()

                    step_image = None

                    if Config.SHOW_STEP_LATENTS:
                        import io

                        step_image = self.diffusers_model.numpy_to_pil(
                            self.diffusers_model.decode_latents(latents)
                        )[0]
                        buffered = io.BytesIO()
                        step_image.save(buffered, format="JPEG")
                        del step_image

                        from base64 import b64encode

                        step_image = f"data:image/jpeg;base64,{b64encode(buffered.getvalue()).decode('utf-8')}"
                        del buffered

                    self.sio.emit(
                        "txt2img:progress",
                        {"type": "main", "data": [step, steps], "image": step_image},
                    )
                    eventlet.sleep(0)

                    del step_image

                if not isinstance(self.diffusers_model.scheduler, scheduler):
                    self.diffusers_model.scheduler = scheduler.from_config(
                        self.diffusers_model.scheduler.config
                    )

                generator = torch.Generator(
                    device="cuda" if torch.cuda.is_available() else "cpu"
                ).manual_seed(seed)

                prompt_conditioning = self.compel(prompt)
                negative_prompt_conditioning = (
                    self.compel(negative_prompt) if negative_prompt else None
                )

                self.check_if_stop()

                output = self.diffusers_model(
                    prompt_embeds=prompt_conditioning,
                    negative_prompt_embeds=negative_prompt_conditioning,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    callback_steps=1,
                    callback=diffusers_callback,
                    generator=generator,
                ).images[0]
            elif self.type == "coreml":

                def diffusers_callback(
                    step: int, timestep: int, latents: torch.FloatTensor
                ):
                    self.check_if_stop()
                    self.sio.emit(
                        "txt2img:progress", {"type": "main", "data": [step, steps]}
                    )
                    eventlet.sleep(0)

                if not isinstance(self.coreml_model.scheduler, scheduler):
                    self.coreml_model.scheduler = scheduler.from_config(
                        self.coreml_model.scheduler.config
                    )

                np.random.seed(seed)

                self.check_if_stop()

                output = self.coreml_model(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=self.coreml_model.width,
                    height=self.coreml_model.height,
                    num_inference_steps=steps,
                    callback_steps=1,
                    callback=diffusers_callback,
                ).images[0]

                np.random.seed(None)
            else:
                raise NotImplementedError()

            self.check_if_stop()

            if upscale or face_restoration:
                self.sio.emit("txt2img:progress", {"type": "postprocessing"})
                eventlet.sleep(0)

            self.check_if_stop()

            if upscale:
                self.esrgan = RealESRGAN()
                output = self.esrgan.upscale(output, upscale)
                self.esrgan = None

            self.check_if_stop()

            if face_restoration:
                self.gfpgan = GFPGAN()
                output = self.gfpgan.restore(output, face_restoration)
                self.gfpgan = None

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

            metadata = {
                "model": "stable diffusion",
                "model_weights": self.name,
                "model_hash": None,
                "app_id": "ryanccn/osmosis",
                "app_version": __version__,
                "image": {
                    "prompt": prompt,
                    "steps": steps,
                    "cfg_scale": 7.5,
                    "threshold": 0,
                    "perlin": 0,
                    "height": height,
                    "width": width,
                    "seed": seed,
                    "seamless": False,
                    "hires_fix": False,
                    "type": "txt2img",
                    "postprocessing": [],
                    "sampler": scheduler_name,
                    "variations": [],
                },
            }

            if upscale:
                metadata["image"]["postprocessing"].append(
                    {"type": "esrgan", "scale": upscale, "strength": 0.75}
                )
            if face_restoration:
                metadata["image"]["postprocessing"].append(
                    {"type": "gfpgan", "strength": 0.5}
                )

            return {"image": output, "metadata": metadata}
        except (StopRequestedException, KeyboardInterrupt):
            print("[yellow]Stop requested, stopping![/yellow]", file=sys.stderr)
            self.gfpgan = None
            self.esrgan = None

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
