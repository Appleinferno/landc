# Prompt: Build the Forestry Mulching Silo (Core Service #2) — Charlotte Land Clearing

Copy everything below the line into a new chat.

---

You are continuing work on **charlottelandclearing.com**, a static HTML SEO lead-gen site for a land clearing company. Project folder: `h:\Websites\landc\charlotte-land-clearing\`. Read these before writing anything:

- `h:\Websites\landc\docs\charlotte-land-clearing-silo-structure.md`: the approved silo rules
- `charlotte-land-clearing/forestry-mulching-charlotte-nc/index.html`: the **parent pillar** for this silo, already built
- `charlotte-land-clearing/land-clearing-huntersville-nc/index.html`: the reference for a **child/tighter** page (compact process, pillar card first)
- `charlotte-land-clearing/service-page.css` and `site.js`: the shared template. Use the existing `svc-*` classes and don't add new CSS unless it's truly needed.

## Goal
Build out the **Forestry Mulching** silo by creating its **Charlotte sub-service pages**. The pillar `/forestry-mulching-charlotte-nc/` already exists.

## Pages to build (one folder + `index.html` each)
| # | URL | H1 |
|---|---|---|
| 1 | `/underbrush-clearing-charlotte-nc/` | Underbrush Clearing in Charlotte, NC |
| 2 | `/pasture-clearing-charlotte-nc/` | Pasture & Field Reclamation in Charlotte, NC |
| 3 | `/trail-cutting-charlotte-nc/` | Trail Cutting in Charlotte, NC |
| 4 | `/food-plot-clearing-charlotte-nc/` | Hunting Land & Food Plot Clearing in Charlotte, NC |
| 5 | `/right-of-way-clearing-charlotte-nc/` | Right-of-Way & Easement Clearing in Charlotte, NC |
| 6 | `/survey-line-clearing-charlotte-nc/` | Survey Line Clearing in Charlotte, NC |
| 7 | `/woodland-thinning-charlotte-nc/` | Woodland Thinning in Charlotte, NC |
| 8 | `/firebreak-clearing-charlotte-nc/` | Firebreak & Fuel Reduction in Charlotte, NC |

Build them in this order. If output length is a concern, build #1 and #5 first, show them to me, then continue.

## Non-negotiable structure rules
1. **URL format:** `/{service}-{city}-{state}/`, service first, lowercase, hyphens, trailing slash. Assets load via `../style.css`, `../service-page.css`, `../site.js`, `../images/*.png`.
2. **Same 9-section skeleton** as the pillar, at sub-service depth (about 1,000–1,500 words of unique copy):
   1. Title/meta, canonical, JSON-LD `@graph` (LocalBusiness `@id` reuse + Service + BreadcrumbList: Home > Forestry Mulching in Charlotte, NC > this page)
   2. Hero: H1 + intro on the left; estimate form `id="estimate"` on the right, above the fold. Service select preselects **Forestry Mulching**, or **Right-of-Way Clearing** on page #5.
   3. Trust bar: Owner on Every Job, Licensed & Insured, Free On-Site Estimates, plus one item specific to the service. Keep the `<!-- TODO: real Google rating -->` comment.
   4. H2 "What Our {Service} Process Is": `svc-steps svc-steps--compact`, 4 steps written for this service
   5. H2 "Where We Serve": **first card = `svc-area-card--pillar` linking `../forestry-mulching-charlotte-nc/`** with the label "Main Service Page". Then town cards for `{service}-{town}-nc` for Huntersville, Mint Hill, Waxhaw, Concord, Mooresville and Indian Trail. All are unbuilt, so render them as `div.svc-area-card--proposed` with `data-href`.
   6. Continuing copy: `svc-split` with H3 sections plus a figure and callout. **No links in body copy.**
   7. H2 "Other Services We Provide in Charlotte" in this order:
      - The Forestry group first. Its head **links** to the pillar `../forestry-mulching-charlotte-nc/`. Its chips are the 8 sibling subs: chips for pages built in this session are real `<a class="svc-chip">` links, and the current page's chip is marked as current, not a link.
      - The Land Clearing group (head links to `../land-clearing-charlotte-nc/`; subs proposed).
      - The Brush Clearing group (head links to `../brush-clearing-charlotte-nc/`; subs proposed).
   8. H2 "Why Choose Us": 3–6 reasons specific to the service plus a short paragraph
   9. H2 "Charlotte {Service} FAQs": 8–10 unique FAQs in `details.svc-faq__item` (site.js builds the FAQ schema automatically)
   - Then the closing CTA band, footer and mobile sticky CTA, copied exactly from the pillar. Header `aria-current="page"` goes on **Forestry Mulching**.
3. **Never link to a page that doesn't exist.** Use dashed `--proposed` divs with `data-href`.
4. **Every page must be 100% unique.** No paragraphs reused between subs or from the pillar. Each page needs its own angle, local detail, process steps and FAQs.

## Content guidance per page
- **Underbrush:** privet and invasive understory in Charlotte's hardwood lots, opening up views, keeping the canopy, tick and snake habitat reduction.
- **Pasture:** cedar, sweetgum and pine encroachment on old fields in east and south Mecklenburg and the Union County edge, fence rows, reseeding afterward.
- **Trail cutting:** walking, ATV and horse trails; widths; drainage and erosion on red clay slopes; keeping trails clear of creek buffers.
- **Food plots:** hunting tracts on the rural outskirts and in nearby counties, plot sizing, shooting lanes, timing before planting season.
- **Right-of-way** (confirmed service): private easements, access roads, utility and pipeline corridors for contractors, gated access, insurance and COI documentation. Mention that utility-owned corridors are coordinated with the utility.
- **Survey lines:** clearing for surveyors, boundary disputes, pre-sale and pre-fence; narrow, low-impact cutting.
- **Woodland thinning:** removing suppressed, dead and crowded stems to improve forest health and views; keeping the healthiest hardwoods.
- **Firebreak/fuel reduction:** defensible space around structures on wooded acreage and reducing ladder fuels. Keep the claims modest; don't promise fire protection.

## Hedged facts you may use (always add "confirm with the city or county")
- NC requires an erosion and sedimentation control plan for most land disturbance over 1 acre.
- Charlotte's tree ordinance applies mainly to commercial and new development; trees in the public right-of-way belong to the city.
- Mecklenburg County stream buffer rules (S.W.I.M.) limit clearing near creeks.
- Open burning of clearing debris is heavily restricted in Mecklenburg County, and mulching avoids burning.

## Do NOT
- Invent reviews, ratings, testimonials, project stories, prices, years in business or certifications.
- Add services I haven't confirmed (stump grinding, herbicide, lakefront, storm cleanup, grading).
- Put internal links inside paragraphs.
- Change the shared CSS/JS in ways that break the 5 existing pages.

## After building, update existing pages
1. In `forestry-mulching-charlotte-nc/index.html`, `land-clearing-charlotte-nc/index.html` and `brush-clearing-charlotte-nc/index.html`, convert the Forestry sub chips you built from `div.svc-chip--proposed` to `<a class="svc-chip" href="...">`.
2. Leave the Huntersville and Mint Hill pages alone. Their chips are city-matched (`-huntersville-nc`), so they stay proposed.
3. Run a link check: start `python -m http.server 8000` from `charlotte-land-clearing\`, request every new URL plus the 3 pillars, and confirm a 200 status for each. Also confirm no `<a href>` points to a missing folder.
4. Open every new page in Chrome: `Start-Process chrome "http://localhost:8000/<slug>/"`.

## Final reply format
Keep it short: a table of the pages built with links, which existing pages were updated, the link-check result, and any open questions (for example, details of the right-of-way work: utility corridors vs. private easements, and any typical corridor widths).
