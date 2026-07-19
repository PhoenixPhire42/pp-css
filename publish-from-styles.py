#!/usr/bin/env python3
"""
Build public PP skins from a local styles directory for CDN sharing.

  python3 publish-from-styles.py
  python3 publish-from-styles.py --styles /path/to/styles

Pure CSS only. No theme switcher UI.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKINS = {
    "phoenix-dark.css": {
        "header": """/*
 * Phoenix Project — Dark
 * Charcoal UI + soft orange accents.
 * External stylesheet URL (ApolloStage base recommended).
 * Pure CSS — no userscript required.
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-dark.css
 */
""",
    },
    "phoenix-flame.css": {
        "header": """/*
 * Phoenix Project — Flame
 * Ember black + phoenix fire accents.
 * External stylesheet URL (ApolloStage base recommended).
 * Pure CSS — no userscript required.
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-flame.css
 */
""",
    },
    "phoenix-neo.css": {
        "header": """/*
 * Phoenix Project — Neo Phoenix (Matrix)
 * Green-on-black terminal palette.
 * External stylesheet URL (ApolloStage base recommended).
 * Pure CSS — no userscript required. Logos embedded as data URIs.
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-neo.css
 */
""",
    },
}


def strip_internal_dnu_attr_rules(css: str) -> str:
    """Drop rules that depend on html[data-*-dnu=…] (private tooling attrs)."""
    lines = css.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r"data-[a-z0-9-]*dnu", line, re.I):
            buf = line
            depth = line.count("{") - line.count("}")
            i += 1
            while i < len(lines) and depth == 0 and "{" not in buf:
                buf += lines[i]
                depth = buf.count("{") - buf.count("}")
                i += 1
            while i < len(lines) and depth > 0:
                buf += lines[i]
                depth = buf.count("{") - buf.count("}")
                i += 1
            continue
        out.append(line)
        i += 1
    return "".join(out)


def rewrite_header(css: str, header: str) -> str:
    return re.sub(r"^/\*.*?\*/\s*", header, css, count=1, flags=re.S)


def soft_clean(css: str) -> str:
    # Neutralize private class prefixes if present in source (generic rename)
    css = re.sub(r"\b[a-z]+-tag-chip\b", "pp-tag-chip", css)
    css = re.sub(r"\b[a-z]+-tags-chipped\b", "pp-tags-chipped", css)
    # Drop lines that document private loaders/pills (comment-only)
    cleaned: list[str] = []
    for line in css.splitlines(keepends=True):
        low = line.lower()
        if "injected by" in low and "loader" in low:
            continue
        if "on-page pill" in low or "tm/vm menu" in low:
            continue
        if "toggle matrix dark theme" in low:
            continue
        cleaned.append(line)
    return "".join(cleaned)


def build_one(src: Path, dest: Path, header: str) -> None:
    css = src.read_text(encoding="utf-8")
    css = rewrite_header(css, header)
    css = soft_clean(css)
    css = strip_internal_dnu_attr_rules(css)
    open_b, close_b = css.count("{"), css.count("}")
    if open_b != close_b:
        raise SystemExit(f"brace mismatch in {src.name}: {{ {open_b} }} {close_b}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(css, encoding="utf-8")
    print(f"  {dest.relative_to(HERE)}  ({dest.stat().st_size} bytes)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--styles",
        type=Path,
        default=HERE.parent / "styles",
        help="Path to source styles directory",
    )
    args = ap.parse_args()
    styles: Path = args.styles
    if not styles.is_dir():
        print(f"styles dir not found: {styles}", file=sys.stderr)
        sys.exit(1)

    print(f"Publishing PP skins from {styles}")
    for name, meta in SKINS.items():
        src = styles / name
        if not src.is_file():
            print(f"  skip missing {src}")
            continue
        build_one(src, HERE / "skins" / name, meta["header"])

    print("Done. Commit, tag, push — see README.md for jsDelivr URLs.")


if __name__ == "__main__":
    main()
