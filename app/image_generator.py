"""Panel illustrations: Stable Diffusion if installed, otherwise a PIL placeholder."""
import hashlib
import os
import random
import re

from PIL import Image, ImageDraw

from app import config

PANEL_DIR = os.path.join("static", "panels")
_pipe = None


def _safe_name(text):
    return re.sub(r"[^a-zA-Z0-9]+", "_", text)[:40].strip("_") or "panel"


def _load_pipe():
    global _pipe
    if _pipe is None:
        import torch
        from diffusers import StableDiffusionPipeline

        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        _pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=dtype, token=config.HF_API_KEY or None
        ).to(device)
    return _pipe


def _placeholder(prompt, path, title=""):
    rnd = random.Random(prompt)
    img = Image.new("RGB", (512, 512))
    d = ImageDraw.Draw(img)
    top = tuple(rnd.randint(40, 200) for _ in range(3))
    bot = tuple(rnd.randint(40, 200) for _ in range(3))
    for y in range(512):
        t = y / 511
        d.line([(0, y), (512, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    for _ in range(6):
        x, y, r = rnd.randint(0, 512), rnd.randint(250, 512), rnd.randint(60, 160)
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(rnd.randint(20, 120) for _ in range(3)))
    d.rectangle([0, 0, 511, 511], outline=(20, 20, 20), width=8)
    d.rectangle([16, 16, 496, 60], fill=(255, 235, 59))
    d.text((26, 30), (title or "Demo panel")[:52], fill=(0, 0, 0))
    img.save(path)


def generate_image(prompt, title=""):
    os.makedirs(PANEL_DIR, exist_ok=True)
    digest = hashlib.md5(prompt.encode()).hexdigest()[:8]
    path = os.path.join(PANEL_DIR, f"{_safe_name(prompt)}_{digest}.png")
    if os.path.exists(path):
        return path
    if config.FORCE_DEMO:
        _placeholder(prompt, path, title)
        return path
    try:
        _load_pipe()(prompt, num_inference_steps=25).images[0].save(path)
    except Exception:  # diffusers/torch missing or no GPU -> graceful fallback
        _placeholder(prompt, path, title)
    return path
