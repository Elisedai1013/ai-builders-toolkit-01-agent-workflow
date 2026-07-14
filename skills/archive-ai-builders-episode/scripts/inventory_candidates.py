#!/usr/bin/env python3
"""Scan candidate episode assets and write a non-mutating confirmation inventory."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".pptx", ".ppt", ".key", ".pdf", ".md", ".txt", ".docx",
    ".mov", ".mp4", ".m4v", ".png", ".jpg", ".jpeg", ".webp",
}

HARD_EXCLUDE_PARTS = {
    ".git", ".cache", "node_modules", "__pycache__", "archive-ai-builders-episode",
    "【AI Builders解读】项目规范与Skill",
}

NON_ARCHIVAL_PATTERNS = [
    (re.compile(r"(?:^|[_\-. ])(?:draft|temp|tmp)(?:$|[_\-. ])", re.I), "draft/temp"),
    (re.compile(r"草稿|候选|旧版"), "draft/old"),
    (re.compile(r"预览|preview|contact.?sheet|montage", re.I), "preview"),
    (re.compile(r"inspect|layout\.json|qa.report", re.I), "validation output"),
    (re.compile(r"(?:^|[/_\-.])slide-?\d+", re.I), "slide render"),
    (re.compile(r"\([0-9]+\)(?=\.[^.]+$)"), "duplicate copy"),
]

VERSION_PATTERN = re.compile(r"(?:^|[_\-. ])v(\d+)(?:$|[_\-. ])", re.I)


def normalize_token(value: str) -> str:
    value = re.sub(r"\s+", "", value.strip())
    return re.sub(r"[\\/:*?\"<>|]", "", value)


def human_size(size: int) -> str:
    units = ["B", "KiB", "MiB", "GiB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def classify(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()

    if suffix in {".mov", ".mp4", ".m4v"}:
        return "原视频" if "原视频" in name else "解读视频"
    if suffix in {".pptx", ".ppt", ".key"}:
        is_source_deck = bool(
            re.search(r"原(?:文|演讲|分享)?[_ -]*ppt|原始[_ -]*ppt|source[_ -]*deck", name, re.I)
        )
        return "原PPT" if is_source_deck else "解读PPT"
    if suffix == ".pdf" and "ppt" in name:
        return "原PPT候选" if "原" in name else "PPT/PDF候选"
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        if any(token in name for token in ["宣传", "封面", "缩略", "3比4", "4比3"]):
            return "解读视频宣传图"
        return "图片候选"
    if any(token in name for token in ["发布", "标题", "标签", "介绍"]):
        return "解读视频发布信息"
    if any(token in name for token in ["双语", "翻译", "中英"]):
        return "原文内容及中文翻译"
    if any(token in name for token in ["原文", "_en", "english"]):
        return "原文内容"
    if "逐字稿" in name:
        return "解读视频逐字稿"
    return "其他候选"


def status_for(path: Path) -> tuple[str, str]:
    text = str(path)
    flags = [label for pattern, label in NON_ARCHIVAL_PATTERNS if pattern.search(text)]
    version = VERSION_PATTERN.search(path.stem)
    if flags:
        return "默认排除", ", ".join(sorted(set(flags)))
    if version:
        return "需确认", f"version V{version.group(1)}"
    return "需确认", "candidate"


def canonical_name(prefix: str, category: str, path: Path) -> str:
    suffix = path.suffix.lower()
    mapping = {
        "解读视频": f"_解读视频_<清晰度>{suffix}",
        "原视频": f"_原视频{suffix}",
        "解读PPT": "_解读PPT.pptx",
        "原PPT": "_原PPT.pptx",
        "原PPT候选": "_原PPT.pdf",
        "PPT/PDF候选": "_<待确认类型>.pdf",
        "解读视频逐字稿": f"_解读视频逐字稿{suffix}",
        "解读视频发布信息": f"_解读视频发布信息{suffix}",
        "原文内容": f"_原文内容{suffix}",
        "原文内容及中文翻译": f"_原文内容及中文翻译{suffix}",
        "解读视频宣传图": f"_解读视频宣传图_<比例>{suffix}",
    }
    return prefix + mapping.get(category, f"_<待确认类型>{suffix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Root to scan recursively")
    parser.add_argument("--episode", required=True, help="Two-digit episode number")
    parser.add_argument("--date", required=True, help="First publication date, YYYYMMDD")
    parser.add_argument("--speaker", required=True, help="Original speaker")
    parser.add_argument("--topic", required=True, help="Exact original talk title")
    parser.add_argument("--output", type=Path, help="Markdown output; stdout when omitted")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Source directory does not exist: {source}")

    episode = str(args.episode).zfill(2)
    if not re.fullmatch(r"\d{8}", args.date):
        raise SystemExit("--date must use YYYYMMDD")

    prefix = (
        f"【AI Builders解读{episode}】{args.date}_"
        f"{normalize_token(args.speaker)}_{normalize_token(args.topic)}"
    )

    candidates = []
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        if any(part in HARD_EXCLUDE_PARTS for part in path.parts):
            continue
        stat = path.stat()
        category = classify(path)
        status, reason = status_for(path)
        candidates.append({
            "path": path,
            "category": category,
            "status": status,
            "reason": reason,
            "size": stat.st_size,
            "mtime_epoch": stat.st_mtime,
            "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "destination": canonical_name(prefix, category, path),
        })

    candidates.sort(
        key=lambda item: (
            item["category"], item["status"], -item["mtime_epoch"], str(item["path"])
        )
    )

    lines = [
        "# AI Builders 候选归档清单（尚未归档）",
        "",
        f"- 扫描目录：`{source}`",
        f"- 建议文件夹：`{prefix}`",
        f"- 候选数量：{len(candidates)}",
        "- 状态说明：任何 `需确认` 项均不得在用户确认前复制到正式资料夹。",
        "",
        "| ID | 内容类型 | 状态 | 原因 | 大小 | 修改时间 | 来源 | 建议归档名 |",
        "| ---: | --- | --- | --- | ---: | --- | --- | --- |",
    ]

    for index, item in enumerate(candidates, start=1):
        lines.append(
            "| {id} | {category} | {status} | {reason} | {size} | {mtime} | `{path}` | `{destination}` |".format(
                id=index,
                category=item["category"],
                status=item["status"],
                reason=item["reason"],
                size=human_size(item["size"]),
                mtime=item["mtime"],
                path=item["path"],
                destination=item["destination"],
            )
        )

    lines.extend([
        "",
        "## 用户确认",
        "",
        "请逐类确认要保存的候选 ID。没有被确认的文件不会进入正式资料夹。",
        "",
        "| 内容类型 | 推荐候选 ID | 正式归档名 | 保存？ |",
        "| --- | ---: | --- | --- |",
        "| 待填写 | 待填写 | 待填写 | 请确认 |",
        "",
    ])

    output = "\n".join(lines)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output)


if __name__ == "__main__":
    main()
