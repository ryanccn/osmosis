import os


def ensure_exists(path: str):
    os.makedirs(path, exist_ok=True)
    return path


class Config:
    DATA_DIR = ensure_exists(os.path.expanduser("~/.osmosis"))
    OUTPUTS_DIR = ensure_exists(os.path.join(DATA_DIR, "outputs"))
    ESRGAN_MODELS_DIR = ensure_exists(os.path.join(DATA_DIR, "esrgan"))
    GFPGAN_MODELS_DIR = ensure_exists(os.path.join(DATA_DIR, "gfpgan"))
