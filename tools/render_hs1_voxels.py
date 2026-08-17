#!/usr/bin/env python3
"""Render additive HS/1 full-spectrum voxel atmosphere bands."""

from __future__ import annotations

import math
import random
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
SIZE = (960, 96)
FRAMES = 48
FPS = 6
VARIANTS = ("top",)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
PALETTE = (
    (247, 118, 142),  # red
    (255, 158, 100),  # orange
    (224, 175, 104),  # yellow
    (158, 206, 106),  # mint
    (115, 218, 202),  # green-cyan
    (125, 207, 255),  # cyan
    (122, 162, 247),  # blue
    (196, 167, 231),  # lavender
    (228, 120, 208),  # magenta
    (247, 148, 190),  # pink
)


def shade(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, round(channel * amount))) for channel in color)


def particles(seed: int) -> list[dict[str, float | int]]:
    rng = random.Random(seed)
    result: list[dict[str, float | int]] = []
    for index in range(32):
        depth = rng.uniform(0.45, 1.0)
        result.append(
            {
                "x": rng.uniform(-20, SIZE[0] + 20),
                "y": rng.choice((rng.uniform(9, 29), rng.uniform(68, SIZE[1] - 10))),
                "size": rng.uniform(3.5, 7.4) * depth,
                "speed": rng.uniform(5.0, 18.0) * depth,
                "bob": rng.uniform(1.2, 5.0),
                "offset": rng.random(),
                "depth": depth,
                "color": index % len(PALETTE),
            }
        )
    return result


def draw_voxel(
    face_layer: Image.Image,
    glow_layer: Image.Image,
    x: float,
    y: float,
    size: float,
    color: tuple[int, int, int],
    alpha: int,
) -> None:
    """Draw a tiny extruded square with light top and dark right facets."""
    face = ImageDraw.Draw(face_layer)
    glow = ImageDraw.Draw(glow_layer)
    x0, y0 = round(x), round(y)
    side = max(3, round(size))
    lift = max(2, round(side * 0.42))
    skew = max(1, round(side * 0.32))

    front = [(x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side)]
    top = [(x0, y0), (x0 + skew, y0 - lift), (x0 + side + skew, y0 - lift), (x0 + side, y0)]
    right = [(x0 + side, y0), (x0 + side + skew, y0 - lift), (x0 + side + skew, y0 + side - lift), (x0 + side, y0 + side)]

    glow.rectangle((x0 - 3, y0 - lift - 3, x0 + side + skew + 3, y0 + side + 3), fill=(*color, alpha))
    face.polygon(top, fill=(*shade(color, 1.28), min(255, alpha + 45)))
    face.polygon(right, fill=(*shade(color, 0.58), min(255, alpha + 24)))
    face.polygon(front, fill=(*color, alpha), outline=(*shade(color, 1.38), min(255, alpha + 60)))


def background() -> Image.Image:
    """Create one uninterrupted atmosphere with no grid or boxed divisions."""
    image = Image.new("RGBA", SIZE, (6, 7, 18, 255))
    bloom = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(bloom)
    draw.ellipse((-90, -115, 350, 205), fill=(247, 118, 142, 38))
    draw.ellipse((300, -135, 700, 220), fill=(196, 167, 231, 32))
    draw.ellipse((635, -120, 1060, 205), fill=(125, 207, 255, 38))
    return Image.alpha_composite(image, bloom.filter(ImageFilter.GaussianBlur(54)))


def add_tagline_lockup(frame: Image.Image) -> Image.Image:
    """Unify the three existing taglines inside the HS/1 atmosphere."""
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    glow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    font = ImageFont.truetype(FONT, 18)
    dot_font = ImageFont.truetype(FONT, 17)
    items = (
        ("GHOST IN THE SEAM", (247, 148, 190)),
        ("SEAM-BACKED AGENT", (196, 167, 231)),
        ("SOURCE-LINKED RECALL", (125, 207, 255)),
    )
    separator = "  /  "
    widths = [ImageDraw.Draw(overlay).textlength(text, font=font) for text, _ in items]
    separator_width = ImageDraw.Draw(overlay).textlength(separator, font=dot_font)
    total_width = sum(widths) + separator_width * (len(items) - 1)
    cursor = (SIZE[0] - total_width) / 2
    y = 37
    for index, ((label, color), width) in enumerate(zip(items, widths)):
        ImageDraw.Draw(glow).text((cursor, y), label, font=font, fill=(*color, 180))
        ImageDraw.Draw(overlay).text((cursor, y), label, font=font, fill=(*color, 245))
        cursor += width
        if index < len(items) - 1:
            ImageDraw.Draw(overlay).text((cursor, y), separator, font=dot_font, fill=(86, 95, 137, 210))
            cursor += separator_width
    frame = Image.alpha_composite(frame, glow.filter(ImageFilter.GaussianBlur(8)))
    return Image.alpha_composite(frame, overlay)


def render_variant(name: str, seed: int) -> None:
    field = particles(seed)
    base = background()
    gif_output = ASSETS / f"hs1-voxel-field-{name}.gif"
    png_output = ASSETS / f"hs1-voxel-field-{name}.png"

    with tempfile.TemporaryDirectory(prefix=f"hs1-{name}-") as temporary:
        frame_dir = Path(temporary)
        for frame_index in range(FRAMES):
            phase = frame_index / FRAMES
            glow_layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
            face_layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
            for particle in field:
                depth = float(particle["depth"])
                x = (float(particle["x"]) + float(particle["speed"]) * phase) % (SIZE[0] + 30) - 15
                y = float(particle["y"]) + math.sin(math.tau * (phase + float(particle["offset"]))) * float(particle["bob"])
                shimmer = 0.5 + 0.5 * math.sin(math.tau * (phase * 1.35 + float(particle["offset"])))
                alpha = round((78 + 92 * shimmer) * depth)
                draw_voxel(
                    face_layer,
                    glow_layer,
                    x,
                    y,
                    float(particle["size"]),
                    PALETTE[int(particle["color"])],
                    alpha,
                )

            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(5))
            frame = Image.alpha_composite(base, glow_layer)
            frame = Image.alpha_composite(frame, face_layer)
            frame = add_tagline_lockup(frame).convert("RGB")
            frame.save(frame_dir / f"frame-{frame_index:03d}.png", optimize=True)
            if frame_index == 12:
                frame.save(png_output, optimize=True)

        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-framerate", str(FPS), "-i", str(frame_dir / "frame-%03d.png"),
                "-filter_complex",
                "[0:v]split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];"
                "[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                "-loop", "0", str(gif_output),
            ],
            check=True,
        )
    print(f"rendered HS/1 {name} -> {gif_output}")


def main() -> None:
    for offset, name in enumerate(VARIANTS):
        render_variant(name, 0x485331 + offset * 101)


if __name__ == "__main__":
    main()
