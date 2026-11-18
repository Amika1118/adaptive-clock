"""Copy clock preview PNGs into folders matching the Gallery categories."""

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LUA_PATH = ROOT / "AdaptiveClock" / "AdaptiveClock.lua"
DEFAULT_SOURCE = ROOT / "docs" / "previews"
DEFAULT_OUTPUT = ROOT / "docs" / "previews-by-category"
CATEGORIES = {
    "code": "coder",
    "easy": "everyday",
    "girl": "bloom",
    "boy": "volt",
    "en": "english",
}


def styles_and_tags():
    lua = LUA_PATH.read_text(encoding="utf-8-sig")
    try:
        names_block = lua.split("local NAMES = {", 1)[1].split("-- Styles that only appear", 1)[0]
    except IndexError as exc:
        raise ValueError(f"Could not find the style names in {LUA_PATH}") from exc
    names = re.findall(r"'([^']+)'", names_block)
    if not names:
        raise ValueError(f"No clock style names found in {LUA_PATH}")

    tags = {}
    for start, end, tag in re.findall(
        r"for i = (\d+), (\d+) do TAGS\[i\] = '(\w+)'", lua
    ):
        for style_id in range(int(start), int(end) + 1):
            tags[style_id] = tag
    for first, second, first_tag, second_tag in re.findall(
        r"TAGS\[(\d+)\], TAGS\[(\d+)\] = '(\w+)', '(\w+)'", lua
    ):
        tags[int(first)] = first_tag
        tags[int(second)] = second_tag
    return names, tags


def main():
    parser = argparse.ArgumentParser(
        description="Copy clock preview PNGs into folders by Gallery category."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"folder containing preview PNGs (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"destination folder (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_dir():
        parser.error(f"Preview folder does not exist: {source}")

    names, tags = styles_and_tags()
    images = {}
    missing = []
    for style_id, name in enumerate(names, start=1):
        matches = sorted(source.glob(f"{style_id:02d}-*.png"))
        if len(matches) != 1:
            missing.append(f"{style_id}: {name} ({len(matches)} matching PNGs)")
        else:
            images[style_id] = matches[0]
    if missing:
        raise SystemExit(
            "Expected exactly one preview PNG for each clock style. "
            "Run tools/preview.py first. Problems:\n  " + "\n  ".join(missing)
        )

    counts = {category: 0 for category in ("all", "classic", *CATEGORIES.values())}
    for style_id, source_image in images.items():
        category_dirs = ["all"]
        tag = tags.get(style_id)
        if tag in CATEGORIES:
            category_dirs.append(CATEGORIES[tag])
        elif tag is None:
            category_dirs.append("classic")
        for category in category_dirs:
            destination_dir = output / category
            destination_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_image, destination_dir / source_image.name)
            counts[category] += 1

    print(f"Copied {sum(counts.values())} PNGs into {output}:")
    for category, count in counts.items():
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
