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
| **Flame** | Ember + fire accents | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-flame.css` |
| **Synth** | 80s synthwave (magenta / violet / cyan) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-synth.css` |
| **MacLite** | Apple-inspired light UI (SF blue + soft grey) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-maclite.css` |
| **Orpheus Matrix** | OPS green-on-black (standalone) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/orpheus-matrix.css` |
| **Redacted Synth** | RED synthwave magenta / violet / cyan | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/redacted-synth.css` |
| **BTN Dark Ambient** | BroadcasTheNet void + teal aurora (Imagine logo) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/broadcasthe-dark.css` |
| **PTP Cinema Noir** | PassThePopcorn greyscale on Dark (Default) | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/ptp-dark.css` |
| **The Lounge Matrix** | Matrix theme for The Lounge IRC | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/thelounge-matrix.css` |

Example:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.1.0/skins/phoenix-synth.css
```

Prefer a **version tag** so updates don’t change under people unexpectedly.

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

### PTP Cinema Noir — install (passthepopcorn.me)

Greyscale overlay. **Official stylesheet must be Dark (Default)** (layout base).

**Correct**

1. **Edit** → **Stylesheet**
2. **Official:** `Dark (Default)` — must be `static/styles/dark/style.css`
3. Then either:
   - **Monkie:** Custom CSS = **Do not load** (Noir toggle injects overlay), or
   - **No monkie:** Custom = **Append**:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/ptp-dark.css
```

**Wrong (breaks posters / layout)**

```text
https://github.com/PhoenixPhire42/pp-css/blob/main/skins/ptp-dark.css
```

Never set a `github.com/…/blob/…` page as the official stylesheet. Use jsDelivr only for Append.

**Pinned tag**

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@ptp-noir-v1/skins/ptp-dark.css
```

Logo only:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/assets/ptp-logo-noir-header.png
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

### BroadcasTheNet Modern Dark — install (broadcasthe.net)

BTN swaps out the main skin for **External CSS only**, so this sheet is a **full standalone** theme (layout + chrome + colors).

1. Log in → **Edit** (user settings) → stylesheet / external CSS  
2. Stylesheet base can stay **darknround** (BTN still replaces maincss)  
3. Set **External stylesheet URL** to **jsDelivr only**:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@main/skins/broadcasthe-dark.css
```

4. Save → hard-refresh (⌘⇧R)

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
