import os
import json
import datetime
from dataforseo_client import DataForSEOClient, DATA_DIR

CITY_CODES = {
    "huntersville-nc": (1021159, "Huntersville,North Carolina,United States"),
    "mint-hill-nc": (9052451, "Mint Hill,North Carolina,United States"),
    "waxhaw-nc": (1021357, "Waxhaw,North Carolina,United States"),
    "concord-nc": (1021064, "Concord,North Carolina,United States"),
    "mooresville-nc": (1021222, "Mooresville,North Carolina,United States"),
    "indian-trail-nc": (1021160, "Indian Trail,North Carolina,United States"),
}

SILOS = ["land-clearing", "forestry-mulching", "brush-clearing"]

def main():
    client = DataForSEOClient(budget_limit_usd=0.35, dry_run=False)
    bundle = {
        "collected_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pages": {}
    }

    for silo in SILOS:
        silo_kw = silo.replace("-", " ")
        for city_slug, (loc_code, loc_name) in CITY_CODES.items():
            page_slug = f"{silo}-{city_slug}"
            if page_slug == "land-clearing-huntersville-nc":
                continue
            city_pretty = city_slug.replace("-nc", "").replace("-", " ")
            kw = f"{silo_kw} {city_pretty} nc"
            print(f"Collecting SERPs for /{page_slug}/ -> '{kw}' (loc={loc_code})...")
            org = client.request(
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
            maps = client.request(
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

            org_items = []
            paa_items = []
            related_items = []
            our_rank = None

            tasks = org.get("tasks") or []
            if tasks and tasks[0].get("result"):
                res0 = tasks[0]["result"][0] or {}
                for it in (res0.get("items") or []):
                    t = it.get("type")
                    if t == "organic":
                        domain = it.get("domain") or ""
                        url = it.get("url") or ""
                        bc = it.get("breadcrumb") or ""
                        rank_group = it.get("rank_group")
                        org_items.append({
                            "rank_group": rank_group,
                            "rank_absolute": it.get("rank_absolute"),
                            "domain": domain,
                            "title": it.get("title"),
                            "description": it.get("description"),
                            "url": url,
                            "breadcrumb": bc,
                            "website_name": it.get("website_name")
                        })
                        if "landclearingcharlotte.com" in (domain + url + bc).lower():
                            our_rank = rank_group
                    elif t == "people_also_ask":
                        for el in (it.get("items") or []):
                            if el.get("title"):
                                paa_items.append(el.get("title"))
                    elif t == "related_searches":
                        for el in (it.get("items") or []):
                            if isinstance(el, str):
                                related_items.append(el)
                            elif isinstance(el, dict) and el.get("title"):
                                related_items.append(el.get("title"))

            maps_items = []
            mtasks = maps.get("tasks") or []
            if mtasks and mtasks[0].get("result"):
                mres0 = mtasks[0]["result"][0] or {}
                for it in (mres0.get("items") or []):
                    if it.get("type") == "maps_search":
                        maps_items.append({
                            "rank_group": it.get("rank_group"),
                            "title": it.get("title"),
                            "domain": it.get("domain"),
                            "url": it.get("url"),
                            "rating": (it.get("rating") or {}).get("value"),
                            "reviews_count": (it.get("rating") or {}).get("votes_count"),
                            "category": it.get("category"),
                            "address": it.get("address")
                        })

            bundle["pages"][page_slug] = {
                "slug": f"/{page_slug}/",
                "keyword": kw,
                "location_code": loc_code,
                "location_name": loc_name,
                "our_organic_rank": our_rank,
                "organic_top10": org_items[:10],
                "paa_questions": paa_items,
                "related_searches": related_items,
                "maps_top5": maps_items[:5]
            }

    bundle["session_spend_usd"] = round(client.session_spend_usd, 4) if hasattr(client, "session_spend_usd") else 0.0
    out_path = os.path.join(DATA_DIR, "city_batch_raw_bundle.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
    print(f"Saved {len(bundle['pages'])} Wave 1 city page SERP packs to {out_path}.")

if __name__ == "__main__":
    main()
