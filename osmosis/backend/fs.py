from .config import Config
from .utils import pad_int

from PIL import PngImagePlugin, Image

import json
import datetime
import json
import os


def save_image(image: Image.Image, metadata=None) -> str:
    now = datetime.datetime.now()
    output_filename = f"{pad_int(now.year, 4)}-{pad_int(now.month, 2)}-{pad_int(now.day, 2)} {pad_int(now.hour, 2)}.{pad_int(now.minute, 2)}.{pad_int(now.second, 2)}.png"
    path = os.path.join(Config.OUTPUTS_DIR, output_filename)

    while os.path.exists(path):
        path = path.replace(".png", " 1.png")

    info = PngImagePlugin.PngInfo()
    if metadata:
        info.add_text("sd-metadata", json.dumps(metadata))

    image.save(path, "PNG", pnginfo=info, compress_level=6)

    return path


MODELS_CONFIG_PATH = os.path.join(Config.DATA_DIR, "models.json")


def load_models():
    try:
        with open(MODELS_CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        save_models({})
        return {}


def save_models(data):
    with open(MODELS_CONFIG_PATH, "w") as f:
        json.dump(data, f)
