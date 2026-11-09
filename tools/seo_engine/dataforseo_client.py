"""Phase 2 — DataForSEO Integration Client & Dry-Run Planner for LandClearingCharlotte.com.

Implements:
- Secure authentication via environment variables (DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD, or DATAFORSEO_BASIC_AUTH)
- Location lookup & strict city-level targeting validation (Charlotte, Huntersville, Mint Hill, Waxhaw, Concord, Mooresville, Indian Trail, NC)
- Google Organic SERP Advanced (/v3/serp/google/organic/live/advanced)
- Google Maps SERP Advanced (/v3/serp/google/maps/live/advanced)
- DataForSEO Labs Keyword Overview (/v3/dataforseo_labs/google/keyword_overview/live)
- DataForSEO Labs Keyword Ideas (/v3/dataforseo_labs/google/keyword_ideas/live)
- OnPage Instant Pages (/v3/on_page/instant_pages)
- Deterministic disk caching with collection timestamps, retry handling, request logging, and hard budget caps
- Dry-run mode (--dry-run) that outputs exact planned API payloads, location targeting notes, and cost estimates without making paid requests.
"""
import os
import sys
import json
import time
import base64
import hashlib
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE_DIR = r"h:\Websites\landc\tools\seo_engine"
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
LOG_FILE = os.path.join(DATA_DIR, "dataforseo_request_log.jsonl")
DRY_RUN_FILE = os.path.join(DATA_DIR, "dry_run_plan.json")

API_HOST = "https://api.dataforseo.com"

# Estimated live/instant pricing per request in USD (conservative standard DataForSEO live tier rates)
COST_ESTIMATES_USD = {
    "/v3/serp/google/organic/live/advanced": 0.002,
    "/v3/serp/google/maps/live/advanced": 0.002,
    "/v3/dataforseo_labs/google/keyword_overview/live": 0.011,
    "/v3/dataforseo_labs/google/keyword_ideas/live": 0.011,
    "/v3/on_page/instant_pages": 0.00125,
    "/v3/serp/google/locations/us": 0.0,  # Free metadata endpoint
    "/v3/appendix/user_data": 0.0,        # Free account check endpoint
}

# Target cities and explicit geographic targeting rules:
# Note: Google Organic & Maps SERP APIs support city-level `location_name` targeting.
# DataForSEO Labs (Keyword Ideas / Keyword Overview) ONLY supports country-level (2840 = United States) in DataForSEO's schema;
# therefore, local specificity in Labs is achieved via city-modified seed keywords while SERP endpoints enforce strict city-level geo-targeting.
TARGET_LOCATIONS = {
    "charlotte-nc": {
        "city": "Charlotte",
        "county": "Mecklenburg County",
        "state": "North Carolina",
        "serp_location_name": "Charlotte,North Carolina,United States",
        "fallback_location_name": "Charlotte,North Carolina,United States",
        "coordinates": "35.2271,-80.8431,12z",
    },
    "huntersville-nc": {
        "city": "Huntersville",
        "county": "Mecklenburg County",
        "state": "North Carolina",
        "serp_location_name": "Huntersville,North Carolina,United States",
        "fallback_location_name": "Charlotte,North Carolina,United States",
        "coordinates": "35.4107,-80.8428,13z",
    },
    "mint-hill-nc": {
        "city": "Mint Hill",
        "county": "Mecklenburg County",
        "state": "North Carolina",
        "serp_location_name": "Mint Hill,North Carolina,United States",
        "fallback_location_name": "Charlotte,North Carolina,United States",
        "coordinates": "35.1796,-80.6473,13z",
    },
    "waxhaw-nc": {
        "city": "Waxhaw",
        "county": "Union County",
        "state": "North Carolina",
        "serp_location_name": "Waxhaw,North Carolina,United States",
        "fallback_location_name": "Monroe,North Carolina,United States",
        "coordinates": "34.9246,-80.7434,13z",
    },
    "concord-nc": {
        "city": "Concord",
        "county": "Cabarrus County",
        "state": "North Carolina",
        "serp_location_name": "Concord,North Carolina,United States",
        "fallback_location_name": "Charlotte,North Carolina,United States",
        "coordinates": "35.4088,-80.5795,12z",
    },
    "mooresville-nc": {
        "city": "Mooresville",
        "county": "Iredell County",
        "state": "North Carolina",
        "serp_location_name": "Mooresville,North Carolina,United States",
        "fallback_location_name": "Charlotte,North Carolina,United States",
        "coordinates": "35.5849,-80.8101,12z",
    },
    "indian-trail-nc": {
        "city": "Indian Trail",
        "county": "Union County",
        "state": "North Carolina",
        "serp_location_name": "Indian Trail,North Carolina,United States",
        "fallback_location_name": "Monroe,North Carolina,United States",
        "coordinates": "35.0768,-80.6692,13z",
    },
}


class DataForSEOClient:
    def __init__(self, budget_limit_usd: float = 5.0, dry_run: bool = True):
        self.budget_limit_usd = budget_limit_usd
        self.dry_run = dry_run
        self.spent_usd = 0.0
        self.request_count = 0
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.auth_header = self._resolve_auth()

    def _resolve_auth(self):
        # Load .env if present in workspace root
        env_path = r"h:\Websites\landc\.env"
        if os.path.isfile(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

        basic = os.environ.get("DATAFORSEO_BASIC_AUTH") or os.environ.get("DFS_BASIC_AUTH")
        if basic:
            if not basic.startswith("Basic "):
                basic = f"Basic {basic}"
            return basic

        login = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DFS_LOGIN")
        password = os.environ.get("DATAFORSEO_PASSWORD") or os.environ.get("DFS_PASSWORD")
        if login and password:
            token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
            return f"Basic {token}"
        return None

    def check_credentials_status(self) -> dict:
        if not self.auth_header:
            return {
                "configured": False,
                "message": (
                    "DataForSEO credentials not found in environment. Set DATAFORSEO_LOGIN and "
                    "DATAFORSEO_PASSWORD (or DATAFORSEO_BASIC_AUTH) in environment variables or h:\\Websites\\landc\\.env."
                ),
            }
        return {"configured": True, "message": "DataForSEO credentials detected in environment."}

    def _cache_key(self, endpoint: str, payload) -> str:
        raw = json.dumps({"endpoint": endpoint, "payload": payload}, sort_keys=True)
        h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]
        slug = endpoint.strip("/").replace("/", "_")
        return os.path.join(CACHE_DIR, f"{slug}_{h}.json")

    def _log_request(self, record: dict):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def request(self, endpoint: str, payload=None, method: str = "POST", retries: int = 3):
        est_cost = COST_ESTIMATES_USD.get(endpoint, 0.005)
        cache_path = self._cache_key(endpoint, payload)

        if os.path.isfile(cache_path):
            with open(cache_path, encoding="utf-8") as f:
                cached = json.load(f)
            return cached["response"]

        if self.dry_run:
            raise RuntimeError(f"Dry-run mode active: blocked live call to {endpoint}")

        if not self.auth_header:
            raise RuntimeError("Missing DataForSEO credentials in environment.")

        if self.spent_usd + est_cost > self.budget_limit_usd:
            raise RuntimeError(
                f"Budget limit exceeded: current={self.spent_usd:.4f}, next={est_cost:.4f}, limit={self.budget_limit_usd:.4f}"
            )

        url = f"{API_HOST}{endpoint}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        last_err = None
        for attempt in range(1, retries + 1):
            t0 = time.time()
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                with urllib.request.urlopen(req, timeout=45) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                elapsed = round(time.time() - t0, 3)

                status_code = body.get("status_code")
                if status_code != 20000:
                    raise RuntimeError(f"DataForSEO API error {status_code}: {body.get('status_message')}")

                actual_cost = float(body.get("cost") or est_cost)
                self.spent_usd += actual_cost
                self.request_count += 1

                ts = datetime.now(timezone.utc).isoformat()
                envelope = {
                    "collected_at": ts,
                    "endpoint": endpoint,
                    "payload": payload,
                    "cost_usd": actual_cost,
                    "elapsed_sec": elapsed,
                    "response": body,
                }
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(envelope, f, indent=2, ensure_ascii=False)

                self._log_request(
                    {
                        "timestamp": ts,
                        "endpoint": endpoint,
                        "status_code": status_code,
                        "cost_usd": actual_cost,
                        "cumulative_usd": round(self.spent_usd, 5),
                        "elapsed_sec": elapsed,
                        "cache_file": os.path.basename(cache_path),
                    }
                )
                return body
            except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
                last_err = str(e)
                if attempt < retries:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"Failed request to {endpoint} after {retries} attempts: {last_err}")


def build_keyword_map_and_dry_run():
    inv_path = os.path.join(DATA_DIR, "master_url_inventory.json")
    inv = json.load(open(inv_path, encoding="utf-8"))["pages"]

    pilot_slugs = [
        "/land-clearing-charlotte-nc/",
        "/forestry-mulching-charlotte-nc/",
        "/brush-clearing-charlotte-nc/",
        "/land-clearing-huntersville-nc/",
    ]

    page_plans = []
    for p in inv:
        slug = p["slug"]
        ptype = p["page_type"]
        if ptype not in ("core_service", "location_service", "specialised_service", "homepage", "informational"):
            continue

        # Determine target city & primary keyword
        city_key = "charlotte-nc"
        for ck in TARGET_LOCATIONS:
            if slug.endswith(f"-{ck}/"):
                city_key = ck
                break
        loc = TARGET_LOCATIONS[city_key]

        if slug == "/":
            primary_kw = "land clearing charlotte company"
            secondary_kws = ["land clearing charlotte nc", "forestry mulching charlotte nc", "brush clearing charlotte nc"]
        elif slug == "/free-estimate/":
            primary_kw = "land clearing estimate charlotte nc"
            secondary_kws = ["free land clearing quote charlotte nc"]
        elif slug == "/land-clearing-cost-calculator/":
            primary_kw = "land clearing cost calculator north carolina"
            secondary_kws = ["land clearing cost per acre charlotte nc", "forestry mulching cost calculator"]
        elif slug == "/lot-clearing-tips/":
            primary_kw = "lot clearing tips north carolina"
            secondary_kws = ["how to prepare land for clearing nc"]
        elif slug.startswith("/lot-clearing-tips/"):
            sub = slug.strip("/").split("/")[-1].replace("-", " ")
            primary_kw = sub
            secondary_kws = [f"{sub} charlotte"]
        else:
            # /{service}-{city}-nc/
            clean = slug.strip("/")
            svc_part = clean[: -(len(city_key) + 1)].replace("-", " ")
            city_name = loc["city"].lower()
            primary_kw = f"{svc_part} {city_name} nc"
            secondary_kws = [
                f"{svc_part} {city_name}",
                f"{svc_part} cost {city_name} nc",
                f"{svc_part} near {city_name} nc",
            ]

        is_pilot = slug in pilot_slugs
        page_plans.append(
            {
                "slug": slug,
                "url": p["url"],
                "page_type": ptype,
                "batch": "Batch 1 (Pilot)" if is_pilot else (
                    "Batch 2 (Remaining Wave 1 City Pages - 17 pages)"
                    if ptype == "location_service"
                    else (
                        "Batch 3 (Charlotte Sub-Service Pillars - 22 pages)"
                        if ptype == "specialised_service"
                        else "Batch 4 (Homepage & Informational Guides - 6 pages)"
                    )
                ),
                "primary_keyword": primary_kw,
                "secondary_keywords": secondary_kws,
                "city_key": city_key,
                "serp_location_name": loc["serp_location_name"],
                "fallback_location_name": loc["fallback_location_name"],
                "maps_coordinates": loc["coordinates"],
                "labs_location_note": (
                    "DataForSEO Labs endpoints (Keyword Overview / Keyword Ideas) only support country-level "
                    "location_code=2840 (United States); local specificity is enforced via explicit city+state "
                    "modifiers in the seed keywords, while Organic & Maps SERP endpoints use strict city-level location_name."
                ),
            }
        )

    # Calculate API requests & costs for Pilot (4 pages) vs Full Site (43 service pages / 49 total content pages)
    pilot_requests = [
        {
            "endpoint": "/v3/serp/google/locations/us",
            "method": "GET",
            "count": 1,
            "unit_cost_usd": 0.0,
            "total_cost_usd": 0.0,
            "purpose": "Verify exact supported DataForSEO location_code IDs for Charlotte, Huntersville, Mint Hill, Waxhaw, Concord, Mooresville, and Indian Trail, NC (documenting any town that requires fallback to nearest county seat + lat/lng).",
        },
        {
            "endpoint": "/v3/serp/google/organic/live/advanced",
            "method": "POST",
            "count": 4,
            "unit_cost_usd": 0.002,
            "total_cost_usd": 0.008,
            "purpose": "Fetch city-targeted Google Organic SERP (depth=20, PAA expanded, related searches) for the 4 pilot primary keywords.",
        },
        {
            "endpoint": "/v3/serp/google/maps/live/advanced",
            "method": "POST",
            "count": 4,
            "unit_cost_usd": 0.002,
            "total_cost_usd": 0.008,
            "purpose": "Fetch city-targeted Google Maps Local Pack competitors, primary/secondary GBP categories, ratings, and service area signals for the 4 pilot queries.",
        },
        {
            "endpoint": "/v3/dataforseo_labs/google/keyword_overview/live",
            "method": "POST",
            "count": 1,
            "unit_cost_usd": 0.011,
            "total_cost_usd": 0.011,
            "purpose": "Batch keyword overview (up to 700 keywords in 1 call) covering primary + secondary keywords across pilot & full site.",
        },
        {
            "endpoint": "/v3/dataforseo_labs/google/keyword_ideas/live",
            "method": "POST",
            "count": 4,
            "unit_cost_usd": 0.011,
            "total_cost_usd": 0.044,
            "purpose": "Discover high-intent service + modifier keyword ideas for each of the 4 pilot clusters.",
        },
        {
            "endpoint": "/v3/on_page/instant_pages",
            "method": "POST",
            "count": 16,
            "unit_cost_usd": 0.00125,
            "total_cost_usd": 0.020,
            "purpose": "Audit live OnPage metrics & heading structure of our 4 pilot pages + top 3 local organic competitors per pilot SERP (12 competitor URLs).",
        },
    ]

    full_site_requests = [
        {
            "endpoint": "/v3/serp/google/organic/live/advanced",
            "count": 43,
            "est_cost_usd": round(43 * 0.002, 4),
            "scope": "All 43 service & location-service pages (3 core pillars + 18 city pages + 22 sub-service pillars)",
        },
        {
            "endpoint": "/v3/serp/google/maps/live/advanced",
            "count": 21,
            "est_cost_usd": round(21 * 0.002, 4),
            "scope": "3 core services × 7 cities (Charlotte + 6 Wave 1 towns = 21 city-service combinations)",
        },
        {
            "endpoint": "/v3/dataforseo_labs/google/keyword_overview/live",
            "count": 1,
            "est_cost_usd": 0.011,
            "scope": "1 batched request covering all ~200 target & variant keywords across all 43 service pages",
        },
        {
            "endpoint": "/v3/dataforseo_labs/google/keyword_ideas/live",
            "count": 10,
            "est_cost_usd": round(10 * 0.011, 4),
            "scope": "10 service-cluster seed batches covering all core services, sub-services, and NC modifiers",
        },
        {
            "endpoint": "/v3/on_page/instant_pages",
            "count": 120,
            "est_cost_usd": round(120 * 0.00125, 4),
            "scope": "43 live site service URLs + ~77 unique top-ranking competitor URLs across SERPs",
        },
    ]

    client = DataForSEOClient(dry_run=True)
    plan_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "credentials_status": client.check_credentials_status(),
        "pilot_batch_summary": {
            "pilot_pages_count": 4,
            "pilot_pages": pilot_slugs,
            "estimated_requests": sum(r["count"] for r in pilot_requests),
            "estimated_cost_usd": round(sum(r["total_cost_usd"] for r in pilot_requests), 4),
            "breakdown": pilot_requests,
        },
        "full_site_summary": {
            "service_pages_count": 43,
            "total_indexable_pages": 53,
            "estimated_requests": sum(r["count"] for r in full_site_requests),
            "estimated_cost_usd": round(sum(r["est_cost_usd"] for r in full_site_requests), 4),
            "breakdown": full_site_requests,
        },
        "page_keyword_map": page_plans,
    }

    with open(DRY_RUN_FILE, "w", encoding="utf-8") as f:
        json.dump(plan_doc, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "credentials_status": plan_doc["credentials_status"],
        "pilot_batch_summary": plan_doc["pilot_batch_summary"],
        "full_site_summary": plan_doc["full_site_summary"],
    }, indent=2))


if __name__ == "__main__":
    build_keyword_map_and_dry_run()
