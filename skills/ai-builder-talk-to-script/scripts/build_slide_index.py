#!/usr/bin/env python3
"""Build a minimal slides.json from a PPTX without inventing topics or timestamps."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


SLIDE_PATTERN = re.compile(r"^ppt/slides/slide(\d+)\.xml$")


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def text_of_first(root: ElementTree.Element, local_name: str) -> str | None:
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == local_name and element.text:
            return element.text.strip()
    return None


def inspect_pptx(path: Path, official: bool | None) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        slide_entries = []
        for name in names:
            match = SLIDE_PATTERN.match(name)
            if match:
                slide_entries.append((int(match.group(1)), name))
        slide_entries.sort()
        if not slide_entries:
            raise ValueError("PPTX contains no slide XML files")

        slide_structure = []
        for number, name in slide_entries:
            root = ElementTree.fromstring(archive.read(name))
            picture_count = 0
            shape_count = 0
            graphic_frame_count = 0
            for element in root.iter():
                local = element.tag.rsplit("}", 1)[-1]
                if local == "pic":
                    picture_count += 1
                elif local == "sp":
                    shape_count += 1
                elif local == "graphicFrame":
                    graphic_frame_count += 1
            slide_structure.append(
                {
                    "slide": number,
                    "picture_count": picture_count,
                    "shape_count": shape_count,
                    "graphic_frame_count": graphic_frame_count,
                }
            )

        creator = None
        if "docProps/core.xml" in names:
            core = ElementTree.fromstring(archive.read("docProps/core.xml"))
            creator = text_of_first(core, "creator")

        flattened = all(
            item["picture_count"] == 1
            and item["shape_count"] == 0
            and item["graphic_frame_count"] == 0
            for item in slide_structure
        )
        notes_files = len(
            [name for name in names if re.match(r"^ppt/notesSlides/notesSlide\d+\.xml$", name)]
        )

    count = len(slide_entries)
    return {
        "kind": "flattened_ppt_index" if flattened else "pptx_slide_index",
        "official_original_deck": official,
        "source": {
            "pptx": str(path),
            "sha256": sha256(path),
        },
        "inspection": {
            "creator": creator,
            "slide_count": count,
            "all_slides_single_picture_no_text_shapes": flattened,
            "notes_slide_file_count": notes_files,
            "limitations": [
                "This index contains file-page numbers only.",
                "No slide topic, video timestamp, or official provenance was inferred.",
            ],
        },
        "extraction": {"final_slide_count": count},
        "slides": [
            {
                "slide": number,
                "topic": None,
                "timestamp": None,
                "filename": None,
            }
            for number, _ in slide_entries
        ],
    }


def parse_official(value: str) -> bool | None:
    return {"true": True, "false": False, "unknown": None}[value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", required=True, type=Path)
    parser.add_argument(
        "--official-original-deck",
        choices=("true", "false", "unknown"),
        default="unknown",
        help="Declare provenance only when it is actually known",
    )
    parser.add_argument("--output", type=Path, help="Write JSON here; omit to print to stdout")
    parser.add_argument("--force", action="store_true", help="Allow replacing an existing output file")
    args = parser.parse_args()

    pptx = args.pptx.expanduser().resolve()
    if not pptx.is_file():
        parser.error(f"PPTX does not exist: {pptx}")
    if not zipfile.is_zipfile(pptx):
        parser.error(f"not a readable PPTX ZIP package: {pptx}")

    try:
        index = inspect_pptx(pptx, parse_official(args.official_original_deck))
    except (ValueError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(index, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        output = args.output.expanduser().resolve()
        if output.exists() and not args.force:
            parser.error(f"output exists; pass --force to replace it: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {len(index['slides'])}-slide index: {output}", file=sys.stderr)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
