"""Phase 2 & 3 — Execute Pilot Batch DataForSEO Collection & Competitor Analysis.

Collects and caches:
1. Google Organic SERP Advanced (city-level location_code) for the 4 pilot pages:
   - /land-clearing-charlotte-nc/ (location_code=1021048, Charlotte, NC)
   - /forestry-mulching-charlotte-nc/ (location_code=1021048, Charlotte, NC)
   - /brush-clearing-charlotte-nc/ (location_code=1021048, Charlotte, NC)
   - /land-clearing-huntersville-nc/ (location_code=1021159, Huntersville, NC)
2. Google Maps SERP Advanced (city-level location_code) for the 4 pilot pages.
3. DataForSEO Labs Keyword Overview (batched keywords across all site services/cities).
4. DataForSEO Labs Keyword Ideas for the 4 pilot clusters.
5. OnPage Instant Pages for our 4 live pilot URLs + top local organic competitors per SERP.
"""
import os
import json
from urllib.parse import urlparse
from dataforseo_client import DataForSEOClient, DATA_DIR

PILOT_PAGES = [
    {
        "slug": "/land-clearing-charlotte-nc/",
        "url": "https://landclearingcharlotte.com/land-clearing-charlotte-nc/",
        "primary_keyword": "land clearing charlotte nc",
        "location_code": 1021048,
        "location_name": "Charlotte,North Carolina,United States",
        "seed_keywords": [
            "land clearing charlotte nc",
            "lot clearing charlotte nc",
            "land clearing cost charlotte nc",
            "acreage clearing charlotte nc",
            "commercial land clearing charlotte nc",
        ],
    },
    {
        "slug": "/forestry-mulching-charlotte-nc/",
        "url": "https://landclearingcharlotte.com/forestry-mulching-charlotte-nc/",
        "primary_keyword": "forestry mulching charlotte nc",
        "location_code": 1021048,
        "location_name": "Charlotte,North Carolina,United States",
        "seed_keywords": [
            "forestry mulching charlotte nc",
            "forestry mulching near me",
            "forestry mulching cost per acre nc",
            "underbrush clearing charlotte nc",
            "brush mulching charlotte nc",
        ],
    },
    {
        "slug": "/brush-clearing-charlotte-nc/",
        "url": "https://landclearingcharlotte.com/brush-clearing-charlotte-nc/",
        "primary_keyword": "brush clearing charlotte nc",
        "location_code": 1021048,
        "location_name": "Charlotte,North Carolina,United States",
        "seed_keywords": [
            "brush clearing charlotte nc",
            "brush removal charlotte nc",
            "overgrown lot cleanup charlotte nc",
            "briar clearing charlotte nc",
            "fence line clearing charlotte nc",
        ],
    },
    {
        "slug": "/land-clearing-huntersville-nc/",
        "url": "https://landclearingcharlotte.com/land-clearing-huntersville-nc/",
        "primary_keyword": "land clearing huntersville nc",
        "location_code": 1021159,
        "location_name": "Huntersville,North Carolina,United States",
        "seed_keywords": [
            "land clearing huntersville nc",
            "forestry mulching huntersville nc",
            "brush clearing huntersville nc",
            "lot clearing huntersville nc",
            "land clearing lake norman nc",
        ],
    },
]

DIRECTORY_DOMAINS = {
    "angi.com",
    "homeadvisor.com",
    "thumbtack.com",
    "yelp.com",
    "bbb.org",
    "houzz.com",
    "bark.com",
    "manta.com",
    "yellowpages.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "reddit.com",
    "nextdoor.com",
    "networx.com",
    "porch.com",
    "buildzoom.com",
    "expertise.com",
}


def is_directory(url: str) -> bool:
    host = urlparse(url).netloc.lower().lstrip("www.")
    return any(host == d or host.endswith("." + d) for d in DIRECTORY_DOMAINS)


def main():
    # Hard budget limit of $0.75 USD for Pilot Batch safety
    client = DataForSEOClient(budget_limit_usd=0.75, dry_run=False)

    dry_plan = json.load(open(os.path.join(DATA_DIR, "dry_run_plan.json"), encoding="utf-8"))
    all_site_kws = set()
    for p in dry_plan["page_keyword_map"]:
        all_site_kws.add(p["primary_keyword"])
        for sk in p["secondary_keywords"]:
            all_site_kws.add(sk)
    for pp in PILOT_PAGES:
        for sk in pp["seed_keywords"]:
            all_site_kws.add(sk)

    all_site_kws_list = sorted(all_site_kws)[:700]
    print(f"1. Running Keyword Overview batch for {len(all_site_kws_list)} site keywords...")
    kw_overview_resp = client.request(
        "/v3/dataforseo_labs/google/keyword_overview/live",
        [
            {
                "keywords": all_site_kws_list,
                "location_code": 2840,
                "language_code": "en",
                "include_serp_info": False,
                "include_clickstream_data": False,
            }
        ],
    )

    pilot_results = {}
    competitor_urls_to_audit = []

    for pp in PILOT_PAGES:
        slug = pp["slug"]
        kw = pp["primary_keyword"]
        loc_code = pp["location_code"]
        print(f"2. Fetching Organic SERP, Maps SERP, and Keyword Ideas for {slug} ({kw} @ {loc_code})...")

        org_resp = client.request(
            "/v3/serp/google/organic/live/advanced",
            [
                {
                    "keyword": kw,
                    "location_code": loc_code,
                    "language_code": "en",
                    "device": "desktop",
                    "os": "windows",
                    "depth": 20,
                    "people_also_ask_click_depth": 1,
                }
            ],
        )

        maps_resp = client.request(
            "/v3/serp/google/maps/live/advanced",
            [
                {
                    "keyword": kw,
                    "location_code": loc_code,
                    "language_code": "en",
                    "device": "desktop",
                    "depth": 10,
                }
            ],
        )

        ideas_resp = client.request(
            "/v3/dataforseo_labs/google/keyword_ideas/live",
            [
                {
                    "keywords": pp["seed_keywords"],
                    "location_code": 2840,
                    "language_code": "en",
                    "closely_variants": True,
                    "limit": 50,
                }
            ],
        )

        # Extract top 3 non-directory local competitor URLs from organic SERP
        items = (org_resp.get("tasks", [{}])[0].get("result") or [{}])[0].get("items") or []
        org_items = [it for it in items if it.get("type") == "organic" and it.get("url")]
        local_comp_urls = []
        for it in org_items:
            u = it["url"]
            if "landclearingcharlotte.com" in u:
                continue
            if not is_directory(u) and u not in local_comp_urls:
                local_comp_urls.append(u)
            if len(local_comp_urls) >= 3:
                break

        for u in [pp["url"]] + local_comp_urls:
            if u not in competitor_urls_to_audit:
                competitor_urls_to_audit.append(u)

        pilot_results[slug] = {
            "meta": pp,
            "organic_serp": org_resp,
            "maps_serp": maps_resp,
            "keyword_ideas": ideas_resp,
            "selected_competitor_urls": local_comp_urls,
        }

    print(f"3. Running OnPage Instant Pages for {len(competitor_urls_to_audit)} URLs (4 pilot + local competitors)...")
    onpage_results = {}
    for u in competitor_urls_to_audit:
        try:
            op_resp = client.request(
                "/v3/on_page/instant_pages",
                [
                    {
                        "url": u,
                        "enable_javascript": False,
                        "load_resources": False,
                    }
                ],
            )
            onpage_results[u] = op_resp
        except Exception as e:
            onpage_results[u] = {"error": str(e)}

    # Save structured summary for Phase 3 analysis
    summary_out = {
        "total_requests_made": client.request_count,
        "total_cost_usd": round(client.spent_usd, 5),
        "audited_urls_count": len(competitor_urls_to_audit),
        "audited_urls": competitor_urls_to_audit,
    }
    print("Pilot DataForSEO collection finished:", json.dumps(summary_out, indent=2))

    with open(os.path.join(DATA_DIR, "pilot_raw_bundle.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "collection_summary": summary_out,
                "keyword_overview": kw_overview_resp,
                "pilot_pages": pilot_results,
                "onpage_instant": onpage_results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    main()
