"""Render static PNG previews of the Settings and Gallery Rainmeter skins."""

import argparse
import math
import os
import re
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit("Pillow is required. Install it with: python -m pip install pillow") from exc


ROOT = Path(__file__).resolve().parents[1]
SETTINGS_INI = ROOT / "AdaptiveClock" / "Settings" / "Settings.ini"
GALLERY_INI = ROOT / "AdaptiveClock" / "Gallery" / "Gallery.ini"
CLOCK_INI = ROOT / "AdaptiveClock" / "AdaptiveClock.ini"
DEFAULT_OUTPUT = ROOT / "docs" / "ui-screenshots"
SCALE = 2
ACTIVE = "77,142,255,235"
INACTIVE = "255,255,255,28"
FILTERS = (
    ("all", "All"),
    ("code", "Coder"),
    ("easy", "Everyday"),
    ("girl", "Bloom"),
    ("boy", "Volt"),
    ("en", "English"),
)
SORTS = (("recent", "recent"), ("name", "a-z"))


def parse_ini(path):
    sections = {}
    current = None
    with path.open(encoding="utf-8-sig") as source:
        for raw_line in source:
            line = raw_line.strip()
            if not line or line.startswith((";", "#")):
                continue
            match = re.fullmatch(r"\[([^\]]+)\]", line)
            if match:
                current = sections.setdefault(match.group(1), {})
            elif current is not None and "=" in line:
                key, value = line.split("=", 1)
                current[key.strip()] = value.strip()
    return sections


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def expand(value, variables):
    pattern = re.compile(r"#([A-Za-z0-9_]+)#")
    for _ in range(5):
        updated = pattern.sub(lambda match: variables.get(match.group(1), ""), str(value))
        if updated == value:
            break
        value = updated
    return value


def color(value, fallback=(245, 245, 250, 255)):
    try:
        parts = [int(float(part.strip())) for part in value.split(",")]
        if len(parts) == 3:
            parts.append(255)
        if len(parts) != 4:
            return fallback
        return tuple(max(0, min(255, part)) for part in parts)
    except (AttributeError, ValueError):
        return fallback


def font_for(size, bold=False):
    font_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    filename = "segoeuib.ttf" if bold else "segoeui.ttf"
    path = font_dir / filename
    try:
        return ImageFont.truetype(str(path), max(1, round(size * SCALE)))
    except OSError:
        return ImageFont.load_default(size=max(1, round(size * SCALE)))


def text_lines(text, font, max_width, draw, wrap):
    if not max_width:
        return [text]
    if wrap:
        lines = []
        for paragraph in text.splitlines() or [""]:
            line = ""
            for word in paragraph.split():
                candidate = f"{line} {word}".strip()
                if line and draw.textlength(candidate, font=font) > max_width:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        return lines
    if draw.textlength(text, font=font) <= max_width:
        return [text]
    shortened = text
    while shortened and draw.textlength(shortened + "...", font=font) > max_width:
        shortened = shortened[:-1]
    return [shortened + "..." if shortened else ""]


def draw_shape(image, section, variables):
    x = round(number(section.get("X")) * SCALE)
    y = round(number(section.get("Y")) * SCALE)
    width = max(1, round(number(section.get("W")) * SCALE))
    height = max(1, round(number(section.get("H")) * SCALE))
    shape = expand(section.get("Shape", ""), variables)
    fill_match = re.search(r"Fill Color\s+([^|]+)", shape, re.IGNORECASE)
    fill = color(fill_match.group(1).strip(), (0, 0, 0, 0)) if fill_match else (0, 0, 0, 0)
    stroke_match = re.search(r"Stroke Color\s+([^|]+)", shape, re.IGNORECASE)
    stroke = color(stroke_match.group(1).strip()) if stroke_match else None
    stroke_width = round(number(re.search(r"StrokeWidth\s+([^|]+)", shape, re.IGNORECASE).group(1)) * SCALE) if re.search(
        r"StrokeWidth\s+([^|]+)", shape, re.IGNORECASE
    ) else 0
    radius_match = re.search(r"Rectangle\s+[^|]*?,\s*([\d.]+)\s*$", shape, re.IGNORECASE)
    radius = round(number(radius_match.group(1)) * SCALE) if radius_match else 0

    left, top = max(0, x), max(0, y)
    right, bottom = min(image.width, x + width), min(image.height, y + height)
    if left >= right or top >= bottom:
        return
    layer = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)
    box = (x - left, y - top, x + width - 1 - left, y + height - 1 - top)
    layer_draw.rounded_rectangle(
        box,
        radius=min(radius, width // 2, height // 2),
        fill=fill,
        outline=stroke if stroke_width else None,
        width=max(1, stroke_width) if stroke_width else 1,
    )
    image.alpha_composite(layer, (left, top))


def draw_string(image, section, variables):
    text = expand(section.get("Text", ""), variables)
    if not text:
        return
    x = number(section.get("X")) * SCALE
    y = number(section.get("Y")) * SCALE
    width = number(section.get("W")) * SCALE
    height = number(section.get("H")) * SCALE
    size = number(expand(section.get("FontSize", "10"), variables), 10)
    font = font_for(size, section.get("StringStyle", "").lower() == "bold")
    fill = color(expand(section.get("FontColor", "245,245,250"), variables))
    draw = ImageDraw.Draw(image)
    wrap = section.get("ClipString") == "2"
    lines = text_lines(text, font, width, draw, wrap)
    align = section.get("StringAlign", "").lower()
    multiline_align = "center" if align == "centercenter" else "right" if align == "right" else "left"
    text = "\n".join(lines)
    spacing = round(size * SCALE * 0.2)
    bounds = draw.multiline_textbbox((0, 0), text, font=font, align=multiline_align, spacing=spacing)
    text_width, text_height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    if align == "centercenter":
        x -= text_width / 2
        y -= text_height / 2
    elif align == "right":
        x -= text_width
    draw.multiline_text(
        (x - bounds[0], y - bounds[1]),
        text,
        font=font,
        fill=fill,
        align=multiline_align,
        spacing=spacing,
    )


def render_skin(sections, variables):
    background = sections.get("Bg", {})
    width = max(1, round(number(background.get("W"), 680)))
    height = max(1, round(number(background.get("H"), 640)))
    image = Image.new("RGBA", (width * SCALE, height * SCALE), (17, 20, 27, 255))
    for name, section in sections.items():
        meter = section.get("Meter", "").lower()
        if meter not in {"shape", "string"}:
            continue
        hidden = expand(section.get("Hidden", "0"), variables).strip()
        if hidden not in {"", "0", "false", "False"}:
            continue
        if meter == "shape":
            draw_shape(image, section, variables)
        else:
            draw_string(image, section, variables)
    return image.resize((width, height), Image.Resampling.LANCZOS).convert("RGB")


def settings_variables(settings, clock):
    variables = dict(settings.get("Variables", {}))
    clock_values = clock.get("Variables", {})
    page_count = int(number(variables.get("PageCount"), 0))
    for page in range(1, page_count + 1):
        variables[f"Pg{page}"] = "1"
        variables[f"Tab{page}"] = INACTIVE
    for name in ("GreetingName", "Birthday", "City", "Latitude", "Longitude",
                 "AlarmTime", "FontText", "FontMono", "CustomColor"):
        variables.setdefault(f"Input{name}", "")
        variables[f"Input{name}Label"] = variables.get(f"Input{name}") or "(click to enter)"
    variables.update({
        "NowShowing": "Now showing: (static preview)",
        "LocStatus": "Location: preview only",
        "InputStatusPersonal": "",
        "InputStatusFonts": "",
        "QuoteStatus": "",
    })

    for section_name, section in settings.items():
        match = re.fullmatch(r"Btn(\d+)", section_name)
        if not match:
            continue
        button = match.group(1)
        setting_name = variables.get(f"B{button}V", "")
        expected = variables.get(f"B{button}X", "")
        actual = clock_values.get(setting_name, "")
        if setting_name == "HourFormat":
            actual = {"%H": "H24", "%#I": "H12"}.get(actual, actual)
        if actual and actual == expected:
            variables[f"B{button}C"] = ACTIVE
            group = variables.get(f"B{button}G", "")
            if group:
                variables[f"GV{group}"] = variables.get(f"B{button}L", "")

    return variables


def render_settings(settings, clock, page):
    variables = settings_variables(settings, clock)
    page_count = int(number(variables.get("PageCount"), 0))
    if page < 1 or page > page_count:
        raise ValueError(f"Settings page {page} is outside 1..{page_count}")
    for current in range(1, page_count + 1):
        variables[f"Pg{current}"] = "0" if current == page else "1"
    variables[f"Tab{page}"] = ACTIVE
    variables["CrumbPage"] = variables.get(f"PageName{page}", "")
    variables["PageHint"] = variables.get(f"PageHint{page}", "")
    return render_skin(settings, variables)


def gallery_styles(gallery):
    variables = gallery.get("Variables", {})
    count = int(number(variables.get("BtnCount"), 0))
    styles = []
    for style_id in range(1, count + 1):
        styles.append({
            "id": style_id,
            "name": variables.get(f"B{style_id}L", f"Style {style_id}"),
            "tag": variables.get(f"B{style_id}T", ""),
        })
    return styles


def render_gallery(sections, all_styles, tag, sort, page):
    variables = dict(sections.get("Variables", {}))
    filtered = [style for style in all_styles if tag == "all" or style["tag"] == tag]
    if sort == "name":
        filtered.sort(key=lambda style: style["name"].casefold())
    per_page = max(1, int(number(variables.get("GalleryPerPage"), 25)))
    page_count = max(1, math.ceil(len(filtered) / per_page))
    if page < 1 or page > page_count:
        raise ValueError(f"Gallery page {page} is outside 1..{page_count} for {tag}/{sort}")

    variables.update({
        "NowShowing": "Now showing: (static preview)",
        "GalleryTag": tag,
        "GallerySort": sort,
        "GalleryPage": str(page),
        "GalleryPageCount": str(page_count),
        "GalleryPageLabel": f"PAGE {page} / {page_count}",
        "GalleryResults": (
            f"Showing {(page - 1) * per_page + 1}-{min(len(filtered), page * per_page)} of {len(filtered)} matching styles"
            if filtered else "No styles found. Try a different search or category."
        ),
        "GallerySearchLabel": "Search styles...",
        "GalleryPrevC": ACTIVE if page > 1 else "255,255,255,14",
        "GalleryNextC": ACTIVE if page < page_count else "255,255,255,14",
    })
    for filter_tag, _ in FILTERS:
        variables[f"Filter{filter_tag}C"] = ACTIVE if tag == filter_tag else INACTIVE
    variables["SortRecentC"] = ACTIVE if sort == "recent" else INACTIVE
    variables["SortNameC"] = ACTIVE if sort == "name" else INACTIVE

    for style in all_styles:
        style_id = style["id"]
        variables[f"GH{style_id}"] = "1"
        variables[f"B{style_id}C"] = variables.get(f"B{style_id}O", INACTIVE)

    cols = max(1, int(number(variables.get("GalleryCols"), 5)))
    width = number(variables.get("GalleryButtonWidth"), 128)
    height = number(variables.get("GalleryButtonHeight"), 34)
    gap = number(variables.get("GalleryGap"), 6)
    top = number(variables.get("GalleryTop"), 222)
    start = (page - 1) * per_page
    for slot, style in enumerate(filtered[start:start + per_page]):
        style_id = style["id"]
        row, col = divmod(slot, cols)
        x = 18 + col * (width + gap)
        y = top + row * (height + gap)
        variables[f"GH{style_id}"] = "0"
        variables[f"B{style_id}C"] = variables.get(f"B{style_id}O", INACTIVE)
        sections[f"Btn{style_id}"].update(X=str(x), Y=str(y), W=str(width), H=str(height))
        sections[f"Btn{style_id}T"].update(
            X=str(x + width / 2),
            Y=str(y + height / 2),
            W=str(width - 8),
        )
    return render_skin(sections, variables)


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def main():
    parser = argparse.ArgumentParser(
        description="Render static PNG mockups of every Adaptive Clock settings and gallery page."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output folder (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    output = args.output.resolve()

    settings = parse_ini(SETTINGS_INI)
    gallery = parse_ini(GALLERY_INI)
    clock = parse_ini(CLOCK_INI)
    output.mkdir(parents=True, exist_ok=True)

    settings_dir = output / "settings"
    settings_dir.mkdir(exist_ok=True)
    page_count = int(number(settings.get("Variables", {}).get("PageCount"), 0))
    written = 0
    for page in range(1, page_count + 1):
        name = settings["Variables"].get(f"PageName{page}", f"page-{page}")
        destination = settings_dir / f"{page:02d}-{slug(name)}.png"
        render_settings(settings, clock, page).save(destination)
        written += 1

    styles = gallery_styles(gallery)
    filters_dir = output / "gallery"
    for tag, label in FILTERS:
        for sort, sort_label in SORTS:
            matching = [style for style in styles if tag == "all" or style["tag"] == tag]
            if sort == "name":
                matching.sort(key=lambda style: style["name"].casefold())
            pages = max(1, math.ceil(len(matching) / max(1, int(number(
                gallery.get("Variables", {}).get("GalleryPerPage"), 25
            )))))
            destination_dir = filters_dir / slug(label) / sort_label
            destination_dir.mkdir(parents=True, exist_ok=True)
            for page in range(1, pages + 1):
                image = render_gallery(gallery, styles, tag, sort, page)
                image.save(destination_dir / f"page-{page:02d}.png")
                written += 1

    print(f"Generated {written} PNG mockups in {output}")


if __name__ == "__main__":
    main()
