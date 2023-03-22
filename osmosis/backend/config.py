import os


def ensure_exists(path: str):
    os.makedirs(path, exist_ok=True)
    return path


class Config:
    DATA_DIR = ensure_exists(os.path.expanduser("~/.osmosis"))
    OUTPUTS_DIR = ensure_exists(os.path.join(DATA_DIR, "outputs"))
    ESRGAN_MODELS_DIR = ensure_exists(os.path.join(DATA_DIR, "esrgan"))
    GFPGAN_MODELS_DIR = ensure_exists(os.path.join(DATA_DIR, "gfpgan"))

    SHOW_STEP_LATENTS = False
    SAFETY_CHECKER = False
    EXPERIMENTAL_TORCH_COMPILE = False

    MODEL_CPU_OFFLOAD = False
    SEQUENTIAL_CPU_OFFLOAD = False

    DEBUG = True if os.environ.get("DEBUG", None) == "1" else False
