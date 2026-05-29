#!/usr/bin/env python3
"""Generate branded social cover images for blog posts.

Renders a 1200x630 OpenGraph "title card" for each Pelican post, matching the
site's dark GitHub-style theme, and stamps a ``Cover:`` line into the post's
front matter so the theme's OpenGraph/Twitter/JSON-LD partials pick it up.

Usage::

    python scripts/generate_covers.py                # all posts, stamp Cover:
    python scripts/generate_covers.py --force         # also overwrite existing
    python scripts/generate_covers.py --only <stem>   # single post by file stem
    python scripts/generate_covers.py --no-stamp      # render images only

Run via ``make covers``.
"""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
COVERS_DIR = CONTENT / "images" / "covers"
PROFILE = CONTENT / "images" / "profile.jpeg"
FONT_PATH = ROOT / "scripts" / "fonts" / "Inter-Variable.ttf"

# --- Brand palette (matches themes/flex variables.less) --------------------
BG = (13, 17, 23)        # #0d1117  @bg-primary
BORDER = (48, 54, 61)    # #30363d  @border-secondary
ACCENT = (88, 166, 255)  # #58a6ff  @accent
TITLE = (240, 246, 252)  # #f0f6fc  @text-heading
MUTED = (139, 148, 158)  # #8b949e  @text-muted

# --- Card geometry ---------------------------------------------------------
W, H = 1200, 630
MARGIN = 80
TITLE_TOP = 210
TITLE_AREA_H = 250
AVATAR_D = 76
TITLE_SIZES = (76, 64, 54, 46)
MAX_TITLE_LINES = 4


def font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    """Return the Inter variable font at the given size and named weight."""
    f = ImageFont.truetype(str(FONT_PATH), size)
    f.set_variation_by_name(weight)
    return f


def parse_front_matter(text: str) -> tuple[dict[str, str], int]:
    """Parse a Pelican markdown header.

    Returns a dict of the ``Key: Value`` metadata and the line index of the
    blank line that terminates the header block (where new keys are inserted).
    """
    lines = text.splitlines()
    meta: dict[str, str] = {}
    end = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            end = i
            break
        if ":" in line and not line[0].isspace():
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()
        end = i + 1
    return meta, end


def wrap(text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Greedy word-wrap ``text`` to fit within ``max_w`` pixels."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if fnt.getlength(trial) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_title(title: str, max_w: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """Pick the largest title font size whose wrapped text fits the card."""
    for size in TITLE_SIZES:
        fnt = font(size, "Bold")
        lines = wrap(title, fnt, max_w)
        line_h = int(size * 1.18)
        if len(lines) <= MAX_TITLE_LINES and len(lines) * line_h <= TITLE_AREA_H:
            return fnt, lines
    # Fallback: smallest size, hard-truncate to the line budget.
    fnt = font(TITLE_SIZES[-1], "Bold")
    lines = wrap(title, fnt, max_w)[:MAX_TITLE_LINES]
    return fnt, lines


def circular_avatar(path: Path, diameter: int) -> Image.Image | None:
    """Return a circular, center-cropped avatar, or None if unavailable."""
    if not path.exists():
        return None
    img = Image.open(path).convert("RGBA")
    side = min(img.size)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize(
        (diameter, diameter), Image.LANCZOS
    )
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    img.putalpha(mask)
    return img


def render_card(title: str, category: str) -> Image.Image:
    """Render the full cover card for one post."""
    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    # Subtle inner border.
    draw.rectangle((40, 40, W - 41, H - 41), outline=BORDER, width=2)

    # Category row: accent bar + uppercase label.
    if category:
        bar_y = 120
        draw.rectangle((MARGIN, bar_y, MARGIN + 6, bar_y + 34), fill=ACCENT)
        cat_font = font(24, "SemiBold")
        draw.text(
            (MARGIN + 22, bar_y + 2),
            category.upper(),
            font=cat_font,
            fill=ACCENT,
        )

    # Title (auto-sized, wrapped).
    title_font, lines = fit_title(title, W - 2 * MARGIN)
    line_h = int(title_font.size * 1.18)
    y = TITLE_TOP
    for line in lines:
        draw.text((MARGIN, y), line, font=title_font, fill=TITLE)
        y += line_h

    # Footer: avatar + name + domain.
    footer_y = H - MARGIN - AVATAR_D
    avatar = circular_avatar(PROFILE, AVATAR_D)
    text_x = MARGIN
    if avatar is not None:
        card.paste(avatar, (MARGIN, footer_y), avatar)
        text_x = MARGIN + AVATAR_D + 24
    name_font = font(28, "SemiBold")
    domain_font = font(22, "Regular")
    draw.text((text_x, footer_y + 8), "Ashley Kleynhans", font=name_font, fill=TITLE)
    draw.text((text_x, footer_y + 44), "trapdoor.cloud", font=domain_font, fill=ACCENT)

    return card


def stamp_cover(path: Path, cover_rel: str, force: bool) -> str:
    """Insert/update the ``Cover:`` metadata line in a post. Returns status."""
    text = path.read_text(encoding="utf-8")
    meta, end = parse_front_matter(text)
    if "cover" in meta and not force:
        return "kept"
    lines = text.splitlines()
    cover_line = f"Cover: {cover_rel}"
    # Drop any existing Cover line in the header (for --force).
    header = [
        ln for ln in lines[:end]
        if not ln.lower().startswith("cover:")
    ]
    new_lines = header + [cover_line] + lines[end:]
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return "stamped"


def post_files(only: str | None) -> list[Path]:
    """Return dated post markdown files, optionally filtered to one stem."""
    files = sorted(CONTENT.glob("20*/**/*.md"))
    if only:
        files = [f for f in files if f.stem == only]
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing Cover: lines and images")
    parser.add_argument("--only", metavar="STEM",
                        help="process a single post by its file stem")
    parser.add_argument("--no-stamp", action="store_true",
                        help="render images only; do not edit posts")
    args = parser.parse_args()

    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    files = post_files(args.only)
    if not files:
        print("No matching posts found.")
        return

    for path in files:
        meta, _ = parse_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title", path.stem)
        category = meta.get("category", "")
        out = COVERS_DIR / f"{path.stem}.png"
        render_card(title, category).save(out, "PNG")
        status = "rendered"
        if not args.no_stamp:
            status = stamp_cover(path, f"images/covers/{path.stem}.png", args.force)
        print(f"{out.relative_to(ROOT)}  [{status}]  {title}")


if __name__ == "__main__":
    main()
