# Land Clearing Charlotte: Design System

> Brand: **Land Clearing Charlotte** (landclearingcharlotte.com). Owner-operated land clearing, forestry mulching and brush clearing across Charlotte, NC and the Piedmont.
> Source of truth: the live site at `charlotte-land-clearing/` (`style.css`, `service-page.css`). Every value in this system comes from that code. The one new addition is `gold-ink`, marked **NEW**.

Files: [`tokens.css`](tokens.css) · [`tokens.json`](tokens.json) · [`components.css`](components.css) · [`components.html`](components.html) · `assets/` · `screenshots/`

---

## 1. Brand essence

| | |
|---|---|
| **Promise** | The owner is on every job. You get a firm written price, and the trees you want to keep stay standing. |
| **Personality** | Trustworthy, plain-spoken, practical, local. A working contractor, not an agency. |
| **Audience** | Homeowners, custom-home builders, rural acreage owners, small commercial developers in Mecklenburg, Union, Cabarrus and Gaston counties. |
| **Visual feel** | Deep navy plus "equipment" gold. Clean white cards on a cool off-white page. Big, heavy headings. Real job-site photography. |

### Voice
- Short, direct sentences, in second person ("your lot", "your builder").
- Lead with what the customer gets: a usable lot, keeper trees flagged, erosion handled, a written price.
- Local specifics: Charlotte neighborhoods, Piedmont red clay, lake lots, county names.
- Avoid hype words like "best", "#1", "cheapest", and avoid exclamation marks. Never use em dashes in headlines.

### Content guardrails (must follow)
- **Never claim:** grading, house pads, herbicide or chemical treatment, kudzu or invasive-species removal.
- **Never invent:** reviews, star ratings, prices, years in business, certifications, equipment brands, tree sizes. Use `<!-- TODO: real Google rating -->` as the placeholder.
- **Regulatory facts are hedged.** Use "confirm with the city or county" rather than stating rules as fact.
- **Right-of-way work:** the company clears private easements and access roads directly for landowners. On utility, sewer, water or pipeline corridors it works only as a subcontractor to the contractor.
- **Links:** no links inside body copy. Unbuilt pages appear as dashed, non-clickable "proposed" elements (`div` + `data-href`), never as `<a>`.

### Canonical contact details
| Field | Value |
|---|---|
| Display phone | **(828) 576-3931** |
| `tel:` link | `tel:8285763931` |
| Schema phone | `+1-828-576-3931` |
| Hours | Mon–Sat, 7:00 AM–6:30 PM |
| Address | 1930 Camden Rd Ste 238, Charlotte, NC 28203 |
| Service area | Charlotte, Mecklenburg, Union, Cabarrus & Gaston counties |

---

## 2. Color

### Core palette
| Token | Hex | Role |
|---|---|---|
| `--ds-navy-900` (`--clc-navy-dark`) | `#121E33` | Hero background, footer, sticky CTA |
| `--ds-navy-800` (`--clc-navy`) | `#1B2B48` | Headings, navy buttons, callouts, CTA band |
| `--ds-navy-700` (`--clc-navy-light`) | `#24395E` | Hover on navy |
| `--ds-gold-400` (`--clc-gold`) | `#F2C84B` | **Primary accent**: CTAs, accent borders, logo, step digits |
| `--ds-gold-500` (`--clc-gold-dark`) | `#E0B431` | Gold hover, decorative arrows |
| `--ds-gold-ink` **NEW** | `#8A6A0A` | Gold-family *text* on light backgrounds |
| `--ds-gold-50` | `#FFF8E1` | Pillar-card gradient tint |
| `--ds-slate-600` (`--clc-text`) | `#51607A` | Body text |
| `--ds-slate-500` | `#64748B` | Muted text, proposed items |
| `--ds-slate-300` | `#CBD5E1` | Input borders, dashed proposed borders |
| `--ds-slate-200` (`--clc-border-subtle`) | `#E2E8F0` | Card and section borders |
| `--ds-slate-100` | `#F1F4F9` | Subtle surface |
| `--ds-slate-25` (`--clc-tint`) | `#F8F9FB` | Page background, alternate sections |
| `--ds-white` | `#FFFFFF` | Cards, alternate sections |
| `--ds-slate-275` | `#D3DDEB` | Body text on dark |
| `--ds-slate-350` | `#A3B3CC` | Footer text |

### Silo accents (Other Services group heads)
| Silo | Token | Hex |
|---|---|---|
| Land Clearing | `--ds-color-silo-land` | `#F2C84B` gold |
| Forestry Mulching | `--ds-color-silo-forestry` | `#2F855A` green (also used for the "You're here" current state) |
| Brush Clearing | `--ds-color-silo-brush` | `#C05621` orange |

### Contrast (WCAG 2.1)
| Pair | Ratio | Result |
|---|---|---|
| Navy `#1B2B48` on white | 14.1 | AAA |
| Navy on gold `#F2C84B` | 8.84 | AAA, used for all gold buttons |
| Body `#51607A` on white / tint | 6.36 / 6.03 | AA |
| `#D3DDEB` on navy-900 | 12.2 | AAA |
| Muted `#64748B` on white | 4.76 | AA |
| Green `#2F855A` on white | 4.54 | AA (only 4.31 on tint, so fails for small text) |
| Orange `#C05621` on white | 4.57 | AA |
| **Gold-dark `#E0B431` text on white** | **1.95** | **Fail.** The live site uses it for arrows and "View service →" |
| **Gold `#F2C84B` text on white** | **1.60** | **Fail** |
| Gold-ink `#8A6A0A` on white | 5.06 | AA |

> **Rule:** Gold is a *fill* and *border* color on light backgrounds. It is a text color only on navy. For gold-looking text on white or tint, use `--ds-gold-ink`.

---

## 3. Typography

System font stack only, with no webfonts (fast, and native on every device):
`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`

| Role | Size | Weight | Line-height | Notes |
|---|---|---|---|---|
| Hero H1 | `clamp(2.2rem, 4.4vw, 3.5rem)` | 800 | 1.08 | letter-spacing −.02em; a key phrase in `<span>` turns gold (on navy) |
| Section H2 (`.svc-h2`) | `clamp(1.8rem, 3.2vw, 2.55rem)` | 800 | 1.15 | navy, −.01em |
| Prose H3 | 1.32rem | 800 | | navy |
| Card title | 1.12rem | 800 | | navy |
| Lead | 1.05–1.08rem | 400 | 1.75 | |
| Prose | 1.04rem | 400 | 1.8 | long-form copy |
| Body | 1rem | 400 | 1.65 | `#51607A` |
| Small | .92rem | | | |
| Caption | .86rem | | | figure captions |
| Label | .84rem | 700 | | form labels |
| Eyebrow (`.svc-eyebrow`) | .78rem | 800 | | uppercase, .14em tracking, 3px gold underline |
| Micro tag | .68–.7rem | 800 | | uppercase, .1em (e.g. "Main Service Page", "You're here") |

Weights used: 600, 700, 800, 900. The logo wordmark is outlined Barlow Condensed ExtraBold, not live text.

---

## 4. Layout, spacing, shape

- **Container:** max 1440px, side padding `clamp(16px, 3.5vw, 48px)`.
- **Section rhythm:** vertical padding `clamp(60px, 7vw, 100px)`. Sections **alternate tint → white → tint**.
- **Section head:** eyebrow, then H2, then a lead paragraph. Max width 820px, 40px below.
- **Breakpoints:** 1100 · 960 (nav collapses to drawer) · 768 (sticky CTA appears) · 640 · 480.

| Radius | Use |
|---|---|
| 10px | Inputs, selects |
| 12px | Chips, icon tiles |
| 14px | Area cards, FAQ items, group heads |
| 16px | Cards, process steps |
| 18px | Figures, callouts |
| 20px | Estimate form card |
| 50px | Buttons, pills, tag pills |
| 50% | Step numbers, trust icons |

**Signature accent borders:** a gold *top* border marks premium surfaces: cards 5px, the form card 6px, compact steps, the CTA band and the footer 4px. A gold *left* border (6px) marks group heads and the callout.

### Elevation
| Token | Value | Use |
|---|---|---|
| `--ds-shadow-trust` | `0 8px 24px rgba(27,43,72,.05)` | Trust bar |
| `--ds-shadow-chip-hover` | `0 8px 20px rgba(27,43,72,.10)` | Chip hover |
| `--ds-shadow-card` | `0 14px 34px rgba(27,43,72,.10)` | Cards at rest |
| `--ds-shadow-card-hover` | `0 22px 46px rgba(27,43,72,.18)` | Cards on hover |
| `--ds-shadow-button-hover` | `0 10px 22px rgba(27,43,72,.18)` | Navy button hover |
| `--ds-shadow-gold-glow` | `0 10px 24px rgba(242,200,75,.35)` | Gold button hover |
| `--ds-shadow-form` | `0 30px 60px rgba(0,0,0,.35)` | Form card on the dark hero |

### Motion
All transitions use `.2s ease`. Hover lift: −2px for buttons and chips, −3px for area cards, −5px for homepage cards. The FAQ "+" rotates 45° and turns gold when open. Nothing else animates; keep it calm.

---

## 5. Iconography & imagery

- **Icons:** inline SVG, 24×24 viewBox, `fill="none"`, `stroke="currentColor"`, `stroke-width="2.2"`, round caps. They sit inside 42px gold-tint circles (trust bar) or 48px gold tiles (reasons). No icon fonts.
- **Logo: Tree Line Crown.** A gold Queen City crown whose center point is a tiered pine and whose two side points carry jagged, branch-like teeth, over a cleared-lot wedge. Wordmark: "LAND CLEARING / CHARLOTTE" in Barlow Condensed ExtraBold (800), outlined to shapes, both lines the same width. No subline. On white: gold crown, navy ground and wordmark (`assets/logo.svg`). On navy: white ground, white "LAND CLEARING", gold "CHARLOTTE" (`assets/logo-on-navy.svg`). Symbol alone: `assets/logo-mark.svg` / `logo-mark-on-navy.svg`. App icon: `assets/app-icon.svg` (navy rounded square). Favicon: `assets/favicon.svg`, the same crown with smooth side points, used only at 16 and 32px; use the jagged version at 48px and up. Site: header logo 52px tall (42px under 640px), footer 60px.
- **Photography:** real job-site photos only: Piedmont pine and hardwood, red clay, tracked mulcher. Six approved images are in `assets/images/`. Use `full-lot-clearing` and `forestry-mulcher-active` for heroes, and the `before-` / `after-land-clearing` pair for comparisons. Hero images sit at 32% opacity under a navy gradient. Don't use stock people or AI-generated equipment with fake logos.

---

## 6. Components (class names in `components.css`)

| Component | Classes | Spec & states |
|---|---|---|
| **Button** | `.svc-btn` + `--gold` / `--navy` / `--ghost` | Padding 15×30, pill, 700. Gold = primary CTA (navy text). Navy = secondary (call). Ghost = white outline on dark. Hover: lift −2px plus shadow. |
| **Topbar** | `.site-topbar` | Navy-900 strip with a gold "Fast Response" badge, service area, direct owner line and an estimate link. |
| **Navigation** | `.site-navigation` | White, sticky. Logo image (`.site-navigation__brand-logo`, `assets/logo.svg`), 4 silo links (navy 600 .95rem; hover gold-dark; current = gold inset underline), gold pill CTA. Under 960px it becomes a phone button, hamburger and drawer. |
| **Service hero** | `.svc-hero`, `__eyebrow`, `__checks` | Navy-900, photo at 32%, gradient. Grid 1.2fr / .8fr: H1 + intro + 2 buttons + gold-check list on the left, form card on the right. Breadcrumb above. |
| **Estimate form card** | `.svc-form-card` | `id="estimate"`. White, 20px radius, 6px gold top border, deep shadow. Fields: name, phone, service (select), property size, address, notes, gold submit, "No obligation" plus phone. |
| **Trust bar** | `.svc-trust` | 4 columns: Owner on Every Job · Licensed & Insured · Free On-Site Estimates · one service-specific item. 42px gold-tint icon circles. |
| **Process steps** | `.svc-steps` (+ `--compact`) | 4 cards, each with a navy number circle and a gold digit, title and text. The compact variant has a 4px gold top border. |
| **Area cards** | `.svc-area-card` (+ `--pillar`, `--proposed`) | Pillar card always comes first ("Main Service Page" micro label, gold-50 gradient). Live = `<a>` with an arrow. Proposed = dashed `div` with muted text, not clickable. |
| **Split / figure / callout** | `.svc-split`, `.svc-figure`, `.svc-callout` | Long-form copy with a sticky aside. Figures have an 18px radius and a caption. The callout is a navy card with a 6px gold left border and a gold button. |
| **Group head** | `.svc-group__head` + `--land` / `--forestry` / `--brush` / `--current` / `--proposed` | Left border in the silo color, "Parent / Core Service" micro label, "View service →" link. |
| **Chip** | `.svc-chip` (`a` live / `--current` / `--proposed`) | 12px radius. Live = white with hover lift. Current = green-tint with a "You're here" tag and `aria-current="page"`. Proposed = dashed and muted. |
| **Reasons** | `.svc-reasons` | Why Choose Us cards with a 48px gold icon tile. |
| **FAQ** | `.svc-faq__item` | `<details>`/`<summary>`, 14px radius. "+" rotates and turns gold when open. FAQPage schema is generated from the visible FAQs by `site.js`. |
| **CTA band** | `.svc-cta` | Navy, 4px gold top border, H2, a line of copy, gold and ghost buttons. |
| **Footer** | `.site-footer` | Navy-900, 4px gold top border, 4 columns (brand, services, areas, contact). Text `#A3B3CC`. |
| **Sticky CTA** | `.mobile-sticky-cta` | Under 768px only. Blurred navy bar with "Call Operator" (translucent) and "Free Estimate" (gold). |
| **Homepage silo card** | `.service-catalog__grid-card--elevated-white`, `__tag-pill` | White card with a gold top border, title, text, sub-service pill links, and an arrow link to the pillar. |

---

## 7. Page pattern: service page (9 sections)

1. **Head:** title `{Service} in Charlotte, NC | Land Clearing Charlotte`, meta, canonical, JSON-LD `@graph` (LocalBusiness `@id` + Service + BreadcrumbList).
2. **Hero:** breadcrumb, H1, intro, checks on the left; estimate form (`#estimate`) on the right, above the fold.
3. **Trust bar:** 4 items.
4. **Process:** "What Our {Service} Process Is", 4 steps (compact on sub-service pages).
5. **Where We Serve:** pillar card first, then town cards (live or proposed).
6. **Continuing copy:** split prose plus figure plus callout.
7. **Other Services:** 3 silo groups (Land, Forestry, Brush) with chips; the current page shows the current chip.
8. **Why Choose Us** reasons, then the **FAQ**.
9. **Closing CTA band**, footer, mobile sticky CTA.

Background order: hero (navy) → trust (white) → tint → white → tint → white → tint → white → CTA (navy).

---

## 8. Accessibility

- One H1 per page, then H2 per section. Sections use `aria-labelledby`.
- All interactive targets are at least 44px tall on mobile. Buttons are pill-shaped with 15px vertical padding.
- Gold text only on navy. Use `--ds-gold-ink` on light backgrounds.
- The current page is marked with `aria-current="page"` (nav and chips). Decorative SVGs use `aria-hidden="true"`; hero background images use `alt=""`.
- Form fields have visible `<label>`s. The phone is always a `tel:` link.

## 9. Do / Don't

| Do | Don't |
|---|---|
| Use the navy + gold + white palette with real job photos | Add new hues outside the three silo accents |
| Put a phone number and an estimate CTA on every screen | Hide the CTA below long copy |
| Mark premium surfaces with a gold top border | Use gold text on white or tint |
| Keep sections alternating tint and white | Stack two same-color sections |
| Render unbuilt pages as dashed "proposed" items | Link to pages that don't exist |
| Write hedged, local, specific copy | Invent ratings, prices or claims (grading, herbicide) |
