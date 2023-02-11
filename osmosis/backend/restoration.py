from PIL import Image
import torch
import numpy as np

from urllib import request
from tqdm import tqdm

from osmosis.backend.config import Config
import os


def check_download(url: str, file_path: str):
    if os.path.exists(file_path):
        return

    progress = None

    def request_hook(a: int, b: int, c: int):
        nonlocal progress
        if not progress:
            progress = tqdm(
                unit_scale=True,
                unit="B",
                desc=f"[restoration] Downloading {file_path.split('/')[-1]}",
            )
            progress.total = c

        progress.update(b)

    try:
        request.urlretrieve(
            url,
            file_path,
            request_hook,
        )
    except KeyboardInterrupt as e:
        os.remove(file_path)
        raise e


class RealESRGAN:
    net = None
    scales: str
    file_paths: list[str] = []

    def __init__(self):
        from realesrgan.archs.srvgg_arch import SRVGGNetCompact

        self.scales = [2, 4]

        download_urls = {
            "realesr-general-x4v3.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
            "realesr-general-wdn-x4v3.pth": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
        }

        self.net = SRVGGNetCompact(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_conv=32,
            upscale=4,
            act_type="prelu",
        )

        for file in download_urls:
            abs_file_path = os.path.join(Config.ESRGAN_MODELS_DIR, file)
            check_download(download_urls[file], abs_file_path)
            self.file_paths.append(abs_file_path)

    def upscale(self, image, scale):
        from realesrgan import RealESRGANer

        upsampler = RealESRGANer(
            scale=4,
            model_path=self.file_paths,
            dni_weight=[0.75, 0.25],
            model=self.net,
            tile=400,
            tile_pad=10,
            pre_pad=0,
            half=torch.cuda.is_available(),
        )

        image = image.convert("RGB")

        bgr_image = np.array(image, dtype=np.uint8)[..., ::-1]

        output, _ = upsampler.enhance(
            bgr_image, outscale=scale, alpha_upsampler="realesrgan"
        )

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        upsampler = None

        return Image.fromarray(output[..., ::-1])


class GFPGAN:
    def __init__(self):
        file = "GFPGANv1.4.pth"
        url = "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth"

        abs_file_path = os.path.join(Config.GFPGAN_MODELS_DIR, file)
        check_download(url, abs_file_path)
        self.file_path = abs_file_path

    def restore(self, image, strength):
        from gfpgan import GFPGANer

        # GFPGAN downloads its own weights into the current working directory, thus the preposterous workaround
        cwd = os.getcwd()
        os.chdir(Config.DATA_DIR)

        upsampler = GFPGANer(
            model_path=self.file_path,
            upscale=1,
            arch="clean",
            channel_multiplier=2,
            bg_upsampler=None,
        )

        image = image.convert("RGB")

        bgr_image = np.array(image, dtype=np.uint8)[..., ::-1]

        _, _, output = upsampler.enhance(bgr_image, paste_back=True, weight=strength)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        upsampler = None
        os.chdir(cwd)

        return Image.fromarray(output[..., ::-1])
