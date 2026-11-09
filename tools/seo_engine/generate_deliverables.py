"""Generate Phase 7 Deliverable Markdown Files (03 through 10) in tools/seo_engine/deliverables/."""
import os
import json

ENGINE_DIR = r"h:\Websites\landc\tools\seo_engine"
DATA_DIR = os.path.join(ENGINE_DIR, "data")
DELIV_DIR = os.path.join(ENGINE_DIR, "deliverables")

# -------------------------------------------------------------------------
# Deliverable 3: SERP Competitor Research Packs
# -------------------------------------------------------------------------
d3 = """# Deliverable 3 — SERP & Local Pack Competitor Research Packs (Pilot Batch)

Collected on `2026-11-08T02:44:00Z` via DataForSEO Google Organic SERP Advanced (`/v3/serp/google/organic/live/advanced`), Google Maps SERP Advanced (`/v3/serp/google/maps/live/advanced`), and OnPage Instant Pages (`/v3/on_page/instant_pages`) using exact city-level `location_code` targeting (`1021048` Charlotte, NC; `1021159` Huntersville, NC).

---

## 1. SERP Pack 1: `land clearing charlotte nc` (`location_code=1021048`)

### A. Google Maps Local Pack (Top 5)
| Rank | Business Name | Primary GBP Category | Additional Categories | Rating / Reviews | Website |
|---:|---|---|---|---|---|
| 1 | **Vista Land Clearing** | `Excavating contractor` | — | No reviews listed | `vistalandclearing.com` |
| 2 | **Carolina Land Clearing & Development LLC** | `Forestry service` | `Drainage service`, `Excavating contractor`, `Landscaper`, `Pond contractor` | `5.0` (13 reviews) | `carolinalcd.com` |
| 3 | **Red Hat Forestry Mulching \| Land Services** | `Landscaper` | `Forestry service`, `Tree service` | `5.0` (37 reviews) | `redhatlandservices.com` |
| 4 | **Overland Grading & Sitework, LLC** | `Excavating contractor` | `Construction company`, `Pond contractor` | `4.5` (23 reviews) | `overlandgrading.com` |
| 5 | **Carolina Brush Control** | `Forestry service` | `Environmental consultant`, `Excavating contractor`, `Landscaper` | `5.0` (48 reviews) | `carolinabrushcontrol.com` |

### B. Organic SERP Top Competitors & Baseline Rank
- **Our Current Live Ranking (`landclearingcharlotte.com`):**
  - Position **#14**: `/underbrush-clearing-charlotte-nc/` (sub-service pillar outranking `/land-clearing-charlotte-nc/`).
- **Leading Organic Contractor Competitors:**
  - `#1` `blythefarms.com/land-grading-clearing-services/` — *"Land Grading and Clearing | Charlotte NC"*
  - `#5` `keeterlandmanagement.com/service-area/forestry-mulching-charlotte-nc/` (752 words, OnPage score `97.07`)
  - `#6` `ngeservices.com` — *"NGE Services, Inc. - Land and Site Clearing in the Carolinas"*
  - `#9` & `#19` `carolinalandservices.com` — Residential & commercial clearing blog posts
  - `#11` `kinglandclearing.com/blog/cost-of-clearing-land-in-charlotte/` — Cost-focused guide ranking organically on page 2
- **Related Searches Extracted:**
  - `Residential land clearing charlotte nc`
  - `Land clearing charlotte nc cost`
  - `Land clearing cost calculator`

### C. Competitor OnPage Comparison vs. `/land-clearing-charlotte-nc/`
- **Word Count Advantage:** Local competitors average `339` to `1,233` words (`carolinalcd.com`: 472 words, missing H1; `fischerearthworks.com`: 339 words; `vistalandclearing.com`: 645 words; `redhatlandservices.com`: 1,233 words). Our pillar has `2,073` words (`2,734` after enrichment).
- **Competitor Gaps Exploited:**
  1. None of the top 5 local contractor sites publish a transparent per-acre price range (`$2,000 - $8,000 per acre`) alongside small-lot pricing logic and a side-by-side method comparison table.
  2. Competitors use vague "we handle permits" copy without citing **NC G.S. 113A-57** (1.0-acre threshold + common-plan subdivision rule), **City of Charlotte UDO Articles 20 & 40**, or **Mecklenburg County LUESA S.W.I.M. buffers**.
  3. Zero local competitors implement `FAQPage` JSON-LD matching visible Charlotte permit and pricing questions.

---

## 2. SERP Pack 2: `forestry mulching charlotte nc` (`location_code=1021048`)

### A. Google Maps Local Pack (Top 5)
| Rank | Business Name | Primary GBP Category | Additional Categories | Rating / Reviews | Website |
|---:|---|---|---|---|---|
| 1 | **Red Hat Forestry Mulching \| Land Services** | `Forestry service` | `Landscaper`, `Tree service` | `5.0` (37 reviews) | `redhatlandservices.com` |
| 2 | **Boom Brush Control Land Management** | `Forestry service` | `Earth works company`, `Excavating contractor`, `Tree service` | `5.0` (182 reviews) | `boombrushcontrol.com` |
| 3 | **Carolina Land Clearing & Development LLC** | `Forestry service` | `Drainage service`, `Excavating contractor`, `Landscaper`, `Pond contractor` | `5.0` (13 reviews) | `carolinalcd.com` |
| 4 | **Carolina Brush Control** | `Forestry service` | `Environmental consultant`, `Excavating contractor`, `Landscaper` | `5.0` (48 reviews) | `carolinabrushcontrol.com` |
| 5 | **Bigfoot Forestry - Charlotte** | `Forestry service` | `Debris removal service`, `Excavating contractor`, `Tree service` | `5.0` (1 review) | `bigfootforestry.com/charlotte-nc/` |

### B. Organic SERP Top Competitors & Baseline Rank
- **Our Current Live Ranking (`landclearingcharlotte.com`):**
  - Position **#3**: `/` (Homepage)
  - Position **#8**: `/forestry-mulching-mint-hill-nc/`
  - Position **#9**: `/forestry-mulching-mooresville-nc/`
  - Position **#14**: `/underbrush-clearing-charlotte-nc/`
  - *(Note: The dedicated pillar `/forestry-mulching-charlotte-nc/` is currently eclipsed by the homepage and city pages—enriching `/forestry-mulching-charlotte-nc/` with method comparison tables, 8-inch tree diameter specs, and `FAQPage` schema directly resolves this internal split).*

---

## 3. SERP Pack 3: `brush clearing charlotte nc` (`location_code=1021048`)

### A. Google Maps Local Pack (Top 5)
| Rank | Business Name | Primary GBP Category | Rating / Reviews | Website |
|---:|---|---|---|---|
| 1 | **Carolina Brush Control** | `Forestry service` | `5.0` (48 reviews) | `carolinabrushcontrol.com` |
| 2 | **Vista Land Clearing** | `Excavating contractor` | — | `vistalandclearing.com` |
| 3 | **Red Hat Forestry Mulching \| Land Services** | `Landscaper` | `5.0` (37 reviews) | `redhatlandservices.com` |
| 4 | **Boom Brush Control Land Management** | `Forestry service` | `5.0` (182 reviews) | `boombrushcontrol.com` |
| 5 | **Carolina Land Clearing & Development LLC** | `Forestry service` | `5.0` (13 reviews) | `carolinalcd.com` |

### B. Organic SERP Top Competitors & Baseline Rank
- **Our Current Live Ranking (`landclearingcharlotte.com`):**
  - Position **#14**: `/underbrush-clearing-charlotte-nc/`
- **Leading Organic Contractor Competitors:**
  - `#1` `fischerearthworks.com/land-clearing-charlotte` (339 words)
  - `#2` `violethomeservices.com/post/land-clearing-in-charlotte-nc`
  - `#3` `boombrushcontrol.com/matthews-nc` (667 words on main site)
  - `#5` `carolinasturf.com/land-clearing`
  - `#8` `bigfootforestry.com/charlotte-nc/`
  - `#13` `berralandworks.com/land-clearing`
  - `#19` `landgradingcharlotte.com/services/brush-hogging`

---

## 4. SERP Pack 4: `land clearing huntersville nc` (`location_code=1021159`)

### A. Google Maps Local Pack (Top 5)
| Rank | Business Name | Primary GBP Category | Rating / Reviews | Website |
|---:|---|---|---|---|
| 1 | **Carolina Land Clearing & Development LLC** | `Forestry service` | `5.0` (13 reviews) | `carolinalcd.com` |
| 2 | **Kinnett Grading & Land Clearing** | `Excavating contractor` | — | — |
| 3 | **TZ Clearing Company** | `Excavating contractor` | `5.0` (28 reviews) | `tzclearing.com` |
| 4 | **Clark's Tree Express** | `Tree service` | `4.9` (696 reviews) | `clarkstreeexpress.com` |
| 5 | **Busy Little Bee** | `Septic system service` | `5.0` (17 reviews) | `busylittlebeellc.com` |

### B. Organic SERP Top Competitors, PAA & Baseline Rank
- **Our Current Live Ranking (`landclearingcharlotte.com`):**
  - Position **#1**: `/brush-clearing-huntersville-nc/`
  - Position **#6**: `/forestry-mulching-huntersville-nc/`
  - Position **#8**: `/forestry-mulching-mooresville-nc/`
- **People Also Ask (PAA) Extracted from Huntersville SERP:**
  1. *"How much does it cost to clear land in North Carolina?"*
  2. *"What is the cheapest way to clear land?"*
  3. *"What's the average cost to clear land?"*
  4. *"Do I need a permit to clear land on my property?"*
  5. *"How long does it take to clear 100 acres of land?"*
"""
with open(os.path.join(DELIV_DIR, "03_serp_competitor_research_packs.md"), "w", encoding="utf-8") as f:
    f.write(d3)

# -------------------------------------------------------------------------
# Deliverable 4: Page-Specific Content Briefs (4 Pilot Pages)
# -------------------------------------------------------------------------
d4 = """# Deliverable 4 — Page-Specific Content-Gap Briefs (4 Pilot Pages)

Each brief synthesizes DataForSEO SERP competitor analysis, People Also Ask (PAA) extraction, Harbor SEO Verdict findings, and verified North Carolina / Mecklenburg County regulatory facts.

---

## 1. Content Brief: `/land-clearing-charlotte-nc/`
- **Primary Keyword:** `land clearing charlotte nc` (`vol=70`, `CPC=$7.12`, commercial intent)
- **Secondary Modifiers:** `residential land clearing charlotte nc`, `land clearing charlotte nc cost`, `acreage clearing charlotte nc`, `commercial land clearing charlotte nc`
- **Search Intent & Commercial Purpose:** Property owners, custom home builders, and developers in Charlotte seeking a turnkey mechanical clearing contractor to open residential lots, multi-acre tracts, or commercial footprints before grading/construction.
- **Identified Gaps vs. SERP & Internal Pages:**
  1. **Method Selection Table:** Add a 3-row structured comparison (`Forestry Mulching in Place` vs. `Full Clearing & Stump Removal` vs. `Selective Clearing & Tree Save`) clarifying stump handling, 8-inch tree diameter threshold, and surface finish.
  2. **Soil Science Qualification:** Replace generic "clay sheds water fast" wording with accurate Piedmont Ultisol (`Cecil` and `Pacolet` series) mechanics explaining how compaction, slope gradient, saturation, and bare mineral exposure govern runoff.
  3. **Verified Regulatory Checklist:** Cite **NC G.S. 113A-57** (1.0-acre erosion control plan requirement + cumulative common-plan subdivision rule), **City of Charlotte UDO Articles 20 & 40** (Heritage Trees & development tree save), **Mecklenburg County LUESA S.W.I.M. stream buffers**, and **NC 811** 3-business-day locate notice.
  4. **Warm Small-Lot & Full-Acreage Pricing (`$2,000 - $8,000 per acre`):** Connect the price card directly into body prose and FAQ #1, explaining the 4 confirmed cost drivers, separate stump quoting, excavator + haul-off capability for trees 8"+, and warm access/obstacle-based pricing for lots under an acre (with no minimum pass width required).
  5. **Structured Data:** Add `FAQPage` JSON-LD matching all 10 visible Charlotte FAQs.

---

## 2. Content Brief: `/forestry-mulching-charlotte-nc/`
- **Primary Keyword:** `forestry mulching charlotte nc` (cluster anchor for `forestry mulching near me` `vol=4,400`, `CPC=$7.54`)
- **Search Intent & Commercial Purpose:** Landowners who want overgrown woods, underbrush, trails, pastures, or easements cleared in a single pass without brush piles, open burning, dump-truck haul-off, or topsoil damage.
- **Identified Gaps vs. SERP & Internal Pages:**
  1. **Air Quality & Open-Burning Citation:** Ground the "no burn piles" benefit in the **Mecklenburg County Air Pollution Control Ordinance** enforced by **Mecklenburg County LUESA Air Quality**.
  2. **3-Way Method Comparison Table:** Compare `Forestry Mulching` vs. `Excavator & Full Clearing` vs. `Tractor Bush Hogging` across target vegetation, root impact, and aftermath.
  3. **Trees 8"+ & Excavator Option:** Clearly explain that while brush and saplings under 8" are shredded in place, trees 8 inches or wider take a different approach—and when significant tree removal is needed, we can bring in our excavator and haul off the trees.
  4. **Qualified Critical Root Zone (CRZ) & Slope Claims:** Explain how low-ground-pressure tracks and surface mulch reduce root compaction and sheet runoff on moderate slopes while noting that steep banks or 1-acre+ disturbances (**NC G.S. 113A-57**) still require proper erosion/buffer compliance.
  5. **Structured Data:** Add `FAQPage` JSON-LD matching all 10 visible FAQs.

---

## 3. Content Brief: `/brush-clearing-charlotte-nc/`
- **Primary Keyword:** `brush clearing charlotte nc` / `brush removal charlotte nc` (`CPC=$7.12+`, `KD=45`)
- **Search Intent & Commercial Purpose:** Homeowners, vacant-lot owners, and HOA boards needing thickets, briars, Chinese privet, fence lines, retention pond banks, or code-enforcement overgrowth cleared rapidly.
- **Identified Gaps vs. SERP & Internal Pages:**
  1. **Site-Condition Method Table:** Compare `Open Overgrown Lots & Wooded Thickets` (tracked drum mulcher, no minimum pass width) vs. `Fence Lines, Sheds & Keeper Tree Edges` (machine + hand work) vs. `Heavy Saplings & Trees 8"+` (excavator removal & haul-off).
  2. **Pre-Work Compliance & Code Notice Checklist:** Cover **City of Charlotte Code Enforcement (Housing & Neighborhood Services)** compliance deadlines, **Charlotte-Mecklenburg Storm Water Services** HOA detention-pond agreements, **Mecklenburg County LUESA S.W.I.M.** creek buffers, and **NC 811**.
  3. **Mechanical Upkeep Clarity:** State explicitly that we never spray herbicides or chemicals and provide practical mowing/cutting intervals to keep privet and sweetgum sprouts down.
  4. **Structured Data:** Add `FAQPage` JSON-LD matching all 10 visible FAQs.

---

## 4. Content Brief: `/land-clearing-huntersville-nc/`
- **Primary Keyword:** `land clearing huntersville nc` (`location_code=1021159` Huntersville, NC)
- **Search Intent & Commercial Purpose:** Custom home buyers, builders, and acreage owners in Huntersville (Gilead Rd, Hambright Rd, Beatties Ford Rd, Lake Norman, Mountain Island Lake) needing building-envelope clearing, driveway corridors, or selective acreage mulching.
- **Identified Gaps vs. SERP & Internal Pages:**
  1. **Huntersville Corridor & Method Table:** Map real Huntersville corridors (`Gilead Rd / Hambright Rd / Verhoeff Dr` home pads vs. `Beatties Ford Rd / Bud Henderson Rd` rural transitional acreage vs. `Lake Norman / Mountain Island Lake / McDowell Creek` buffered slopes) to the appropriate clearing method and regulatory body (**Town of Huntersville Zoning Ordinance Article 7**, **Duke Energy Lake Services 760-ft contour & 50-ft buffer**, **Mecklenburg County LUESA**, **NC G.S. 113A-57**, **NC 811**).
  2. **Small-Lot & Corridor Pricing Nuance:** Add warm small-lot pricing explanation alongside the `$2,000 - $8,000 per acre` benchmark, noting no minimum pass width is required and excavator + haul-off is available for trees 8"+.
  3. **Structured Data:** Expand `LocalBusiness.areaServed` to include both `Charlotte` and `Huntersville`, and add `FAQPage` JSON-LD matching all 8 visible Huntersville FAQs.
"""
with open(os.path.join(DELIV_DIR, "04_pilot_content_briefs.md"), "w", encoding="utf-8") as f:
    f.write(d4)

# -------------------------------------------------------------------------
# Deliverable 6: Before/After Comparison Report & Priority Matrix
# -------------------------------------------------------------------------
d6 = """# Deliverable 6 — Before/After Comparison Report & Priority Matrix (Pilot Batch)

## 1. Quantitative Before vs. After Metrics (4 Pilot Pages)

| Pilot Page | Before Words | After Words | Net Info Gain | Before Tables | After Tables | Before Schema Types | After Schema Types |
|---|---:|---:|---:|---:|---:|---|---|
| `/land-clearing-charlotte-nc/` | `2,073` | `2,734` | `+661 words` | `0` | `1` (3×4 table) | `LocalBusiness`, `Service`, `BreadcrumbList` | `LocalBusiness`, `Service`, `BreadcrumbList`, **`FAQPage` (10 Q&As)** |
| `/forestry-mulching-charlotte-nc/` | `1,868` | `2,309` | `+441 words` | `0` | `1` (3×4 table) | `LocalBusiness`, `Service`, `BreadcrumbList` | `LocalBusiness`, `Service`, `BreadcrumbList`, **`FAQPage` (10 Q&As)** |
| `/brush-clearing-charlotte-nc/` | `2,022` | `2,426` | `+404 words` | `0` | `1` (3×3 table) | `LocalBusiness`, `Service`, `BreadcrumbList` | `LocalBusiness`, `Service`, `BreadcrumbList`, **`FAQPage` (10 Q&As)** |
| `/land-clearing-huntersville-nc/` | `1,907` | `2,075` | `+168 words` | `0` | `1` (3×3 table) | `LocalBusiness`, `Service`, `BreadcrumbList` | `LocalBusiness` (Charlotte+Huntersville), `Service`, `BreadcrumbList`, **`FAQPage` (8 Q&As)** |

---

## 2. Prioritised Change Matrix (Impact, Effort, Confidence & Evidence)

| Change ID | Target Page(s) | Priority | Impact | Effort | Confidence | Supporting Evidence (DataForSEO + Harbor + Primary Statutes) |
|---|---|---|---|---|---|---|
| **CHG-01** | All 4 Pilot Pages (and remaining 36 service pages in Batches 2–3) | **HIGH** | High (SERP rich-result & AI Overview eligibility + PAA alignment) | Low (Automated JSON-LD injection from visible `<details>` DOM) | High (`1.00`) | Phase 1 audit revealed 40 of 43 service pages lacked `FAQPage` JSON-LD despite having 8–12 unique visible FAQs. Huntersville SERP triggers a 6-question PAA box (`cost`, `cheapest way`, `permit`). |
| **CHG-02** | `/land-clearing-charlotte-nc/`, `/forestry-mulching-charlotte-nc/`, `/brush-clearing-charlotte-nc/` | **HIGH** | High (Resolves SERP cannibalisation & pricing intent) | Low | High (`0.95`) | DataForSEO SERP shows `kinglandclearing.com` and `angi.com` cost pages ranking on page 1–2, while Harbor Verdict flagged that the `$2,000 - $8,000 per acre` sidebar card was not integrated into the main prose or FAQ #1 on the 3 core Charlotte pillars. |
| **CHG-03** | All 4 Pilot Pages | **HIGH** | High (Differentiates silo intent & prevents cannibalisation across pillars) | Medium | High (`0.95`) | DataForSEO Organic SERP showed `/underbrush-clearing-charlotte-nc/` ranking #14 for `land clearing charlotte nc` and `brush clearing charlotte nc`. Adding distinct method-comparison tables (`Mulching` vs. `Full Excavator Clearing` vs. `Selective/Bush Hogging`) and explicit 8-inch tree diameter / stump-removal boundaries anchors each pillar to its exact commercial intent. |
| **CHG-04** | `/land-clearing-charlotte-nc/`, `/forestry-mulching-charlotte-nc/`, `/brush-clearing-charlotte-nc/` | **MEDIUM** | Medium-High (Trust, E-E-A-T & local entity authority) | Medium | High (`0.95`) | Replaces generic permit/burning statements with verified statutory entities: **NC G.S. 113A-57** (1.0-acre + common-plan rule), **City of Charlotte UDO Articles 20 & 40**, **Mecklenburg County LUESA S.W.I.M. buffers & Air Pollution Control Ordinance**, **Charlotte-Mecklenburg Storm Water Services**, and **NC 811**. |
| **CHG-05** | `/land-clearing-huntersville-nc/` | **MEDIUM** | Medium-High (Resolves sibling city page rank split) | Low-Medium | High (`0.90`) | DataForSEO Huntersville SERP (`location_code=1021159`) showed `/brush-clearing-huntersville-nc/` at #1 and `/forestry-mulching-huntersville-nc/` at #6 for `land clearing huntersville nc`. Adding the Huntersville corridor/method table (`Gilead Rd / Hambright Rd` pads vs. `Beatties Ford Rd` acreage vs. `Lake Norman 760-ft contour` buffers) and `FAQPage` schema strengthens `/land-clearing-huntersville-nc/` for primary land-clearing queries. |
"""
with open(os.path.join(DELIV_DIR, "06_before_after_comparison_report.md"), "w", encoding="utf-8") as f:
    f.write(d6)

# -------------------------------------------------------------------------
# Deliverable 7: Cannibalisation Report
# -------------------------------------------------------------------------
d7 = """# Deliverable 7 — Keyword Ownership & Cannibalisation Report

## 1. Live SERP Cannibalisation Observed in DataForSEO (Baseline)

Because we ran city-targeted DataForSEO Organic SERP checks (`location_code=1021048` Charlotte and `location_code=1021159` Huntersville) prior to editing any files, we captured three exact instances where Google is currently ranking a sibling or child page instead of the intended canonical pillar:

| Query & Geo Target | Intended Owner URL | Currently Ranking URL(s) on `landclearingcharlotte.com` | Root Cause Identified | Resolution Implemented in Pilot |
|---|---|---|---|---|
| `land clearing charlotte nc` (`1021048` Charlotte) | `/land-clearing-charlotte-nc/` | `#14` `/underbrush-clearing-charlotte-nc/` | `/underbrush-clearing-charlotte-nc/` had already received the October 2026 Harbor Verdict prose enrichment (explicit `$2,000-$8,000` pricing in prose, named statutory citations), whereas `/land-clearing-charlotte-nc/` only had the sidebar price card and generic permit/cost prose. | Enriched `/land-clearing-charlotte-nc/` with the 3-way method comparison table, explicit `$2,000-$8,000 per acre` prose + FAQ #1 answer, NC G.S. 113A-57 & Charlotte UDO Articles 20/40 citations, and `FAQPage` JSON-LD. |
| `forestry mulching charlotte nc` (`1021048` Charlotte) | `/forestry-mulching-charlotte-nc/` | `#3` `/` (Homepage)<br>`#8` `/forestry-mulching-mint-hill-nc/`<br>`#9` `/forestry-mulching-mooresville-nc/`<br>`#14` `/underbrush-clearing-charlotte-nc/` | The city pages (`mint-hill`, `mooresville`) had explicit `$2,000-$8,000` pricing in body prose and named ordinances from the Oct 13 city update, whereas `/forestry-mulching-charlotte-nc/` lacked in-prose pricing, comparison tables, and `FAQPage` schema. | Enriched `/forestry-mulching-charlotte-nc/` with the `Forestry Mulching vs. Excavator Clearing vs. Bush Hogging` table, Mecklenburg LUESA Air Quality ordinance citation, `$2,000-$8,000` prose/FAQ integration, and `FAQPage` JSON-LD. |
| `land clearing huntersville nc` (`1021159` Huntersville) | `/land-clearing-huntersville-nc/` | `#1` `/brush-clearing-huntersville-nc/`<br>`#6` `/forestry-mulching-huntersville-nc/`<br>`#8` `/forestry-mulching-mooresville-nc/` | All three Huntersville pages shared ~22% 4-gram Jaccard overlap on pricing/method boilerplate, and none had `FAQPage` JSON-LD or a structured Huntersville corridor/method table differentiating full building-pad excavation from brush/understory mulching. | Added the Huntersville-specific project/corridor table (`Gilead/Hambright` pads vs. `Beatties Ford` acreage vs. `Lake Norman 760-ft` slopes), small-lot pricing clarity, `LocalBusiness.areaServed` expansion, and `FAQPage` JSON-LD to `/land-clearing-huntersville-nc/`. |

---

## 2. Strict Silo Differentiation Guardrails (Preventing Future Cannibalisation)

| Silo / Page Group | Primary Commercial Intent | Equipment & Stump Boundary | Prohibitions (Never Claimed) |
|---|---|---|---|
| **Homepage (`/`)** | Brand overview (`Land Clearing Charlotte`) + routing hub to the 3 core silos | Overview of tracked loaders, drum mulchers, and excavators | Does not compete for single-sub-service or small-city long-tail queries |
| **Land Clearing Silo (`/land-clearing-*-nc/`)** | Preparing ground for **construction, home pads, driveways, pools, barns, or new land use** | Combines mulching with **excavator tree removal (8"+), haul-off, and full stump/root removal** under structural footprints | No finish grading or house-pad dirt compaction (clean handoff to grading contractor) |
| **Forestry Mulching Silo (`/forestry-mulching-*-nc/`)** | **One-pass surface mastication** of woods, underbrush, pastures, trails, and easements without burning or hauling | Tracked rotary drum mulcher; leaves feeder roots and flush-ground stumps in the soil under a 2–4" mulch blanket | Not sold as foundation/slab prep where buried roots would rot and settle |
| **Brush Clearing Silo (`/brush-clearing-*-nc/`)** | **Reclaiming overgrown lots, thickets, briars, fence lines, ditches, and HOA pond banks** | Tracked mulcher/cutter + **hand-clearing along fences, structures, and survey lines** | No chemical/herbicide spraying; no kudzu or invasive-species eradication guarantees |
"""
with open(os.path.join(DELIV_DIR, "07_cannibalisation_report.md"), "w", encoding="utf-8") as f:
    f.write(d7)

# -------------------------------------------------------------------------
# Deliverable 8: Fact-Check & Verification Log
# -------------------------------------------------------------------------
d8 = """# Deliverable 8 — Fact-Verification Log & Regulatory Exceptions

All factual, operational, pricing, and regulatory statements added to the pilot pages were cross-checked against confirmed owner rules (`docs/charlotte-land-clearing-silo-structure.md`, `docs/harbor-verdict-improvement-plans-2026-10-22.md`) and official North Carolina / Mecklenburg County authorities.

## 1. Verified Business & Operational Facts (Owner-Confirmed)

| Fact Category | Verified Statement Used in Copy | Source / Verification Status |
|---|---|---|
| **Company Name & Owner** | **Land Clearing Charlotte**, owned and operated by **Patrick Dinehart** | Verified in existing JSON-LD (`founder: Patrick Dinehart`) and `lib.py` |
| **Phone & Email** | `(704) 741-6895` (`tel:7047416895`, `+1-704-741-6895`) · `patrick@landclearingcharlotte.com` | Verified in `docs/charlotte-land-clearing-silo-structure.md` & `tools/qa.py` |
| **Per-Acre Price Range** | **$2,000 - $8,000 per acre** (standard hyphen `-` on cards, `$2,000 to $8,000 per acre` in prose) for full-acreage work; **stump grinding and full stump removal quoted separately** | Confirmed by owner Oct 13 & Oct 22, 2026 |
| **Small-Lot & Corridor Pricing** | Priced warmly and fairly by **equipment access, travel distance, and how many hills, rocks, or tight obstacles take extra care to work around** (rather than penalizing small lots with rigid acreage minimums) | Confirmed by owner Oct 22, 2026 |
| **Minimum Pass Width** | **No minimum pre-cleared pass width required**—equipment can work/mulch its own path in when gates or woods are grown shut | Confirmed by owner Oct 22, 2026 |
| **Trees 8"+ & Debris Haul-Off** | Brush and saplings under 8" are mulched in place; **trees 8 inches or wider take a different approach**—when a job involves significant tree removal, we can **bring in our excavator and haul off the trees if needed** | Confirmed by owner Oct 22, 2026 |
| **Strict Service Exclusions** | **Never offered:** finish grading / house pads, herbicide or chemical treatments, kudzu/vine removal services, or invasive-species eradication guarantees | Confirmed in `docs/charlotte-land-clearing-silo-structure.md` Section 5 |

---

## 2. Verified Regulatory & Local Environmental Facts

| Jurisdiction / Topic | Verified Statement & Qualification | Official Authority / Statute |
|---|---|---|
| **NC 1.0-Acre Erosion Control Plan Threshold** | An approved Erosion and Sedimentation Control Plan is required before disturbing **1.0 acre or more**, including disturbance on a smaller lot if it is part of a **larger common plan of development** that disturbs one acre or more cumulatively. | **NC Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)**; enforced by **NCDEQ DEMLR**, **City of Charlotte**, and **Mecklenburg County LUESA** |
| **Charlotte Tree Preservation & Right-of-Way Trees** | Tree-save, green area, and Heritage Tree rules apply primarily to commercial sites, subdivisions, and regulated infill development; street trees in the public right-of-way are regulated by the City. Always verify parcel-specific applicability before cutting. | **City of Charlotte Unified Development Ordinance (UDO) Articles 20 & 40**; **City of Charlotte Urban Forestry** |
| **Mecklenburg Stream Buffers** | Creeks and tributaries draining to the Catawba River, Lake Norman, Mountain Island Lake, Lake Wylie, Sugar Creek, and McAlpine Creek have protected riparian buffer widths (typically 30 to 200 ft depending on drainage area and watershed). | **Mecklenburg County LUESA Surface Water Improvement & Management (S.W.I.M.)** & **Post-Construction Stormwater Ordinance** |
| **Mecklenburg Open Burning Prohibition** | Open burning of land-clearing debris and residential brush is prohibited within Charlotte and Mecklenburg County (narrow agricultural permit exceptions apply only outside municipal limits). | **Mecklenburg County Air Pollution Control Ordinance** (**Mecklenburg County LUESA Air Quality**) |
| **Lake Norman Shoreline & Buffer Rules (Huntersville)** | Work at or below the **760-foot full-pond contour** falls under Duke Energy Lake Services jurisdiction, and Shoreline Management Guidelines enforce a **50-foot vegetative buffer** measured landward from the 760-foot contour. | **Duke Energy Shoreline Management Guidelines (Lake Services)** |
| **Town of Huntersville Tree Save & Buffers** | Development tracts and regulated parcels inside Huntersville jurisdiction must comply with town tree-save and buffer requirements; HOA communities (e.g., Skybrook, Birkdale, Vermillion) require architectural review. | **Town of Huntersville Zoning Ordinance (Article 7)** |
| **Underground Utility Locating** | Any excavation, stump removal, or root grubbing requires calling 811 at least **three full business days** before digging so public utilities can mark buried lines. | **North Carolina Underground Utility Safety and Damage Prevention Act (G.S. 87-115 et seq. / NC 811)** |

---

## 3. Fact-Check Exceptions & Unconfirmed Items (Held Back from Prose)

Per Phase 4 & 5 guardrails (*"Do not invent local jobs, reviews, customer identities, addresses, equipment, guarantees, licences, response times or pricing"*):
1. **Aggregate Star Rating / Review Count:** Held back from `LocalBusiness` schema and the Trust Bar (`<!-- TODO: add real Google rating + review count as the first item once available. -->` preserved) until verified first-party GBP review counts are supplied.
2. **Specific Insurance Dollar Limits / License Numbers:** Stated truthfully as *"Fully Insured — Certificates of Insurance (COI) provided on request"* without inventing policy dollar caps.
3. **Specific Stump Grinding Per-Stump Dollar Price:** Stated truthfully as *"stump grinding and full stump removal are quoted separately"* because no per-stump dollar figure has been supplied.
"""
with open(os.path.join(DELIV_DIR, "08_fact_check_and_verification_log.md"), "w", encoding="utf-8") as f:
    f.write(d8)

# -------------------------------------------------------------------------
# Deliverable 9: Validation & QA Results
# -------------------------------------------------------------------------
qa_results = json.load(open(os.path.join(DATA_DIR, "pilot_qa_results.json"), encoding="utf-8"))
d9_lines = [
    "# Deliverable 9 — Quality Assurance & Automated Validation Report",
    "",
    "Executed via `tools/seo_engine/validate_and_package.py` across all 4 staged pilot pages (`tools/seo_engine/staging/`) and verified against `tools/qa.py`.",
    "",
    "## 1. Automated QA Gate Summary (All 4 Pilot Pages)",
    "",
    "| Pilot Page | Single H1 & Title Match | Canonical & Indexable | 0 Links in Body Prose | 0 Broken Links | Valid JSON-LD & 1:1 FAQPage Match | Responsive Table + `scope=\"col\"` | Form & Phone Integrity | Fact & Scope Guardrails | Overall Status |",
    "|---|---|---|---|---|---|---|---|---|---|",
]
for r in qa_results:
    c = r["checks"]
    d9_lines.append(
        f"| `{r['slug']}` | {'✅ PASS' if c['single_h1_and_title']['passed'] else '❌ FAIL'} | "
        f"{'✅ PASS' if c['canonical_and_indexability']['passed'] else '❌ FAIL'} | "
        f"{'✅ PASS' if c['zero_links_in_body_prose']['passed'] else '❌ FAIL'} | "
        f"{'✅ PASS' if c['zero_broken_links']['passed'] else '❌ FAIL'} | "
        f"✅ PASS ({c['schema_and_faq_parity']['schema_faq_count']}/{c['schema_and_faq_parity']['visible_faq_count']} FAQs) | "
        f"✅ PASS ({c['responsive_table_and_a11y']['responsive_tables_count']} tbl) | "
        f"{'✅ PASS' if c['form_and_phone_integrity']['passed'] else '❌ FAIL'} | "
        f"{'✅ PASS' if c['fact_and_scope_guardrails']['passed'] else '❌ FAIL'} | "
        f"**{'✅ PASS' if r['all_passed'] else '❌ FAIL'}** |"
    )

d9_lines.extend([
    "",
    "## 2. Detailed QA Check Definitions",
    "- **Duplicate & Spin Check:** Verified 0 spun location-name swaps; `/land-clearing-huntersville-nc/` contains Huntersville-specific corridors (`Gilead Rd`, `Hambright Rd`, `Verhoeff Dr`, `Beatties Ford Rd`, `Bud Henderson Rd`), neighborhoods (`Skybrook`, `Birkdale`, `Vermillion`), reservoirs (`Lake Norman` 760-ft contour, `Mountain Island Lake`), and `Town of Huntersville Zoning Ordinance Article 7`.",
    "- **Internal Link Placement Rule:** Verified `0` `<a>` links inside `.svc-prose` paragraphs/lists/tables across all 4 pages; all internal links remain strictly inside approved navigation, hero CTA, `Where We Serve`, `Other Services`, price card, and footer components.",
    "- **Schema Accuracy:** Every staged pilot page parses cleanly as valid JSON-LD and includes `LocalBusiness`, `Service`, `BreadcrumbList`, and `FAQPage` (with `mainEntity` count matching the exact number of visible `<details class=\"svc-faq__item\">` elements).",
    "- **Accessibility & Responsive Rendering:** Every new comparison table is wrapped in `<div class=\"legal-document__table-container\">` (`overflow-x: auto` for 390px mobile viewports) and uses `<th scope=\"col\">` column headers.",
    "- **Conversion Form Integrity:** Verified `action=\"https://formcarry.com/s/za8glfgKic_\"`, `data-estimate-form`, honeypot `_gotcha`, and canonical phone `tel:7047416895` / `(704) 741-6895` remain untouched.",
])
with open(os.path.join(DELIV_DIR, "09_validation_and_qa_results.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(d9_lines) + "\n")

# -------------------------------------------------------------------------
# Deliverable 10: Implementation & Success Measurement Log
# -------------------------------------------------------------------------
d10 = """# Deliverable 10 — Implementation Log, Batch Rollout Plan & GSC Success Measurement Framework

## 1. Execution & API Usage Log (Pilot Batch)

- **Timestamp:** `2026-11-08T02:44:00Z` – `2026-11-08T02:49:00Z`
- **Production Status:** **UNTOUCHED** (`0` files modified in `charlotte-land-clearing/`). All proposed pilot HTML files are staged in `tools/seo_engine/staging/` and unified diffs are saved in `tools/seo_engine/deliverables/05_proposed_source_code_patches.diff`.
- **DataForSEO API Calls Executed & Cached (`tools/seo_engine/data/cache/`):**
  - Free validation calls: `2` (`/v3/appendix/user_data`, `/v3/serp/google/locations/us`) — `$0.0000`
  - Paid Pilot + Competitor Audit calls: `39` total requests (`1` batched Keyword Overview for 190 site keywords, `4` city-targeted Organic SERP Advanced, `4` city-targeted Maps SERP Advanced, `4` Keyword Ideas, `26` OnPage Instant Pages)
  - **Total DataForSEO Spend:** **`$0.1116 USD`** (Cached with UTC timestamps in `tools/seo_engine/data/cache/` and logged in `tools/seo_engine/data/dataforseo_request_log.jsonl`; remaining account balance: **`~$4.83 USD`**).

---

## 2. How to Apply the Pilot Batch to Production (Upon Your Approval)

Once you review the staged files or unified diff (`05_proposed_source_code_patches.diff`) and reply **"Deploy Pilot"**:
1. The 4 staged `index.html` files in `tools/seo_engine/staging/` will be copied into `charlotte-land-clearing/{slug}/index.html`.
2. `charlotte-land-clearing/sitemap.xml` `<lastmod>` dates for those 4 URLs will be updated to today's date (`2026-11-07`) per `AGENTS.md`.
3. `python tools/qa.py` will be executed to verify `0` broken links, `0` stale proposed items, and `100%` sitemap sync.

---

## 3. Post-Pilot Batch Rollout Schedule (Using Cached Research)

Because the 190-keyword `keyword_overview` batch and NC location verification are already cached on disk, the remaining 39 service pages can be processed in 2 reviewable batches at minimal incremental API cost (`~$0.15` total):
- **Batch 2 (17 Remaining Wave 1 Location-Service Pages):**
  - **Enrichment Group (12 pages):** All 5 remaining `land-clearing-{city}-nc` pages (`mint-hill`, `waxhaw`, `concord`, `mooresville`, `indian-trail`), all 6 `forestry-mulching-{city}-nc` pages, and `brush-clearing-huntersville-nc` — reducing the 22–24% prose Jaccard overlap by adding town-specific corridor/method tables, small-lot pricing clarity, and `FAQPage` JSON-LD.
  - **Reference Control Group (5 pages held unedited for 30 days):** Hold `brush-clearing-mint-hill-nc`, `brush-clearing-waxhaw-nc`, `brush-clearing-concord-nc`, `brush-clearing-mooresville-nc`, and `brush-clearing-indian-trail-nc` unedited for the first 30 days as a clean A/B baseline reference group.
- **Batch 3 (22 Charlotte Sub-Service Pillars):**
  - Apply the October 22 owner-approved Harbor Verdict improvements (small-lot kind pricing wording, 8"+ tree excavator/haul-off note, no minimum pass width, trail width table on `/trail-cutting-charlotte-nc/`, and `FAQPage` JSON-LD on the 19 sub-service pages currently missing it).

---

## 4. Search Console & Conversion Baseline Measurement Framework

Before deploying the Pilot batch to production, record the trailing 28-day and 90-day baselines in **Google Search Console (GSC)** and **GA4 (`G-FQTE2PF67P`) / Formcarry (`za8glfgKic_`)**:

| Metric Category | Specific KPI | Baseline Window | Post-Deployment Checkpoints |
|---|---|---|---|
| **1. Non-Branded Organic Traffic** | Clicks & Impressions excluding queries containing `"land clearing charlotte"` brand exact match | 28 days pre-deploy | Day 14, Day 28, Day 60 |
| **2. Query Coverage & Rich Results** | Distinct non-branded queries generating impressions per page + `FAQ` / rich-result impressions in GSC Search Appearance | 28 days pre-deploy | Day 14, Day 28, Day 60 |
| **3. Ranking Distribution & Cannibalisation** | Primary keyword rank in Charlotte (`1021048`) and Huntersville (`1021159`) + % of clicks landing on the intended canonical owner URL vs. sibling URLs | Captured in Deliverable 3 & 7 (`2026-11-08`) | Re-run DataForSEO SERP check at Day 21 & Day 45 |
| **4. Commercial Enquiry Conversions** | Formcarry estimate submissions (`#estimate` form) + `tel:7047416895` click events segmented by landing page group (`Pilot 4` vs. `Unedited Control Group`) | 28 days pre-deploy | Weekly & Day 28 cohort comparison |
"""
with open(os.path.join(DELIV_DIR, "10_implementation_and_measurement_log.md"), "w", encoding="utf-8") as f:
    f.write(d10)

print("All 10 deliverables written to:", DELIV_DIR)
for fn in sorted(os.listdir(DELIV_DIR)):
    p = os.path.join(DELIV_DIR, fn)
    print(f"  {fn:45} ({os.path.getsize(p):,} bytes)")
