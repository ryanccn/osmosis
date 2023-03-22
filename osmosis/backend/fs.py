from osmosis.backend.config import Config
from osmosis.backend.utils import pad_int

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


def read_image_metadata(name: str):
    path = os.path.join(Config.OUTPUTS_DIR, name)
    if not os.path.exists(path):
        return None

    image = Image.open(path)
    if image.text and image.text.get("sd-metadata", None):
        data = json.loads(image.text["sd-metadata"])
        image.close()
        return data

    image.close()
    return None


def delete_image(name: str):
    path = os.path.join(Config.OUTPUTS_DIR, name)
    if os.path.exists(path):
        os.remove(path)


MODELS_CONFIG_PATH = os.path.join(Config.DATA_DIR, "models.json")


def load_models():
    try:
        with open(MODELS_CONFIG_PATH, "r") as f:
            data = json.load(f)

            for internal_id in data:
                data_id = data[internal_id].get("id", None)
                data_path = data[internal_id].get("path", None)

                if data_id and os.path.exists(data_id) is not None:
                    data[internal_id]["displayName"] = os.path.basename(data_id)
                elif data_path and os.path.exists(data_path) is not None:
                    data[internal_id]["displayName"] = os.path.basename(data_path)
                else:
                    data[internal_id]["displayName"] = data[internal_id].get(
                        "id", data[internal_id].get("path", None)
                    )

            return data

    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        save_models({})
        return {}


def save_models(data):
    with open(MODELS_CONFIG_PATH, "w") as f:
        json.dump(data, f)
