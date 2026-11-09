# Code Review Prompt — Land Clearing Charlotte Footer Redesign

Copy everything below the line into a new chat.

---

You are reviewing a footer redesign that was just applied to a static marketing site. You have no prior context, so read the files listed below before forming opinions. **This is a review only: do not edit any files.** Report findings; I will decide what to change.

## Project goals (judge everything against these)

1. **Plain HTML and CSS.** The site is static HTML with one shared stylesheet. There is no framework, build step or bundler, and none should be introduced.
2. **As little JavaScript as possible.** The footer was designed to run zero JS in modern browsers. Any JS in or for the footer has to justify its existence.
3. **As little CSS as possible.** Fewer rules, fewer selectors, fewer overrides, fewer breakpoints. If something can be deleted, merged or simplified without visibly changing the design, that's a finding.
4. **The footer must integrate cleanly with the existing site CSS:** no fighting the cascade, no duplicate or dead rules, no leaks into or out of other components.

## Files to read

Repository root: `H:\Websites\landc\` (git repo; the footer changes are uncommitted, so `git diff` shows exactly what changed).

**Live site (primary review target)**
- `H:\Websites\landc\charlotte-land-clearing\style.css`: the single site stylesheet (~5,580 lines, 136 KB; it was 114 KB before this change).
  - New footer block: starts at the comment `REDESIGNED SITE FOOTER` (~line 1358) and runs ~727 lines, ending just before `/* Pre-footer map section` (~line 2086).
  - Pre-existing rules that sit near or interact with the footer: `.site-map-section` / `.site-footer__map-frame` (crown map section above the footer, intentionally kept), `MOBILE CONVERSION BAR` (`.mobile-sticky-cta`, ~line 3515), the shared responsive blocks at `@media (max-width: 960px)`, `768px` and `640px`, and `@media print` (~line 4880).
  - Run `git diff charlotte-land-clearing/style.css` to see which old footer rules were removed and where the new block went.
- `H:\Websites\landc\charlotte-land-clearing\index.html`: the homepage. Footer markup is `<footer class="site-footer">` (~lines 1479–1658), including a one-line inline fallback `<script>` at the end of the footer.
- `H:\Websites\landc\charlotte-land-clearing\land-clearing-concord-nc\index.html`: a representative depth-1 page (`../` relative paths).
- `H:\Websites\landc\charlotte-land-clearing\lot-clearing-tips\land-clearing-in-western-north-carolina\index.html`: a depth-2 page (`../../` paths).
- `H:\Websites\landc\charlotte-land-clearing\404.html`: uses root-relative `/` paths, unlike every other page.
- `H:\Websites\landc\charlotte-land-clearing\site.js`: the site's shared script. Check that nothing in it touches the footer or duplicates footer behavior.
- `H:\Websites\landc\charlotte-land-clearing\images\logo\lockup-on-navy.svg`: the footer logo.

**Scripts that write footer markup (they must stay in sync with the CSS)**
- `H:\Websites\landc\tools\apply_footer.py`: stamps the footer HTML into all 54 live pages and 21 staged pages; it is idempotent.
- `H:\Websites\landc\tools\gen\build_cities.py`: rewrites the footer's "Service Areas" list (it can output a greyed-out `site-footer__link-item--muted` item for a town without a page yet).
- `H:\Websites\landc\tools\gen\lib.py`: `CLOSING` is sliced from `land-clearing-charlotte-nc/index.html` and reused by `gen_article.py`, `gen_sub.py` and `gen_city.py`, so generated pages inherit whatever footer that page has.
- `H:\Websites\landc\tools\seo_engine\deploy_city_batch.py`: copies `tools\seo_engine\staging\*\index.html` over live pages.
- `H:\Websites\landc\tools\qa.py`: site QA. Run `python tools/qa.py` from the repo root. The baseline after this change is `BROKEN: 0`, `ISSUES: 43`; all 43 existed before the change and are unrelated (mostly page titles).

**Design reference and history (read for intent, not as code to review)**
- `H:\Websites\landc\footer design.png`: the mockup (desktop on top, mobile below).
- `H:\Websites\landc\docs\footer-redesign-implementation-plan.md`: the implementation spec (architecture decisions in section 1).
- `H:\Websites\landc\land-clearing-charlotte\footer-preview\`: the isolated sandbox where the footer was built (`index.html`, `footer-sandbox.css`, `mobile.html`). The live block in `style.css` was generated from `footer-sandbox.css`.

## Key design decisions (verify these hold up, don't take them on faith)

- **One set of links for both layouts:** each link group is a native `<details class="site-footer__accordion">` **without** `open`. Mobile (≤900px) shows them collapsed natively. On desktop (≥901px), CSS keeps them expanded with `.site-footer__accordion::details-content { content-visibility: visible; display: block; }` and `pointer-events: none` on `<summary>`.
- **JS fallback:** a one-line inline script inside `<footer>` runs only when `CSS.supports('selector(::details-content)')` is false and the viewport is desktop width, opening the groups once.
- **Layout tiers:** full 5 columns at ≥1440px; compact 5 columns at 1280–1439px; tablet at 901–1279px; mobile at ≤900px; extra bottom padding for the sticky call/estimate bar at ≤768px.
- **Footer-only CSS variables** (`--ft-*`, `--clc-navy-ink`, `--clc-gold-deep`, `--font-display`) are set on `.site-footer`, not `:root`.
- **Social icon selectors** include `:link` and `:visited` specifically to outrank legacy rules. Check whether those legacy rules still exist; if they were removed, this extra specificity may now be unnecessary.
- **Inline SVG backgrounds:** the background uses two inline SVG images (contour lines, and a pine-forest outline of ~8 KB).

## What to review

Focus on the footer and how it fits the rest of the site. For each area, look for concrete problems, not style preferences.

1. **CSS size and redundancy (highest priority).**
   - Rules, declarations or breakpoints that can be removed or merged without changing the rendered result.
   - Values that repeat the browser default, or that a parent already sets for its children.
   - The four layout tiers: are all four needed? Could fewer breakpoints, or a more fluid grid (`clamp`, `minmax`, `auto-fit`), get the same result?
   - Whether the 1280–1439px "compact" overrides could be replaced by fluid sizing.
   - Whether the ~8 KB tree image and the contour image are worth their weight, or could be smaller, simpler or an external cached `.svg`.
   - Leftovers from the sandbox (sandbox-only comments or tokens, unused classes).
   - Dead selectors: any footer class in `style.css` that no page uses, and any class used in the footer HTML with no styles.
2. **Cascade and integration with the existing stylesheet.**
   - Old footer rules that survived the removal, or pre-existing rules elsewhere in `style.css` that still apply to footer elements (element selectors on `a`, `ul`, `li`, `p`, `details`, `summary`, `svg`; utility classes; later `@media` blocks).
   - Places where the footer CSS fights the cascade (`!important`, extra specificity like `:link`/`:visited`, source-order dependence), and whether that's still needed.
   - Whether footer-only variables duplicate site variables that already exist on `:root` and could just be reused.
   - Whether the footer's breakpoints (900/1280/1440) make sense next to the site's existing ones (960/768/640/480/420). Flag places where mismatched widths cause awkward in-between layouts.
   - Whether the sticky bar and footer padding work together without a gap or overlap at ≤768px and ≤480px.
   - Whether `@media print` still hides the footer correctly.
3. **JavaScript.**
   - Whether the inline fallback is correct, safe, and truly the minimum. Could it be removed (given current `::details-content` support) or replaced with a no-JS pattern?
   - Whether `site.js` has anything left over from an earlier footer approach.
4. **HTML semantics and accessibility.**
   - Whether `<details>`/`<summary>` is right for the desktop "always open" state. Screen readers will announce a collapsed/expanded control that does nothing on desktop, and summaries stay in the tab order. Is there a better no-JS pattern?
   - Heading structure (the footer uses `<summary>` and `<p class="site-footer__contact-title">`, with no headings), link text, `aria-label`s, decorative icon `aria-hidden`, focus-visible styles, color contrast (gold on navy, dimmed text), and tap-target sizes on mobile.
   - Whether `content-visibility` on `::details-content` affects find-in-page or anchor links into the footer.
5. **Scripts that write footer markup.**
   - Whether the regexes in `apply_footer.py` and `build_cities.py` are robust (indentation, attribute order, line endings, a re-run after manual edits).
   - Whether every page type gets correct relative paths (root, depth-1, depth-2, `404.html`, staging).
   - Whether `lib.py`'s `CLOSING` and the generators that use it still produce correct footers.
6. **Performance.** How much the 22 KB stylesheet growth costs, render cost of the background layers and `backdrop-filter`, and image/SVG sizing.

## How to verify (read-only)

- `git diff --stat` and `git diff charlotte-land-clearing/style.css` to see exactly what changed.
- `python tools/qa.py` should still report `BROKEN: 0`, `ISSUES: 43`.
- To view pages, `python tools/serve.py` serves the site locally (check the script for its port), or open the files in a browser. Check the footer at 1920, 1440, 1280, 1024, 768, 390 and 360px wide, and with a Service Areas group opened on mobile. Compare against `footer design.png`.
- To count selector usage, search the `.html` files for each `site-footer__*` class defined in `style.css`.

## Report format

Give findings ranked most severe first, as a numbered list. For each:
- **Severity:** Bug / Integration risk / Bloat / Accessibility / Nitpick
- **Where:** file path and line number (or selector)
- **What:** the problem in one or two sentences, with evidence (the conflicting rule, the unused selector, the width where it breaks)
- **Fix:** the smallest change that solves it. For CSS bloat, give an estimate of lines or bytes saved.

End with:
1. A short **"CSS to delete"** list: rules or declarations that can go with no visible change.
2. A **verdict on the JS fallback:** keep, change or remove, and why.
3. Anything you could **not verify** and why.

Don't pad the report: if an area has no issues, say so in one line.
