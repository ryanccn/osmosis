from diffusers import (
    DDIMScheduler,
    PNDMScheduler,
    DDPMScheduler,
    LMSDiscreteScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
)

schedulers = {}
for scheduler in [
    DDIMScheduler,
    PNDMScheduler,
    DDPMScheduler,
    LMSDiscreteScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
]:
    schedulers[scheduler().__class__.__name__.replace("Scheduler", "")] = scheduler

__all__ = ["schedulers"]
