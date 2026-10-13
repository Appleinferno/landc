# Land Clearing Charlotte: Claude Design system

A design system you can import into **Claude Design**, generated from the live site (`../charlotte-land-clearing/`). Everything you design in Claude will use the site's real colors, type, components and brand rules.

## File map
| File | What it is |
|---|---|
| `DESIGN.md` | Brand guide: voice, content guardrails, tokens, component specs, page pattern, accessibility. **Claude reads this first.** |
| `tokens.css` | CSS variables: primitives → semantic → component, plus legacy `--clc-*` aliases used by the site |
| `tokens.json` | The same tokens in DTCG format (`$value` / `$type`) |
| `components.css` | The full site stylesheet (global chrome + `svc-*` service template), with hex values swapped for tokens. Load after `tokens.css`. |
| `components.html` | Living component library: real markup for every component. Open it in a browser. |
| `assets/logo.svg`, `logo-on-navy.svg`, `logo-mark*.svg`, `app-icon.svg`, `favicon.svg` | Tree Line Crown logo: lockups for white and navy, symbol, app icon, favicon |
| `logo-concepts/` | Logo source files, generator output and the comparison sheet (`preview.html`) |
| `assets/images/*.jpg` | The 6 approved job-site photos (1600px, web-sized) |
| `screenshots/` | Homepage and service page at desktop (1440) and mobile (390), plus the component library |

## Import into Claude Design
Pick one:

1. **Upload (fastest):** zip this `design-system` folder. In Claude, open **Artifacts → Design**, choose to set up or attach a design system, and upload the zip, or upload the files and screenshots as raw uploads.
2. **GitHub:** push this folder to a repo, then connect the repo as the design-system source.
3. **Claude Code:** from `h:\Websites\landc`, run `/design-sync` and point it at `design-system/`.

Zip it from PowerShell:
```powershell
Compress-Archive -Path h:\Websites\landc\design-system\* -DestinationPath h:\Websites\landc\lcc-design-system.zip -Force
```

## Example prompts
- "Using the Land Clearing Charlotte design system, mock up a city page for **Land Clearing in Matthews, NC** following the 9-section service page pattern in DESIGN.md."
- "Design a one-page printable flyer for forestry mulching: navy hero, gold CTA with (828) 576-3931, trust bar items, and the before/after photos."
- "Create a Facebook ad (1200×628) in the brand style: `svc-hero` look, gold `svc-btn--gold` CTA 'Get My Free Estimate'."
- "Prototype a mobile estimate-form flow based on `.svc-form-card` with the same fields and labels."
- "Make a blog article template using `.svc-eyebrow`, `.svc-h2`, prose type and a `.svc-callout`."

## Keeping it in sync
If the site CSS changes, regenerate with the build script used to create this folder (`scratch/build_ds.py` in the agent's conversation folder): it rebuilds `tokens.json`, `components.css`, `components.html` and the images. `tokens.css` and the docs are edited by hand.

> This folder is **not** part of the deployed site and is not listed in `sitemap.xml`.
