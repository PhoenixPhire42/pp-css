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
import shutil
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
 * STANDALONE pure CSS — do NOT also load ApolloStage (double layout).
 * Site Appearance: leave main Stylesheet minimal/empty if possible; set ONLY
 * External stylesheet URL to this file (jsDelivr). Prefer a version pin.
 *
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.2.1-flame/skins/phoenix-flame.css
 * https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-flame.css
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
    "phoenix-reborn.css": {
        "header": """/*
 * Phoenix Project — Reborn
 * Warm dark rose/gold chrome (Apollostage-based).
 * External stylesheet URL. Pure CSS — no userscript required.
 * Built from monkie styles/phoenix-reborn.css (same SoT as monkie).
 *
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-reborn.css
 */
""",
        # Monkie gates polish on html[data-monkies-phoenix-skin="reborn"]; drop for public.
        "rewrite_skin_attr": "reborn",
    },
    "phoenix-light.css": {
        "header": """/*
 * Phoenix Project — Light (legacy MacLite sibling)
 * Light UI chrome. Prefer phoenix-maclite.css for new installs.
 * Pure CSS — no userscript required. Built from monkie styles/phoenix-light.css.
 *
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-light.css
 */
""",
    },
    "orpheus-matrix.css": {
        "header": """/*
 * Orpheus Network — Matrix (neo)
 * ops-skin: matrix · ops_matrix_cache · OPS_MATRIX_CACHE_V75
 * Green-on-black terminal palette (OPS / orpheus.network).
 * Public mirage/login uses embedded neo logo (orpheus-logo-neo-public-trans).
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
 * Overlay on official darknround (layout geometry from stock).
 * Deep void + indigo/teal aurora + Imagine logo banner.
 * Pure CSS — no userscript required.
 *
 * Best: Stylesheet = darknround, then External Append this URL.
 * If External replaces maincss, geometry is re-asserted so layout still holds.
 *
 * IMPORTANT: Do NOT use raw.githubusercontent.com (serves text/plain; page goes blank).
 * Use jsDelivr (Content-Type: text/css):
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/broadcasthe-dark.css
 */
""",
        "logo_cdn": (
            "https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main"
            "/skins/assets/btn-logo-ambient-header.jpg"
        ),
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
    "thelounge-matrix.css": {
        "header": """/*
 * The Lounge — Matrix Theme
 * Green-on-black terminal palette for The Lounge IRC client.
 *
 * Install: Settings → Advanced → Custom Stylesheet (paste contents),
 * or load via URL if your Lounge host supports external theme CSS.
 *
 * CDN:
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/thelounge-matrix.css
 *   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/thelounge-matrix.css
 *
 * Failsafe: add ?nocss to the Lounge URL if something breaks.
 * Source: monkie styles/thelounge-matrix.css → PhoenixPhire42/pp-css
 */
""",
    },
}


def public_source_names() -> list[str]:
    """CSS basenames under monkie styles/ that feed public skins."""
    names: set[str] = set(SKINS.keys())
    for meta in SKINS.values():
        append = meta.get("append_layout")
        if append:
            names.add(str(append))
    return sorted(names)


def is_public_trigger_path(rel: str) -> bool:
    """True if a monkie-repo-relative path should auto-publish to pp-css."""
    rel = rel.replace("\\", "/").lstrip("./")
    if rel.startswith("styles/assets/"):
        return True
    if rel.startswith("styles/") and rel.count("/") == 1:
        base = rel[len("styles/") :]
        return base in set(public_source_names())
    return False


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


_ASSET_NAME_RE = re.compile(
    r"(?:styles/)?assets/([A-Za-z0-9._@+-]+\.(?:png|jpe?g|svg|webp|gif|ico))",
    re.I,
)


def collect_asset_names(styles: Path) -> set[str]:
    """Asset basenames referenced by public skin sources (or already in pub)."""
    names: set[str] = set()
    for name in public_source_names():
        src = styles / name
        if not src.is_file():
            continue
        try:
            text = src.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in _ASSET_NAME_RE.finditer(text):
            names.add(m.group(1))
    # Always keep logos already published under skins/assets
    dest = HERE / "skins" / "assets"
    if dest.is_dir():
        for p in dest.iterdir():
            if p.is_file() and not p.name.startswith("."):
                names.add(p.name)
    return names


def sync_assets(styles: Path) -> int:
    """Copy monkie styles/assets → skins/assets for public-referenced logos."""
    src_dir = styles / "assets"
    dest_dir = HERE / "skins" / "assets"
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not src_dir.is_dir():
        return 0
    copied = 0
    for name in sorted(collect_asset_names(styles)):
        src = src_dir / name
        if not src.is_file():
            continue
        dest = dest_dir / name
        if dest.is_file() and dest.stat().st_size == src.stat().st_size:
            # same size: still copy if monkie is newer
            if src.stat().st_mtime <= dest.stat().st_mtime:
                continue
        shutil.copy2(src, dest)
        copied += 1
        print(f"  assets/{name}  ({dest.stat().st_size} bytes)")
    return copied


def render_public_css(
    src: Path,
    header: str,
    rewrite_skin_attr: str | None = None,
    logo_cdn: str | None = None,
    append_src: Path | None = None,
) -> str:
    """Build public CSS bytes from monkie SoT (no write). Same transforms as publish."""
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
    return css


def build_one(
    src: Path,
    dest: Path,
    header: str,
    rewrite_skin_attr: str | None = None,
    logo_cdn: str | None = None,
    append_src: Path | None = None,
) -> None:
    css = render_public_css(
        src,
        header,
        rewrite_skin_attr=rewrite_skin_attr,
        logo_cdn=logo_cdn,
        append_src=append_src,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(css, encoding="utf-8")
    print(f"  {dest.relative_to(HERE)}  ({dest.stat().st_size} bytes)")


_BUILD_STAMP_RE = re.compile(
    r"(?m)^[ \t]*/\*[ \t]*pp-css-build:.*?[ \t]*\*/[ \t]*\n?"
    r"|^[ \t]*\*[ \t]*pp-css-build:.*\n?",
)


def normalize_pub_css(css: str) -> str:
    """Strip publish.sh build stamps so content compares equal across rebuilds."""
    return _BUILD_STAMP_RE.sub("", css)


def check_drift(styles: Path, quiet: bool = False) -> list[str]:
    """
    Compare monkie styles/ → expected public skins vs pp-skins/skins/*.css.
    Returns list of drifted skin basenames (empty = in sync).
    Ignores pp-css-build stamps injected by publish.sh after the pure build.
    """
    drifted: list[str] = []
    missing_src: list[str] = []
    missing_pub: list[str] = []
    ok_n = 0

    for name, meta in SKINS.items():
        src = styles / name
        dest = HERE / "skins" / name
        if not src.is_file():
            missing_src.append(name)
            continue
        if not dest.is_file():
            missing_pub.append(name)
            drifted.append(name)
            continue
        append_name = meta.get("append_layout")
        append_src = (styles / append_name) if append_name else None
        expected = normalize_pub_css(
            render_public_css(
                src,
                meta["header"],
                rewrite_skin_attr=meta.get("rewrite_skin_attr"),
                logo_cdn=meta.get("logo_cdn"),
                append_src=append_src,
            )
        )
        actual = normalize_pub_css(dest.read_text(encoding="utf-8"))
        if expected != actual:
            drifted.append(name)
            if not quiet:
                exp_n, act_n = len(expected), len(actual)
                print(
                    f"  ✗ {name}  expected={exp_n}b  published={act_n}b  Δ={act_n - exp_n:+d}",
                    file=sys.stderr,
                )
        else:
            ok_n += 1
            if not quiet:
                print(f"  ✓ {name}  ({len(actual)}b)")

    if not quiet:
        if missing_src:
            print(
                f"  ⚠ monkie styles missing: {', '.join(missing_src)}",
                file=sys.stderr,
            )
        if missing_pub:
            print(
                f"  ⚠ published skins missing: {', '.join(missing_pub)}",
                file=sys.stderr,
            )
        print(
            f"  summary: {ok_n} ok, {len(drifted)} drifted, "
            f"{len(missing_src)} src-missing",
            file=sys.stderr if drifted else sys.stdout,
        )
    return drifted


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--styles",
        type=Path,
        default=HERE.parent / "styles",
        help="Path to source styles directory",
    )
    ap.add_argument(
        "--list-sources",
        action="store_true",
        help="Print monkie styles/ basenames that map to public skins (for hooks)",
    )
    ap.add_argument(
        "--check-path",
        metavar="REL",
        help="Exit 0 if monkie-relative path should trigger auto-publish",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help=(
            "Drift check only: rebuild from monkie styles/ in memory and compare "
            "to pp-skins/skins/*.css. Exit 0 if in sync, 1 if any skin drifted. "
            "Does not write or push."
        ),
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="With --check: only print drifted basenames (one per line)",
    )
    args = ap.parse_args()

    if args.list_sources:
        for n in public_source_names():
            print(n)
        print("styles/assets/*")
        return

    if args.check_path is not None:
        sys.exit(0 if is_public_trigger_path(args.check_path) else 1)

    styles: Path = args.styles
    if not styles.is_dir():
        print(f"styles dir not found: {styles}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        if not args.quiet:
            print(f"Checking pub drift vs monkie SoT: {styles}")
        drifted = check_drift(styles, quiet=args.quiet)
        if args.quiet:
            for name in drifted:
                print(name)
        if drifted:
            if not args.quiet:
                print(
                    "DRIFT: pub skins out of date. Fix:\n"
                    "  ./scripts/sync-pp-pub.sh -m \"sync from monkie\"",
                    file=sys.stderr,
                )
            sys.exit(1)
        if not args.quiet:
            print("OK: pub skins match monkie styles/ (no drift)")
        sys.exit(0)

    print(f"Publishing skins from {styles}")
    n_assets = sync_assets(styles)
    if n_assets:
        print(f"  synced {n_assets} asset file(s)")
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
