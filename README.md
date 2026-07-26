# Phoenix Project (PP) skins

Pure CSS themes for phoenixproject.app and related clients.

- No userscript required for PP skins  
- Install via the site’s **External stylesheet URL**  
- Base stylesheet: **ApolloStage** (recommended for PP)

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
| **Dark** | Charcoal + soft orange | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-dark.css` |
| **Flame** | Ember + fire accents | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/phoenix-flame.css` |
| **The Lounge Matrix** | Matrix theme for The Lounge IRC | `https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@TAG/skins/thelounge-matrix.css` |

Example:

```text
https://cdn.jsdelivr.net/gh/PhoenixPhire42/pp-css@v1.0.0/skins/phoenix-neo.css
```

Prefer a **version tag** so updates don’t change under people unexpectedly.

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
