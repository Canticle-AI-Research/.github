#!/usr/bin/env python3
"""Render the Canticle profile hero's RGB neural-sparkle GIF."""

from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
SOURCE = ASSETS / "canticle-hero-ghost.png"
OUTPUT = ASSETS / "canticle-hero-ghost.gif"
SIZE = (960, 400)
FRAMES = 48
FPS = 6
SPECTRUM = [
    (247, 118, 142),  # red
    (255, 158, 100),  # orange
    (224, 175, 104),  # yellow
    (158, 206, 106),  # mint
    (125, 207, 255),  # cyan
    (122, 162, 247),  # blue
    (196, 167, 231),  # lavender
    (247, 118, 142),  # close the cycle
]

# The glow stays confined to the cybernetic shell, away from skin and hair.
ARMOR_REGIONS = [
    [(775, 91), (868, 83), (906, 151), (845, 190), (776, 151)],
    [(789, 198), (861, 205), (874, 303), (796, 311), (765, 253)],
    [(713, 283), (861, 288), (888, 399), (705, 399)],
    [(859, 277), (959, 274), (959, 399), (884, 399)],
]

NETWORKS = [
    [(802, 109), (823, 123), (846, 105), (862, 139), (835, 157), (878, 166)],
    [(815, 220), (837, 239), (812, 261), (846, 280), (824, 298)],
    [(759, 315), (790, 300), (812, 329), (842, 317), (863, 356)],
    [(882, 304), (909, 322), (937, 303), (929, 348), (902, 371), (948, 377)],
]

SEAM_SQUARES = [
    ((38, 312, 149, 369), (228, 120, 208)),  # RAW
    ((177, 312, 288, 369), (196, 167, 231)),  # MIRL
    ((316, 312, 427, 369), (115, 218, 202)),  # SQLite
    ((455, 312, 567, 369), (125, 207, 255)),  # PACK
]


def hue_color(position: float) -> tuple[int, int, int]:
    """Interpolate through the canonical Canticle RGB-cycle stops."""
    scaled = (position % 1.0) * (len(SPECTRUM) - 1)
    index = min(int(scaled), len(SPECTRUM) - 2)
    blend = scaled - index
    start = SPECTRUM[index]
    end = SPECTRUM[index + 1]
    return tuple(round(a + (b - a) * blend) for a, b in zip(start, end))


def armor_mask() -> Image.Image:
    mask = Image.new("L", SIZE, 0)
    draw = ImageDraw.Draw(mask)
    for polygon in ARMOR_REGIONS:
        draw.polygon(polygon, fill=132)
    return mask.filter(ImageFilter.GaussianBlur(7))


def logo_mask(base: Image.Image) -> Image.Image:
    """Select the colored Canticle lockup without tinting its dark ground."""
    hsv = base.convert("RGB").convert("HSV")
    saturation = hsv.getchannel("S").point(lambda value: 255 if value > 55 else 0)
    value = hsv.getchannel("V").point(lambda level: 255 if level > 70 else 0)
    colored = ImageChops.multiply(saturation, value)
    region = Image.new("L", SIZE, 0)
    ImageDraw.Draw(region).rectangle((18, 17, 262, 82), fill=255)
    return ImageChops.multiply(colored, region).filter(ImageFilter.GaussianBlur(0.8))


def add_armor_cycle(base: Image.Image, phase: float, mask: Image.Image) -> Image.Image:
    color = hue_color(phase)
    screen_color = Image.new("RGB", SIZE, color)
    screened = ImageChops.screen(base.convert("RGB"), screen_color)
    strength = 0.17 + 0.07 * (0.5 + 0.5 * math.sin(phase * math.tau))
    frame_mask = mask.point(lambda value: round(value * strength))
    return Image.composite(screened, base.convert("RGB"), frame_mask).convert("RGBA")


def add_logo_cycle(frame: Image.Image, phase: float, mask: Image.Image) -> Image.Image:
    color = hue_color(phase * 2)
    solid = Image.new("RGB", SIZE, color)
    frame_mask = mask.point(lambda value: round(value * 0.90))
    colored = Image.composite(solid, frame.convert("RGB"), frame_mask)
    glow = mask.filter(ImageFilter.GaussianBlur(7)).point(lambda value: round(value * 0.55))
    glow_layer = Image.new("RGBA", SIZE, (*color, 0))
    glow_layer.putalpha(glow)
    return Image.alpha_composite(colored.convert("RGBA"), glow_layer)


def add_seam_square_breath(frame: Image.Image, phase: float) -> Image.Image:
    """Pulse the real SEAM memory stages without changing their assigned colors."""
    result = frame.convert("RGB")
    for index, (bounds, color) in enumerate(SEAM_SQUARES):
        pulse = 0.5 - 0.5 * math.cos(math.tau * (phase * 2 + index * 0.11))
        core = Image.new("L", SIZE, 0)
        ImageDraw.Draw(core).rounded_rectangle(
            bounds, radius=7, fill=48, outline=255, width=2
        )
        halo = core.filter(ImageFilter.GaussianBlur(10))
        glow_alpha = halo.point(lambda value: round(value * (0.18 + 0.72 * pulse)))
        glow_layer = Image.new("RGBA", SIZE, (*color, 0))
        glow_layer.putalpha(glow_alpha)
        result = Image.alpha_composite(result.convert("RGBA"), glow_layer).convert("RGB")
        core_alpha = core.point(lambda value: round(value * (0.10 + 0.52 * pulse)))
        result = Image.composite(Image.new("RGB", SIZE, color), result, core_alpha)
    return result.convert("RGBA")


def add_neural_sparkles(frame: Image.Image, phase: float) -> Image.Image:
    lines = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    line_draw = ImageDraw.Draw(lines)
    glow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    stars = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(stars)

    node_index = 0
    for network_index, nodes in enumerate(NETWORKS):
        for start, end in zip(nodes, nodes[1:]):
            color = hue_color(phase + network_index * 0.17)
            pulse = 0.5 + 0.5 * math.sin(
                math.tau * (phase * 1.7 + network_index * 0.21)
            )
            line_draw.line([start, end], fill=(*color, round(35 + 55 * pulse)), width=1)

        for x, y in nodes:
            local = (phase + node_index * 0.113) % 1.0
            pulse = max(0.0, math.sin(math.tau * local)) ** 3
            color = hue_color(phase + node_index * 0.071)
            radius = 2 + round(3 * pulse)
            glow_draw.ellipse(
                (x - radius * 2, y - radius * 2, x + radius * 2, y + radius * 2),
                fill=(*color, round(65 + 150 * pulse)),
            )
            star_draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(*color, 255))
            if pulse > 0.62:
                length = 3 + round(5 * pulse)
                alpha = round(130 + 125 * pulse)
                star_draw.line((x - length, y, x + length, y), fill=(*color, alpha), width=1)
                star_draw.line((x, y - length, x, y + length), fill=(*color, alpha), width=1)
            node_index += 1

    glow = glow.filter(ImageFilter.GaussianBlur(5))
    frame = Image.alpha_composite(frame, lines)
    frame = Image.alpha_composite(frame, glow)
    return Image.alpha_composite(frame, stars)


def add_live_border(frame: Image.Image, phase: float) -> Image.Image:
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    color = hue_color(phase)
    draw.rounded_rectangle((1, 1, 958, 398), radius=14, outline=(*color, 155), width=2)
    return Image.alpha_composite(frame, overlay)


def main() -> None:
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    base = Image.open(SOURCE).convert("RGBA").resize(SIZE, resampling)
    armor = armor_mask()
    logo = logo_mask(base)

    with tempfile.TemporaryDirectory(prefix="canticle-hero-") as temporary:
        frame_dir = Path(temporary)
        for index in range(FRAMES):
            phase = index / FRAMES
            frame = add_armor_cycle(base, phase, armor)
            frame = add_logo_cycle(frame, phase, logo)
            frame = add_seam_square_breath(frame, phase)
            frame = add_neural_sparkles(frame, phase)
            frame = add_live_border(frame, phase)
            frame.convert("RGB").save(frame_dir / f"frame-{index:03d}.png", optimize=True)

        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-framerate", str(FPS), "-i", str(frame_dir / "frame-%03d.png"),
                "-filter_complex",
                "[0:v]split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];"
                "[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                "-loop", "0", str(OUTPUT),
            ],
            check=True,
        )

    print(f"rendered {FRAMES} frames at {FPS} fps -> {OUTPUT}")


if __name__ == "__main__":
    main()
