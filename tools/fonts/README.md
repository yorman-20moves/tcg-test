# Studio faces

The three typefaces of the 20 Moves design system, self-hosted so the workbench
does not need the internet to look like itself. `tools/studio.py` serves this
directory at `/fonts/`; `tools/studio.html` declares them with `@font-face`.

| File | Family | What it is for |
|---|---|---|
| `Anton-400.woff2` | Anton | Display — headings and the one hero numeral |
| `Inter-var.woff2` | Inter (variable, 100–900) | Body, controls, nav |
| `IBMPlexMono-400/500/600.woff2` | IBM Plex Mono | Eyebrows, badges, tags, every figure |

All three are released under the **SIL Open Font License 1.1**, which permits
bundling and redistribution. Source: Google Fonts, latin subset only —
`https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700`

Google serves one variable file for all four requested Inter weights, so the
duplicates were collapsed into `Inter-var.woff2`. Total: ~112 KB.

The design system's own stylesheet (`20 Moves - Latest Design System/design-system.css`)
loads these from the CDN and notes that self-hosted `@font-face` rules should
replace that before production. This directory is that replacement for the Studio.
