"""Generate a markdown report of the Master URL Inventory & Dry-Run Plan."""
import os
import json

DATA_DIR = r"h:\Websites\landc\tools\seo_engine\data"
ART_DIR = r"C:\Users\Patrick\.gemini\antigravity\brain\84bd50e0-6aa0-4ce6-96b1-94c868d14018"

inv_data = json.load(open(os.path.join(DATA_DIR, "master_url_inventory.json"), encoding="utf-8"))
plan_data = json.load(open(os.path.join(DATA_DIR, "dry_run_plan.json"), encoding="utf-8"))

pages = inv_data["pages"]
summary = inv_data["summary"]
kw_map = {p["slug"]: p for p in plan_data["page_keyword_map"]}

lines = [
    "# Phase 1 & 2 — Master URL Inventory, Technical Audit & DataForSEO Dry-Run Plan",
    "",
    "> [!IMPORTANT]",
    "> **No paid API calls or production edits have been executed.**",
    "> DataForSEO credentials (`DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` or `DATAFORSEO_BASIC_AUTH`) are currently not set in the environment or `h:\\Websites\\landc\\.env`. Review the dry-run plan and expected request count below before authorizing live API queries.",
    "",
    "---",
    "",
    "## 1. Phase 1 — Website Inventory & Technical Audit Summary",
    "",
    f"- **Total Local HTML Pages Discovered (`index.html`):** `{summary['total_local_html_pages']}` (plus `404.html` error template)",
    f"- **Total Sitemap URLs (`sitemap.xml`):** `{summary['total_sitemap_urls']}` (exact 1:1 match with all 50 non-legal pages)",
    "- **Excluded Legal/Utility Pages (intentionally omitted from `sitemap.xml` per `AGENTS.md`):** `/privacy-policy/`, `/cookies-policy/`, `/terms-and-conditions/`",
    "- **Page Classification Breakdown:**",
    "  - **Homepage (`1`):** `/`",
    "  - **Core Service Pillars (`3`):** `/land-clearing-charlotte-nc/`, `/forestry-mulching-charlotte-nc/`, `/brush-clearing-charlotte-nc/`",
    "  - **Location-Service Pages (`18`):** 3 core services × 6 Wave 1 towns (`huntersville-nc`, `mint-hill-nc`, `waxhaw-nc`, `concord-nc`, `mooresville-nc`, `indian-trail-nc`)",
    "  - **Specialised Sub-Service Pillars (`22`):** 8 Land Clearing + 8 Forestry Mulching + 6 Brush Clearing Charlotte pages",
    "  - **Informational Pages (`5`):** `/land-clearing-cost-calculator/`, `/lot-clearing-tips/` hub + 3 NC guide articles",
    "  - **Utility & Conversion Pages (`4`):** `/free-estimate/` (indexed, in sitemap) + 3 legal pages",
    "",
    "### Technical & Content Overlap Findings",
    "- **Broken Internal Links:** `0` across all 53 pages (`132` future Wave 1 sub-service child pages are properly rendered as unlinked `data-href` cards).",
    "- **Titles, Meta Descriptions & H1s:** `100%` unique (`0` duplicates, `0` missing, `1` H1 per page, `100%` exact canonical tag alignment).",
    "- **Structured Data (JSON-LD) Gap:** All 43 service & location-service pages have valid `LocalBusiness`, `Service`, and `BreadcrumbList` schema, and visible FAQ sections (8–12 Q&As), **but `FAQPage` JSON-LD is missing on 40 of the 43 service pages** (currently present only on `/acreage-clearing-charlotte-nc/`, `/driveway-clearing-charlotte-nc/`, and `/lot-clearing-charlotte-nc/`). Notice also on location-service pages like `/land-clearing-huntersville-nc/`, the `Service` node sets `areaServed: Huntersville`, while the embedded `LocalBusiness` node still only lists `Charlotte` in `areaServed`.",
    "- **Prose Overlap Analysis (4-gram Jaccard Similarity excluding nav/footer/cards):**",
    "  - Highest prose similarity occurs among the 18 Wave 1 location-service pages (`0.216`–`0.248` 4-gram Jaccard overlap across `brush-clearing-{city}-nc` and `forestry-mulching-{city}-nc` siblings), caused by shared pricing-factor and method-comparison boilerplate blocks in `tools/gen/content_cities.py`. Phase 4 & 5 enrichment will replace shared boilerplate with genuinely distinct town-level terrain, watershed, ordinance, and parcel-type specifics.",
    "",
    "---",
    "",
    "## 2. Phase 2 — DataForSEO Architecture & Geographic Targeting Rules",
    "",
    "The integration module (`tools/seo_engine/dataforseo_client.py`) implements:",
    "1. **Environment-Variable Auth:** Reads `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` (or `DATAFORSEO_BASIC_AUTH`) from OS environment variables or `h:\\Websites\\landc\\.env`.",
    "2. **Strict City-Level Geo-Targeting (No Silent US-Wide Substitution):**",
    "   - **Google Organic SERP Advanced (`/v3/serp/google/organic/live/advanced`)** and **Google Maps SERP Advanced (`/v3/serp/google/maps/live/advanced`)** use exact city-level `location_name` targeting (`Charlotte,North Carolina,United States`, `Huntersville,North Carolina,United States`, `Mint Hill,North Carolina,United States`, `Waxhaw,North Carolina,United States`, `Concord,North Carolina,United States`, `Mooresville,North Carolina,United States`, `Indian Trail,North Carolina,United States`) plus exact GPS `location_coordinate` (`lat,lng,13z`) for Maps.",
    "   - First step in live execution queries the free `/v3/serp/google/locations/us` endpoint to verify exact `location_code` IDs for all 7 towns; if any smaller town (e.g., Mint Hill or Waxhaw) is not a standalone criteria ID in Google's geo table, the client logs an explicit exception in the fact-verification log and pairs the closest county-seat criteria (`Charlotte` or `Monroe, NC`) with exact town GPS coordinates (`location_coordinate`).",
    "   - **Documented DataForSEO Labs Limitation:** DataForSEO Labs endpoints (`keyword_overview/live` and `keyword_ideas/live`) architecturally support only country-level `location_code=2840` (United States). We never treat US volume on bare terms as local volume; instead, Labs queries use explicit city+state modified seeds (`{service} {city} nc`) while SERP endpoints enforce strict city-level geo-targeting.",
    "3. **Caching, Logging & Budget Guardrails:**",
    "   - Raw JSON responses are stored with UTC `collected_at` timestamps in `tools/seo_engine/data/cache/` keyed by SHA-256 of `(endpoint, payload)`.",
    "   - Every live call is logged to `tools/seo_engine/data/dataforseo_request_log.jsonl` with cost tracking and a hard `budget_limit_usd` circuit breaker.",
    "",
    "---",
    "",
    "## 3. Proposed Pilot Batch & Expected DataForSEO API Usage",
    "",
    "### Pilot Scope (4 Pages: 3 Core Service Pillars + 1 Location-Service Page)",
    "1. **Core Pillar 1:** `/land-clearing-charlotte-nc/` (`land clearing charlotte nc`)",
    "2. **Core Pillar 2:** `/forestry-mulching-charlotte-nc/` (`forestry mulching charlotte nc`)",
    "3. **Core Pillar 3:** `/brush-clearing-charlotte-nc/` (`brush clearing charlotte nc`)",
    "4. **Location-Service Pilot:** `/land-clearing-huntersville-nc/` (`land clearing huntersville nc` — tests Lake Norman / Duke Energy 760-ft contour, Town of Huntersville Article 7, and Mecklenburg LUESA local entity enrichment)",
    "",
    "### Expected API Request Count & Cost Estimate",
    "",
    "| Endpoint | Pilot Batch (4 Pages) Requests | Pilot Est. Cost (USD) | Full Site (All 43 Service Pages) Requests | Full Site Est. Cost (USD) | Purpose |",
    "|---|---:|---:|---:|---:|---|",
    "| `/v3/serp/google/locations/us` | `1` | `$0.000` | `1` | `$0.000` | Verify exact NC city `location_code` IDs (free endpoint) |",
    "| `/v3/serp/google/organic/live/advanced` | `4` | `$0.008` | `43` | `$0.086` | City-targeted Organic SERP top 20, PAA & related searches |",
    "| `/v3/serp/google/maps/live/advanced` | `4` | `$0.008` | `21` | `$0.042` | City-targeted Local Pack competitors, GBP categories & reviews |",
    "| `/v3/dataforseo_labs/google/keyword_overview/live` | `1` | `$0.011` | `1` | `$0.011` | Batched volume, CPC, intent & difficulty for ~200 site keywords |",
    "| `/v3/dataforseo_labs/google/keyword_ideas/live` | `4` | `$0.044` | `10` | `$0.110` | Service + local modifier keyword discovery per silo cluster |",
    "| `/v3/on_page/instant_pages` | `16` | `$0.020` | `120` | `$0.150` | Live OnPage extraction of our pages + top 3 competitors per SERP |",
    "| **TOTAL** | **`30` requests** | **`~$0.091`** | **`196` requests** | **`~$0.399`** | Cached deterministically on disk |",
    "",
    "---",
    "",
    "## 4. Complete 53-Page Master URL Inventory & Keyword Map",
    "",
    "| # | Slug | Classification | Sitemap | Words (Total / Prose) | H1 | H2 / H3 | Schema Types | Primary Target Keyword | Batch |",
    "|---:|---|---|---|---|---|---:|---|---|---|",
]

for idx, p in enumerate(pages, 1):
    slug = p["slug"]
    km = kw_map.get(slug, {})
    pk = km.get("primary_keyword", "— (utility/noindex)")
    batch = km.get("batch", "Excluded (Utility)")
    sm_str = f"✅ ({p['sitemap_priority']})" if p["in_sitemap"] else "❌ (Excluded)"
    sch_str = ", ".join(p["schema_types"]) if p["schema_types"] else "None"
    lines.append(
        f"| {idx} | `{slug}` | `{p['page_type']}` | {sm_str} | {p['main_word_count']} / {p['prose_word_count']} | {p['h1']} | {p['h2_count']} / {p['h3_count']} | {sch_str} | `{pk}` | {batch} |"
    )

content = "\n".join(lines) + "\n"
with open(os.path.join(DATA_DIR, "phase1_2_inventory_and_dry_run_report.md"), "w", encoding="utf-8") as f:
    f.write(content)

print("Report generated successfully:", len(lines), "lines")
