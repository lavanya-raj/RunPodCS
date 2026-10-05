import os
import base64
from io import BytesIO

import runpod
import torch
from diffusers import FluxPipeline

MODEL_ID = "black-forest-labs/FLUX.1-dev"

pipe = FluxPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    local_files_only=True,
)
pipe.enable_model_cpu_offload()


def handler(job):
    job_input = job.get("input", {}) or {}
    prompt = job_input.get("prompt")
    if not prompt:
        return {"error": "Missing required field: prompt"}

    height = int(job_input.get("height", 1024))
    width = int(job_input.get("width", 1024))
    steps = int(job_input.get("num_inference_steps", 28))
    guidance = float(job_input.get("guidance_scale", 3.5))
    seed = int(job_input.get("seed", 0))

    image = pipe(
        prompt,
        height=height,
        width=width,
        guidance_scale=guidance,
        num_inference_steps=steps,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(seed),
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": img_str}


runpod.serverless.start({"handler": handler})
