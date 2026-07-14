#!/usr/bin/env python3
"""Audit a canonical AI Builders episode folder and its formal delivery bundles."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


FOLDER_PATTERN = re.compile(r"^【AI Builders解读\d{2}】\d{8}_[^_]+_.+$")

FORBIDDEN_NAME_PATTERNS = [
    re.compile(r"(?:^|[_\-. ])v\d+(?:$|[_\-. ])", re.I),
    re.compile(r"draft|草稿|候选|旧版", re.I),
    re.compile(r"最终|最新版|final", re.I),
    re.compile(r"预览|preview|contact.?sheet|montage", re.I),
    re.compile(r"prototype|原型", re.I),
    re.compile(r"inspect|layout\.json|qa[._ -]?report", re.I),
    re.compile(r"(?:^|[_\-. ])(?:tmp|temp|cache)(?:$|[_\-. ])", re.I),
    re.compile(r"\.map$", re.I),
]

ROOT_ONLY_FORBIDDEN_PATTERNS = [
    re.compile(r"(?:^|[_\-.])slide-?\d+", re.I),
]

HIDDEN_ALLOWLIST: set[str] = set()
IGNORED_ROOT_FILES = {"README.md"}
HTML_REFERENCE_PATTERN = re.compile(
    r"(?:src|href)\s*=\s*[\"']([^\"']+)[\"']", re.I
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode-dir", required=True, type=Path)
    return parser.parse_args()


def forbidden_marker(name: str, *, root: bool = False) -> bool:
    patterns = FORBIDDEN_NAME_PATTERNS + (ROOT_ONLY_FORBIDDEN_PATTERNS if root else [])
    return any(pattern.search(name) for pattern in patterns)


def is_formal_bundle(path: Path, prefix: str) -> bool:
    return path.is_dir() and path.name.startswith(prefix + "_解读HTML_")


def check_local_html_references(html_path: Path, bundle: Path, errors: list[str]) -> None:
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"HTML is not UTF-8: {html_path.relative_to(bundle)}")
        return

    for raw_reference in HTML_REFERENCE_PATTERN.findall(text):
        reference = raw_reference.strip()
        if (
            not reference
            or "${" in reference
            or "{{" in reference
            or reference.startswith(("#", "/", "//"))
            or re.match(r"^[a-z][a-z0-9+.-]*:", reference, re.I)
        ):
            continue

        clean_reference = unquote(reference.split("#", 1)[0].split("?", 1)[0])
        if not clean_reference:
            continue

        target = (html_path.parent / clean_reference).resolve()
        try:
            target.relative_to(bundle.resolve())
        except ValueError:
            errors.append(
                f"bundle reference escapes package: {html_path.relative_to(bundle)} -> {reference}"
            )
            continue
        if not target.exists():
            errors.append(
                f"broken bundle reference: {html_path.relative_to(bundle)} -> {reference}"
            )


def audit_bundle(bundle: Path, prefix: str, errors: list[str]) -> None:
    if not is_formal_bundle(bundle, prefix):
        errors.append(f"unexpected nested directory: {bundle.name}")
        return

    if forbidden_marker(bundle.name):
        errors.append(f"non-archival bundle name: {bundle.name}")

    for required in ("index.html", "README.md"):
        if not (bundle / required).is_file():
            errors.append(f"formal bundle missing {required}: {bundle.name}")

    for path in sorted(bundle.rglob("*"), key=lambda item: str(item)):
        relative = path.relative_to(bundle)
        if path.is_symlink():
            errors.append(f"symlink is not allowed in formal bundle: {bundle.name}/{relative}")
            continue
        if any(part.startswith(".") and part not in HIDDEN_ALLOWLIST for part in relative.parts):
            errors.append(f"hidden file or directory in formal bundle: {bundle.name}/{relative}")
        if any(forbidden_marker(part) for part in relative.parts):
            errors.append(f"non-archival item in formal bundle: {bundle.name}/{relative}")
        if path.is_file() and path.suffix.lower() == ".html":
            check_local_html_references(path, bundle, errors)


def main() -> None:
    args = parse_args()
    episode_dir = args.episode_dir.expanduser().resolve()
    errors: list[str] = []

    if not episode_dir.is_dir():
        raise SystemExit(f"Episode directory does not exist: {episode_dir}")

    prefix = episode_dir.name
    if not FOLDER_PATTERN.fullmatch(prefix):
        errors.append(f"folder name does not match canonical schema: {prefix}")

    readme_path = episode_dir / "README.md"
    if not readme_path.is_file():
        errors.append("README.md is missing")
        readme = ""
    else:
        readme = readme_path.read_text(encoding="utf-8")

    artifact_count = 0
    for child in sorted(episode_dir.iterdir(), key=lambda path: path.name):
        if child.name.startswith("."):
            errors.append(f"hidden file or directory in archive root: {child.name}")
            continue

        if child.is_dir():
            audit_bundle(child, prefix, errors)
            if is_formal_bundle(child, prefix):
                artifact_count += 1
                if child.name not in readme:
                    errors.append(f"formal bundle is not listed in README.md: {child.name}")
            continue

        if child.name in IGNORED_ROOT_FILES:
            continue

        artifact_count += 1
        if not child.name.startswith(prefix + "_"):
            errors.append(f"file does not share canonical prefix: {child.name}")
        if forbidden_marker(child.name, root=True):
            errors.append(f"non-archival filename marker in: {child.name}")
        if child.name not in readme:
            errors.append(f"file is not listed in README.md: {child.name}")

    required_readme_terms = [
        "项目概览", "原始分享来源", "内容结构", "文件结构", "渠道发布记录", "命名规范"
    ]
    for term in required_readme_terms:
        if term not in readme:
            errors.append(f"README.md missing required section: {term}")

    if errors:
        print("Archive audit failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Archive audit passed: {artifact_count} canonical artifacts or bundles, "
        "README coverage and bundle dependencies complete."
    )


if __name__ == "__main__":
    main()
