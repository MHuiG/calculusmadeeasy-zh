#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original"
ZH = ROOT / "zh"

ATTR_RE = re.compile(r"""\b(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
MATH_RE = re.compile(
    r"""
    \\begin\{(align\*?|alignat\*?|gather\*?|aligned|equation\*?)\}(?:\{[^}]*\})?.*?\\end\{\1\}
    |(?<!\\)\\\[.*?(?<!\\)\\\]
    |(?<!\\)\\\(.*?(?<!\\)\\\)
    |\$(?:\\.|[^$<])+\$
    """,
    re.DOTALL | re.VERBOSE,
)
TEXT_COMMAND_RE = re.compile(r"\\(?:text|mbox)\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", re.DOTALL)
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z]{2,}\b")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

ALLOW_LATIN = {
    "MathJax",
    "Google",
    "Payhip",
    "Amazon",
    "Wikipedia",
    "Zed",
    "Shaw",
    "John",
    "Baez",
    "Gilbert",
    "Strang",
    "Needham",
    "Strogatz",
    "Silvanus",
    "Thompson",
    "CalculusMadeEasy",
    "HTML",
    "URL",
}


def html_files(base: Path) -> list[Path]:
    return sorted(path.relative_to(base) for path in base.rglob("*.html"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def attrs(html: str) -> list[str]:
    return ATTR_RE.findall(html)


def math_segments(html: str) -> list[str]:
    return [match.group(0) for match in MATH_RE.finditer(html)]


def math_key(segment: str) -> str:
    segment = TEXT_COMMAND_RE.sub(r"\\text{}", segment)
    return re.sub(r"\s+", "", segment)


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def has_cjk_in_math_symbols(segment: str) -> bool:
    return has_cjk(TEXT_COMMAND_RE.sub(" ", segment))


def visible_text(html: str) -> str:
    html = SCRIPT_STYLE_RE.sub(" ", html)
    html = MATH_RE.sub(" ", html)
    html = TAG_RE.sub(" ", html)
    return re.sub(r"\s+", " ", html)


def latin_residue(text: str) -> list[str]:
    words = LATIN_WORD_RE.findall(text)
    return sorted({word for word in words if word not in ALLOW_LATIN})


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []

    original_files = html_files(ORIGINAL)
    zh_files = html_files(ZH)
    if original_files != zh_files:
        problems.append("HTML file lists differ between original/ and zh/.")
        missing = sorted(set(original_files) - set(zh_files))
        extra = sorted(set(zh_files) - set(original_files))
        if missing:
            problems.append(f"Missing zh files: {', '.join(map(str, missing))}")
        if extra:
            problems.append(f"Extra zh files: {', '.join(map(str, extra))}")

    for rel in original_files:
        original_html = read(ORIGINAL / rel)
        zh_html = read(ZH / rel)

        original_attrs = attrs(original_html)
        zh_attrs = attrs(zh_html)
        if original_attrs != zh_attrs:
            problems.append(f"{rel}: href/src attributes changed.")

        zh_math_segments = math_segments(zh_html)
        cjk_math = [segment for segment in zh_math_segments if has_cjk_in_math_symbols(segment)]
        if cjk_math:
            problems.append(f"{rel}: Chinese text appears inside MathJax/math segments.")

        original_math = Counter(math_key(segment) for segment in math_segments(original_html))
        zh_math = Counter(math_key(segment) for segment in zh_math_segments)
        if original_math != zh_math:
            warnings.append(f"{rel}: math segment multiset differs; likely prose reordering or added inline symbols.")

        text = visible_text(zh_html)
        cjk_count = len(CJK_RE.findall(text))
        residue = latin_residue(text)
        if cjk_count == 0:
            warnings.append(f"{rel}: no Chinese visible text detected.")
        elif len(residue) > 40:
            preview = ", ".join(residue[:30])
            warnings.append(f"{rel}: many Latin words remain ({len(residue)}): {preview}")

    print(f"HTML files: original={len(original_files)} zh={len(zh_files)}")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if problems:
        print("\nProblems:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("\nStructural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
