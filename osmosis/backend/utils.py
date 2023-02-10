import torch


# Copyright (c) 2022 Lincoln D. Stein (https://github.com/lstein)
# Derived from source code carrying the following copyrights
# Copyright (c) 2022 Machine Vision and Learning Group, LMU Munich
# Copyright (c) 2022 Robin Rombach and Patrick Esser and contributors
def fix_torch_funcs_mps():
    def fix_func(orig):
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():

            def new_func(*args, **kw):
                device = kw.get("device", "mps")
                kw["device"] = "cpu"
                return orig(*args, **kw).to(device)

            return new_func
        return orig

    torch.rand = fix_func(torch.rand)
    torch.rand_like = fix_func(torch.rand_like)
    torch.randn = fix_func(torch.randn)
    torch.randn_like = fix_func(torch.randn_like)
    torch.randint = fix_func(torch.randint)
    torch.randint_like = fix_func(torch.randint_like)
    torch.bernoulli = fix_func(torch.bernoulli)
    torch.multinomial = fix_func(torch.multinomial)


def auto_device():
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def pad_int(a: int, l: int):
    return str(a).zfill(l)
