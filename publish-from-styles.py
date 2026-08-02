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
 * Charcoal UI + rose-ember accents.
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
    "phoenix-synth.css": {
        "header": """/*
 * Phoenix Project — Synth
 * 80s synthwave (magenta / violet / cyan neon).
 * External stylesheet URL (ApolloStage base recommended).
 * Pure CSS — no userscript required. Self-contained layout + theme.
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-synth.css
 */
""",
    },
    "phoenix-maclite.css": {
        "header": """/*
 * Phoenix Project — MacLite
 * Apple-inspired light UI (SF blue accents, soft grey chrome).
 * Self-contained standalone CSS (structure + theme). Pure CSS — no userscript required.
 * Use as an external stylesheet URL on phoenixproject.app (or paste where custom CSS is allowed).
 *
 * IMPORTANT: Prefer jsDelivr (Content-Type: text/css). raw.githubusercontent.com is text/plain.
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-maclite.css
 */
""",
    },
    "orpheus-matrix.css": {
        "header": """/*
 * Orpheus Network — Matrix
 * Green-on-black terminal palette (OPS / orpheus.network).
 * Self-contained standalone CSS (structure + theme). Pure CSS — no userscript required.
 * Use as an external stylesheet URL on Orpheus (or paste where custom CSS is allowed).
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/orpheus-matrix.css
 */
""",
    },
    "redacted-synth.css": {
        "header": """/*
 * Redacted — Synth
 * 80s synthwave (magenta / violet / cyan neon) for redacted.sh.
 * Self-contained standalone CSS (structure + theme). Pure CSS — no userscript required.
 * Use as an external stylesheet URL on Redacted (or paste where custom CSS is allowed).
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/redacted-synth.css
 */
""",
        # Monkie gates polish on html[data-monkies-redacted-skin="synth"]; drop for public.
        "rewrite_skin_attr": "synth",
    },
    "broadcasthe-dark.css": {
        "header": """/*
 * BroadcasTheNet — Dark Ambient
 * Deep void + indigo/teal aurora for broadcasthe.net (BTN).
 * STANDALONE skin with Imagine-generated ambient logo banner.
 * Pure CSS — no userscript required.
 *
 * IMPORTANT: Do NOT use raw.githubusercontent.com (serves text/plain; page goes blank).
 * Use jsDelivr (Content-Type: text/css):
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/broadcasthe-dark.css
 */
""",
    },
    "ptp-dark.css": {
        "header": """/*
 * PassThePopcorn — Cinema Noir
 * Pure greys + black. RECOMMENDED: Official stylesheet = Dark (Default), then
 * Append this URL (or use monkie Noir). Pure CSS — no userscript required.
 *
 * This public build includes a layout fallback so Replace mode still works.
 * Best results: keep Dark (Default) as the official site stylesheet.
 *
 * Logo: skins/assets/ptp-logo-noir-header.png (jsDelivr)
 *
 * IMPORTANT: Prefer jsDelivr (Content-Type: text/css). Never use github.com/…/blob/…
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/ptp-dark.css
 */
""",
        "rewrite_skin_attr": "dark",
        "logo_cdn": (
            "https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main"
            "/skins/assets/ptp-logo-noir-header.png"
        ),
        "append_layout": "ptp-dark-layout.css",
    },
    "ptp-runner.css": {
        "header": """/*
 * PassThePopcorn — Blade Runner
 * Wet neon noir: void black, cyan, magenta, amber (2049-inspired).
 * RECOMMENDED: Official stylesheet = Dark (Default), then Append this URL
 * (or monkie pill → Runner). Pure CSS — no userscript required.
 *
 * Logo: skins/assets/ptp-logo-runner-header.jpg (jsDelivr)
 *
 * IMPORTANT: Prefer jsDelivr. Never use github.com/…/blob/… as official CSS.
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/ptp-runner.css
 */
""",
        "rewrite_skin_attr": "runner",
        "logo_cdn": (
            "https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main"
            "/skins/assets/ptp-logo-runner-header.jpg"
        ),
        "append_layout": "ptp-dark-layout.css",
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


def rewrite_monkies_skin_attr(css: str, skin: str) -> str:
    """Public external CSS has no monkie userscript — ungate html[data-*-skin="…"] rules."""
    if not skin:
        return css
    # html[data-monkies-redacted-skin="synth"] → html
    # html[data-monkies-orpheus-skin="matrix"] → html  (if ever needed)
    pat = re.compile(
        r'html\[data-monkies-[a-z0-9-]*skin\s*=\s*["\']' + re.escape(skin) + r'["\']\]',
        re.I,
    )
    return pat.sub("html", css)


def rewrite_logo_cdn(css: str, logo_cdn: str | None) -> str:
    """Replace monkie-dev :8000 / relative asset logo urls with public CDN."""
    if not logo_cdn:
        return css
    css = re.sub(
        r'url\(\s*["\']?https?://127\.0\.0\.1:8000/styles/assets/ptp-logo-(?:noir|runner)-header\.(?:png|jpg)(?:\?[^"\')\s]*)?["\']?\s*\)',
        f'url("{logo_cdn}")',
        css,
        flags=re.I,
    )
    css = re.sub(
        r'url\(\s*["\']?(?:\.\./)*styles/assets/ptp-logo-(?:noir|runner)-header\.(?:png|jpg)(?:\?[^"\')\s]*)?["\']?\s*\)',
        f'url("{logo_cdn}")',
        css,
        flags=re.I,
    )
    return css


def build_one(
    src: Path,
    dest: Path,
    header: str,
    rewrite_skin_attr: str | None = None,
    logo_cdn: str | None = None,
    append_src: Path | None = None,
) -> None:
    css = src.read_text(encoding="utf-8")
    css = rewrite_header(css, header)
    css = soft_clean(css)
    css = strip_internal_dnu_attr_rules(css)
    if rewrite_skin_attr:
        css = rewrite_monkies_skin_attr(css, rewrite_skin_attr)
    css = rewrite_logo_cdn(css, logo_cdn)
    if append_src and append_src.is_file():
        extra = append_src.read_text(encoding="utf-8")
        # Drop nested file header; keep body
        extra = re.sub(r"^/\*.*?\*/\s*", "", extra, count=1, flags=re.S)
        # Ungate all monkie skin attrs for public layout fallback
        extra = re.sub(
            r'html\[data-monkies-ptp-skin\s*=\s*["\'](?:dark|runner)["\']\]',
            "html",
            extra,
            flags=re.I,
        )
        extra = re.sub(r"html\s*,\s*html", "html", extra)
        extra = rewrite_logo_cdn(extra, logo_cdn)
        css = css.rstrip() + "\n\n/* ── layout fallback (no Dark base) ── */\n" + extra
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

    print(f"Publishing skins from {styles}")
    for name, meta in SKINS.items():
        src = styles / name
        if not src.is_file():
            print(f"  skip missing {src}")
            continue
        append_name = meta.get("append_layout")
        append_src = (styles / append_name) if append_name else None
        build_one(
            src,
            HERE / "skins" / name,
            meta["header"],
            rewrite_skin_attr=meta.get("rewrite_skin_attr"),
            logo_cdn=meta.get("logo_cdn"),
            append_src=append_src,
        )

    print("Done. Commit, tag, push — see README.md for jsDelivr URLs.")


if __name__ == "__main__":
    main()
