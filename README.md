# Phoenix Project (PP) skins

Pure CSS themes for phoenixproject.app, Orpheus Network, Redacted, BroadcasTheNet (BTN),
PassThePopcorn, and related clients.

- No userscript required  
- Install via the site’s **External stylesheet URL** (or Custom Stylesheet paste)  
- PP base stylesheet: **ApolloStage** (recommended for PP skins)  
- OPS Matrix and RED Synth are **self-contained** (no stock skin required)  
- **PTP Cinema Noir** overlays official **Dark (Default)** only

Also includes a **The Lounge** Matrix theme (paste into Custom Stylesheet).

---

## Install (phoenixproject.app)

1. Log in → **Edit settings**
2. **Site Appearance Settings**
3. **Stylesheet:** `ApolloStage`
4. **External stylesheet URL:** paste one of the links below
5. Save → hard-refresh the page

One external skin at a time. Switch skins by changing the URL.

---

## Skins (jsDelivr)

Published under **PhoenixPhire42/pp-css**. Replace `TAG` with a release tag (e.g. `v1.0.0`) or use `main`.

| Skin | Look | URL |
|------|------|-----|
| **Neo Phoenix** | Matrix green-on-black | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-neo.css` |
| **Dark** | Charcoal + rose-ember | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-dark.css` |
| **Flame** | Ember + fire accents · **standalone** (do not also load ApolloStage) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.2.1-flame/skins/phoenix-flame.css` |
| **Synth** | 80s synthwave (magenta / violet / cyan) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-synth.css` |
| **MacLite** | Apple-inspired light UI (SF blue + soft grey) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-maclite.css` |
| **Orpheus Matrix** | OPS green-on-black (standalone) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/orpheus-matrix.css` |
| **Redacted Synth** | RED synthwave magenta / violet / cyan | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/redacted-synth.css` |
| **BTN Dark Ambient** | BroadcasTheNet void + teal on **darknround** (Imagine logo) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/broadcasthe-dark.css` |
| **PTP Cinema Noir** | PassThePopcorn greyscale on Dark (Default) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/ptp-dark.css` |
| **PTP Blade Runner** | PassThePopcorn cyan/magenta/amber neon on Dark | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/ptp-runner.css` |
| **The Lounge Matrix** | Matrix theme for The Lounge IRC | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/thelounge-matrix.css` |

Example:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.1.0/skins/phoenix-synth.css
```

Prefer a **version tag or commit pin** so updates don’t change under people unexpectedly.


## Monkie ↔ public sync

**Source of truth:** `-=monkies=-/styles/*.css` (this machine).

```bash
cd ~/Developer/xrepo/-=monkies=-/pp-skins
./publish.sh -m "sync skins from monkie"
# or:
python3 publish-from-styles.py --styles ../styles
git add skins && git commit -m "sync" && git push && ./purge-jsdelivr.sh main
```

Public CSS is monkie CSS after `soft_clean` (private DNU/`monkies-*` attrs stripped, public header).  
Visual/layout rules (menu lock, toolbox, logos, colors) must match monkie.

### CDN sync (jsDelivr)

`@main` can lag behind GitHub. This repo keeps it fresh with:

| Tool | What |
|------|------|
| **GitHub Action** `.github/workflows/purge-jsdelivr.yml` | Purges all `skins/**` on every push to `main` |
| **`./purge-jsdelivr.sh [ref]`** | Manual purge (`main`, a tag, or sha) |
| **`./publish.sh`** | Build from monkie `styles/` → commit → push → purge |

After a publish, install URLs:

```text
# best — immutable commit pin (from publish.sh output)
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@<sha>/skins/phoenix-flame.css

# main — after Action/purge (may take 1–2 min)
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-flame.css
```

Verify freshness: open the CSS URL and look for `pp-css-build:` / `flame-build:` near the top.

### Flame — install (standalone)

1. **Edit settings → Site Appearance**
2. **Stylesheet:** leave as-is only if the site *requires* one; best: pick a minimal base **or** clear external-only if your gazelle allows it.
3. **Do not** stack ApolloStage + Flame external (both are full skins → broken layout).
4. **External stylesheet URL** (use the **tag pin**, not bare `@main` — jsDelivr caches `@main` for a long time):

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.2.1-flame/skins/phoenix-flame.css
```

5. Save → hard-refresh. View source: you should see that `phoenix-flame.css` link; optional check the file starts with `flame-build:` / `STANDALONE`.



### MacLite — install (phoenixproject.app)

Apple-inspired **light** UI (SF blue accents, soft grey chrome). Self-contained pure CSS.

1. Log in → **Edit settings** → **Site Appearance Settings**
2. **Stylesheet:** `ApolloStage` (or leave minimal if the site allows external-only)
3. **External stylesheet URL** — use **jsDelivr only**:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/phoenix-maclite.css
```

4. Save → hard-refresh (⌘⇧R)

**Do not use `raw.githubusercontent.com`.** GitHub serves that as `text/plain` with `X-Content-Type-Options: nosniff`, so the browser refuses the CSS and the page can go unstyled/white.

Prefer a version tag when available:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-maclite.css
```

### PTP skins — Noir & Blade Runner (passthepopcorn.me)

Both are **overlays**. **Official stylesheet must be Dark (Default)** (`static/styles/dark/style.css`).

**Monkie (recommended)**  
Custom CSS = **Do not load**. Fixed pill cycles: **Noir → Runner → Stock**.

**No monkie — Append one of:**

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/ptp-dark.css
```

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/ptp-runner.css
```

**Wrong:** `github.com/…/blob/…` as official stylesheet (breaks layout).

| Skin | Look |
|------|------|
| Noir | Pure greys + silver wordmark |
| Runner | Void black, cyan/magenta/amber neon, rain ambient |

Logos:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/assets/ptp-logo-noir-header.png
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/assets/ptp-logo-runner-header.jpg
```

### Orpheus Matrix — install (orpheus.network)

1. Log in → **Edit** (user settings) → appearance / stylesheet
2. Set **External stylesheet URL** (or equivalent custom CSS URL field) to:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/orpheus-matrix.css
```

3. Save → hard-refresh

Or use a versioned tag (recommended once tagged):

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/orpheus-matrix.css
```

Raw GitHub (if jsDelivr lags):

```text
https://raw.githubusercontent.com/PhoenixPhire42/pp-css/main/skins/orpheus-matrix.css
```

Self-contained: no monkie userscript, no stock Apollostage dependency.

### Redacted Synth — install (redacted.sh)

1. Log in → **Edit** (user settings) → appearance / stylesheet  
2. Set **External stylesheet URL** to:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/redacted-synth.css
```

3. Save → hard-refresh  

Prefer a version tag when available:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/redacted-synth.css
```

Raw GitHub:

```text
https://raw.githubusercontent.com/PhoenixPhire42/pp-css/main/skins/redacted-synth.css
```

Self-contained synthwave theme (no monkie userscript). If the site also loads a stock skin, disable or set it to a minimal base so it doesn’t fight the standalone sheet.

### BroadcasTheNet Dark Ambient — install (broadcasthe.net)

**Overlay on official darknround** (same model as PTP Noir on Dark Default).  
Stock owns geometry (`#wrapper` 980, logo 960×140, menu pull-up, chips); this sheet is palette, aurora body, Imagine logo, glass chrome.

1. Log in → **Edit** (user settings) → stylesheet / external CSS  
2. **Stylesheet:** `darknround` (required base)  
3. **External stylesheet URL** — jsDelivr only (prefer Append if the site offers it):

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/broadcasthe-dark.css
```

4. Save → hard-refresh (⌘⇧R)

If External **replaces** maincss, the sheet still re-asserts darknround sizes so layout holds — but keeping **darknround** loaded is best.

**Do not use `raw.githubusercontent.com`.** GitHub serves that as `text/plain` with `X-Content-Type-Options: nosniff`, so the browser refuses the CSS and you get a white/unstyled page.

### The Lounge Matrix — install

1. Open The Lounge → **Settings** → enable **Advanced**
2. Open the raw CSS:  
   https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/thelounge-matrix.css  
   (or open the file in this repo under `skins/`)
3. Copy all CSS → paste into **Custom Stylesheet**
4. Click outside the field; hard-refresh if needed

Failsafe: load Lounge with `?nocss` if a stylesheet bricks the UI.

Share / raw GitHub:

```text
https://github.com/PhoenixPhire42/pp-css/blob/main/skins/thelounge-matrix.css
https://raw.githubusercontent.com/PhoenixPhire42/pp-css/main/skins/thelounge-matrix.css
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/thelounge-matrix.css
```

---

## Files

```text
skins/phoenix-dark.css
skins/phoenix-flame.css
skins/phoenix-neo.css
skins/phoenix-synth.css
skins/phoenix-maclite.css
skins/orpheus-matrix.css
skins/redacted-synth.css
skins/broadcasthe-dark.css
skins/thelounge-matrix.css
```

Self-contained CSS (embedded assets where needed). No third-party runtime.

---

## Adding a skin

1. Add `skins/phoenix-<name>.css` (or another clear name)
2. Document it in this README and `CATALOG.md`
3. Commit, tag (e.g. `v1.1.0`), push

---

## License

CSS provided as-is for personal use. No warranty.
