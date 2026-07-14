#!/usr/bin/env python3
"""Run deterministic structural checks on an AI Builders oral-script draft."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote


FIXED_LINES = (
    "这个系列，我们少听一点二手观点，直接听全球一线 AI Builders 亲口讲，他们是怎么想、怎么做的。再从里面找出，我们今天就能用的方法。",
)

FORBIDDEN_PHRASES = (
    "这场演讲里，没有你",
    "这里面没有你",
    "她的演讲里，为什么没有她自己",
)

METHOD_TERMS = (
    "提示词",
    "模板",
    "测试",
    "清单",
    "观察表",
    "评分表",
    "决策规则",
    "框架",
    "工具卡",
)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, object] = field(default_factory=dict)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path, report: Report, label: str) -> str:
    if not path.is_file():
        report.error(f"{label} does not exist: {path}")
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report.error(f"{label} is not valid UTF-8: {path}")
        return ""
    if not text.strip():
        report.error(f"{label} is empty: {path}")
    return text


def spoken_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    in_fence = False
    for raw in markdown.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith(("#", ">", "|", "- [", "* [")):
            continue
        cleaned = re.sub(r"!?(\[[^\]]*\])\([^)]*\)", r"\1", stripped)
        cleaned = re.sub(r"[`*_~]", "", cleaned)
        lines.append(cleaned)
    return lines


def parse_declared_minutes(text: str) -> tuple[float, float] | None:
    match = re.search(r"预计口播时长[^\d]*(\d+(?:\.\d+)?)\s*[—–\-至~]\s*(\d+(?:\.\d+)?)\s*分钟", text)
    if match:
        return float(match.group(1)), float(match.group(2))
    match = re.search(r"预计口播时长[^\d]*(\d+(?:\.\d+)?)\s*分钟", text)
    if match:
        value = float(match.group(1))
        return value, value
    return None


def load_slide_count(path: Path | None, report: Report) -> tuple[int | None, bool | None]:
    if path is None:
        return None, None
    if not path.is_file():
        report.error(f"slides.json does not exist: {path}")
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        report.error(f"cannot parse slides.json: {exc}")
        return None, None

    count = data.get("extraction", {}).get("final_slide_count")
    if not isinstance(count, int):
        slides = data.get("slides")
        count = len(slides) if isinstance(slides, list) else None
    official = data.get("official_original_deck")
    return count, official if isinstance(official, bool) else None


def parse_page_numbers(text: str) -> list[int]:
    numbers: list[int] = []
    for match in re.finditer(r"第\s*([0-9\s、,，—–\-至]+?)\s*页", text):
        expression = re.sub(r"\s+", "", match.group(1))
        for part in re.split(r"[、,，]", expression):
            if not part:
                continue
            range_match = re.fullmatch(r"(\d+)[—–\-至](\d+)", part)
            if range_match:
                start, end = map(int, range_match.groups())
                if start <= end:
                    numbers.extend(range(start, end + 1))
                else:
                    numbers.extend((start, end))
            elif part.isdigit():
                numbers.append(int(part))
    return numbers


def check_relative_links(path: Path, text: str, report: Report) -> None:
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split("#", 1)[0]
        if not target.startswith("./"):
            continue
        decoded_target = unquote(target)
        resolved = (path.parent / decoded_target).resolve()
        if not resolved.exists():
            report.error(f"broken relative link: {target}")


def check_toolkit(path: Path, text: str, script_text: str, report: Report) -> None:
    if "不是" not in text or "正式名称" not in text or not any(word in text for word in ("提炼", "整理")):
        report.error("toolkit must state that derived tool names are not the speaker's formal names")

    tool_matches = list(re.finditer(r"^##\s+工具[^\n]*", text, re.MULTILINE))
    if not tool_matches:
        report.error("toolkit has no '## 工具…' sections")
        return

    required = {
        "source relationship": r"^###\s+(来源关系|来源)",
        "use case": r"^###\s+(什么时候使用|适用场景)",
        "input": r"^###\s+输入",
        "steps": r"^###\s+(使用步骤|使用方法|测试方法|可复制提示词|步骤)",
        "output": r"^###\s+(输出|最终输出格式)",
        "boundary": r"^###\s+(使用边界|边界)",
    }
    for index, match in enumerate(tool_matches):
        end = tool_matches[index + 1].start() if index + 1 < len(tool_matches) else len(text)
        section = text[match.start() : end]
        title = match.group(0).strip()
        for label, pattern in required.items():
            if not re.search(pattern, section, re.MULTILINE):
                report.error(f"{title} is missing {label}")

        name = re.sub(r"^##\s+工具[^｜|]*[｜|]", "", title).strip()
        if name and name not in script_text:
            report.warn(f"toolkit tool name does not appear verbatim in script: {name}")

    check_relative_links(path, text, report)


def audit(args: argparse.Namespace) -> Report:
    report = Report()
    script_path = args.script.expanduser().resolve()
    text = read_text(script_path, report, "script")
    if not text:
        return report

    if "草稿" not in script_path.name:
        report.warn("working script filename does not contain '_草稿'")
    if re.search(r"【AI Builders解读\d{2}】", str(script_path.parent)):
        if "草稿" in script_path.name:
            report.error("draft appears to be inside a formal episode archive")
        else:
            report.warn("auditing a file in the formal archive; do not modify it without confirmation")

    headings = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)
    if not any(heading.startswith("开场") for heading in headings):
        report.error("missing an opening section headed '## 开场…'")
    if not any(heading.startswith("收尾") for heading in headings):
        report.error("missing an ending section headed '## 收尾…'")
    if len(headings) < 3:
        report.error("script needs at least an opening, one body section, and an ending")

    visual_cues = len(re.findall(r"^>\s*画面[：:]", text, re.MULTILINE))
    if visual_cues < max(2, len(headings) - 1):
        report.warn(f"only {visual_cues} visual cues for {len(headings)} major sections")

    for line in FIXED_LINES:
        count = text.count(line)
        if count != 1:
            report.error(f"fixed series line must appear exactly once (found {count}): {line}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in text:
            report.error(f"rejected ambiguous wording remains: {phrase}")

    for pattern in (r"\bTODO\b", r"待补", r"待核验", r"待确认"):
        if re.search(pattern, text, re.IGNORECASE):
            report.warn(f"unresolved marker found: {pattern}")

    if not any(term in text for term in METHOD_TERMS):
        report.error("no reusable prompt, template, test, checklist, form, rule, or framework is delivered")
    if any(term in text for term in METHOD_TERMS) and not re.search(r"我把.{0,30}(整理|提炼)成", text):
        report.warn("derived methodology lacks a clear '我把它整理/提炼成…' attribution")
    if "三件事" in text or "三件小事" in text:
        report.warn("opening or ending may frame the payoff as an action list instead of reusable methodology")

    method_names = re.findall(r"[“\"]([^”\"\n]{2,36}(?:提示词|模板|测试|清单|观察表|评分表|框架|工具卡))[”\"]", text)
    for name in sorted(set(method_names)):
        if text.count(name) < 2:
            report.warn(f"promised method name appears only once: {name}")

    spoken = spoken_lines(text)
    spoken_text = "".join(spoken)
    spoken_chars = len(re.sub(r"\s+", "", spoken_text))
    estimated_minutes = spoken_chars / args.chars_per_minute if args.chars_per_minute else 0
    report.metrics.update(
        {
            "spoken_chars": spoken_chars,
            "estimated_minutes": round(estimated_minutes, 2),
            "chars_per_minute": args.chars_per_minute,
            "major_sections": len(headings),
            "visual_cues": visual_cues,
        }
    )

    declared = parse_declared_minutes(text)
    if declared:
        low, high = declared
        tolerance = 0.15
        if estimated_minutes < low * (1 - tolerance) or estimated_minutes > high * (1 + tolerance):
            report.warn(
                f"estimated {estimated_minutes:.1f} minutes differs from declared {low:g}–{high:g} minutes by more than 15%"
            )
    else:
        report.warn("script header does not declare an estimated speaking duration")

    for number, paragraph in enumerate(spoken, start=1):
        length = len(re.sub(r"\s+", "", paragraph))
        if length > args.long_paragraph_chars:
            report.warn(f"spoken paragraph {number} is long ({length} chars); consider splitting it")

    slide_count, official = load_slide_count(args.slides_json, report)
    if slide_count is not None:
        bad_pages = sorted({page for page in parse_page_numbers(text) if page < 1 or page > slide_count})
        if bad_pages:
            report.error(f"PPT page references exceed 1–{slide_count}: {bad_pages}")
        report.metrics["slide_count"] = slide_count
    reconstruction_disclosed = re.search(
        r"投屏.{0,12}复原版.{0,18}不是.{0,12}官方.{0,8}PPT",
        text,
        re.DOTALL,
    )
    if official is False and not reconstruction_disclosed:
        report.error("reconstructed deck is not clearly identified as non-official in the script header")

    check_relative_links(script_path, text, report)

    if args.toolkit:
        toolkit_path = args.toolkit.expanduser().resolve()
        toolkit_text = read_text(toolkit_path, report, "toolkit")
        if toolkit_text:
            check_toolkit(toolkit_path, toolkit_text, text, report)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--toolkit", type=Path)
    parser.add_argument("--slides-json", type=Path)
    parser.add_argument("--chars-per-minute", type=float, default=335.0)
    parser.add_argument("--long-paragraph-chars", type=int, default=160)
    args = parser.parse_args()

    report = audit(args)
    print("AI Builders oral-script audit")
    for key, value in report.metrics.items():
        print(f"METRIC {key}: {value}")
    for message in report.errors:
        print(f"ERROR: {message}")
    for message in report.warnings:
        print(f"WARNING: {message}")
    if not report.errors and not report.warnings:
        print("PASS: no structural issues found")
    elif not report.errors:
        print(f"PASS WITH WARNINGS: {len(report.warnings)}")
    else:
        print(f"FAIL: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
