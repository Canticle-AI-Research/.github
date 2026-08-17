#!/usr/bin/env python3
"""Render subtle breathing-glow GIFs for the Canticle profile link panels."""

from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "profile" / "assets" / "links"
FRAMES = 24
FPS = 6
PANELS = {
    "website": (115, 218, 202),
    "research": (228, 120, 208),
    "documentation": (196, 167, 231),
    "lab-notes": (125, 207, 255),
    "projects": (115, 218, 202),
    "benchmarks": (224, 175, 104),
    "contact": (255, 158, 100),
}


def accent_mask(image: Image.Image, accent: tuple[int, int, int]) -> Image.Image:
    """Select pixels already belonging to the panel's accent system."""
    rgb = image.convert("RGB")
    pixels = rgb.load()
    mask = Image.new("L", rgb.size, 0)
    selected = mask.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = pixels[x, y]
            distance = math.sqrt(
                (red - accent[0]) ** 2
                + (green - accent[1]) ** 2
                + (blue - accent[2]) ** 2
            )
            if distance < 118 and max(red, green, blue) > 74:
                selected[x, y] = round(255 * (1 - distance / 118))
    return mask


def render_panel(name: str, accent: tuple[int, int, int]) -> None:
    source = LINKS / f"{name}.png"
    output = LINKS / f"{name}.gif"
    base = Image.open(source).convert("RGB")
    core = accent_mask(base, accent)
    edge = Image.new("L", base.size, 0)
    edge_draw = ImageDraw.Draw(edge)
    edge_draw.rounded_rectangle((2, 2, 597, 177), radius=14, outline=185, width=2)
    edge_draw.rectangle((4, 6, 10, 173), fill=230)
    core = ImageChops.lighter(core, edge)
    halo = core.filter(ImageFilter.GaussianBlur(15))

    with tempfile.TemporaryDirectory(prefix=f"canticle-{name}-") as temporary:
        frame_dir = Path(temporary)
        for index in range(FRAMES):
            phase = index / FRAMES
            breath = 0.5 - 0.5 * math.cos(phase * math.tau)
            halo_alpha = halo.point(lambda value: round(value * (0.10 + 0.78 * breath)))
            halo_layer = Image.new("RGBA", base.size, (*accent, 0))
            halo_layer.putalpha(halo_alpha)
            frame = Image.alpha_composite(base.convert("RGBA"), halo_layer).convert("RGB")
            core_alpha = core.point(lambda value: round(value * (0.08 + 0.62 * breath)))
            frame = Image.composite(Image.new("RGB", base.size, accent), frame, core_alpha)
            frame.save(frame_dir / f"frame-{index:03d}.png", optimize=True)

        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-framerate", str(FPS), "-i", str(frame_dir / "frame-%03d.png"),
                "-filter_complex",
                "[0:v]split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];"
                "[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                "-loop", "0", str(output),
            ],
            check=True,
        )
    print(f"rendered {name}: {FRAMES} frames at {FPS} fps")


def main() -> None:
    for name, accent in PANELS.items():
        render_panel(name, accent)


if __name__ == "__main__":
    main()
