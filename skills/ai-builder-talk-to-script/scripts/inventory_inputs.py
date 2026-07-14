#!/usr/bin/env python3
"""Inventory likely source and draft artifacts for an AI Builders oral script."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path


SKIP_PARTS = {
    ".git",
    ".cache",
    "__pycache__",
    "node_modules",
    "tmp",
    "temp",
    "output",
    "outputs",
    "calibration",
    "calibration-full",
    "sampled-frames",
    "contact-sheets",
    "late-contact-sheets",
    "candidates-stage",
    "seek-test",
    "renders",
    "rendered",
    "previews",
}
SKIP_NAMES = {".DS_Store"}
HASH_LIMIT = 128 * 1024 * 1024
MARKDOWN_DUPLICATE_LIMIT = 10


def classify(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()

    if "解读视频逐字稿" in path.name:
        return "oral-script-draft" if "草稿" in path.name else "oral-script"
    if "解读配套工具箱" in path.name:
        return "companion-toolkit"
    if "证据" in path.name and "映射" in path.name:
        return "evidence-map"
    if name == "slides.json":
        return "slide-index"
    if name == "metadata.json":
        return "video-metadata"
    if name in {"source.md", "readme.md"}:
        return "source-note"
    if "raw" in name and suffix in {".txt", ".md", ".vtt", ".srt"}:
        return "raw-transcript"
    if any(token in path.name for token in ("双语", "中英", "翻译")) and suffix in {
        ".txt",
        ".md",
        ".docx",
    }:
        return "bilingual-transcript"
    if ("_en" in name or "英文" in path.name or "原文内容" in path.name) and suffix in {
        ".txt",
        ".md",
        ".docx",
    }:
        return "english-transcript"
    if suffix in {".vtt", ".srt"}:
        return "subtitle"
    if suffix in {".pptx", ".pdf", ".key"}:
        return "slide-deck"
    if name.startswith("slide-") and suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "slide-image"
    if suffix in {".mp4", ".mov", ".mkv", ".webm"}:
        return "source-video"
    if suffix in {".txt", ".md", ".docx"}:
        return "other-text"
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "other-image"
    if suffix == ".zip":
        return "delivery-package"
    return "other"


def digest(path: Path, size: int) -> str:
    if size > HASH_LIMIT:
        return "skipped-large"
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.name in SKIP_NAMES or any(part in SKIP_PARTS for part in relative.parts):
            continue
        if path.name.startswith("~$"):
            continue
        yield path


def build_inventory(root: Path) -> dict:
    items = []
    hashes: dict[str, list[str]] = defaultdict(list)
    for path in iter_files(root):
        stat = path.stat()
        sha256 = digest(path, stat.st_size)
        relative = str(path.relative_to(root))
        item = {
            "role": classify(path),
            "path": relative,
            "size_bytes": stat.st_size,
            "sha256": sha256,
        }
        items.append(item)
        if len(sha256) == 64:
            hashes[sha256].append(relative)

    duplicates = [
        {"sha256": value, "paths": paths}
        for value, paths in sorted(hashes.items())
        if len(paths) > 1
    ]
    return {"source": str(root), "files": items, "duplicate_groups": duplicates}


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def render_markdown(inventory: dict) -> str:
    rows = [
        "# AI Builders input inventory",
        "",
        f"Source: `{inventory['source']}`",
        "",
        "| Role | Size | SHA-256 | Relative path |",
        "| --- | ---: | --- | --- |",
    ]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in inventory["files"]:
        grouped[item["role"]].append(item)

    for role in sorted(grouped):
        items = grouped[role]
        if len(items) > 12 and role in {"slide-image", "other-image", "other"}:
            common = os.path.commonpath([item["path"] for item in items])
            size = sum(item["size_bytes"] for item in items)
            rows.append(
                f"| {role} ({len(items)} files) | {human_size(size)} | `grouped` | `{common}` |"
            )
            continue
        for item in items:
            sha = item["sha256"][:12] if len(item["sha256"]) == 64 else item["sha256"]
            path = item["path"].replace("|", "\\|")
            rows.append(f"| {item['role']} | {human_size(item['size_bytes'])} | `{sha}` | `{path}` |")

    rows.extend(["", "## Duplicate groups", ""])
    if not inventory["duplicate_groups"]:
        rows.append("No byte-identical duplicates found among hashed files.")
    else:
        visible_groups = inventory["duplicate_groups"][:MARKDOWN_DUPLICATE_LIMIT]
        for group in visible_groups:
            rows.append(f"- `{group['sha256'][:12]}`")
            for path in group["paths"]:
                rows.append(f"  - `{path}`")
        omitted = len(inventory["duplicate_groups"]) - len(visible_groups)
        if omitted:
            rows.append(
                f"- … {omitted} additional duplicate groups omitted; use `--format json` for the full inventory."
            )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Source-material folder to scan")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    root = args.source.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"source is not a directory: {root}")

    inventory = build_inventory(root)
    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
