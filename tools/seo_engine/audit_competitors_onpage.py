"""Run OnPage Instant Pages on the actual local competitor websites and inspect their H1-H3 headings, word counts, and content structure."""
import os
import json
from dataforseo_client import DataForSEOClient, DATA_DIR

COMPETITOR_URLS = [
    # Direct Maps & Organic competitors in Charlotte & Huntersville
    "https://www.carolinalcd.com/",
    "https://redhatlandservices.com/",
    "https://carolinabrushcontrol.com/",
    "https://boombrushcontrol.com/",
    "https://bigfootforestry.com/charlotte-nc/",
    "https://www.keeterlandmanagement.com/forestry-mulching",
    "https://www.fischerearthworks.com/land-clearing-charlotte",
    "https://tzclearing.com/",
    "https://vistalandclearing.com/",
    "https://www.lds-solutions.com/",
]


def main():
    client = DataForSEOClient(budget_limit_usd=0.10, dry_run=False)
    bundle_path = os.path.join(DATA_DIR, "pilot_raw_bundle.json")
    bundle = json.load(open(bundle_path, encoding="utf-8"))

    comp_onpage = bundle.get("onpage_instant", {})

    for u in COMPETITOR_URLS:
        try:
            resp = client.request(
                "/v3/on_page/instant_pages",
                [{"url": u, "enable_javascript": False, "load_resources": False}],
            )
            comp_onpage[u] = resp
        except Exception as e:
            comp_onpage[u] = {"error": str(e)}

    bundle["onpage_instant"] = comp_onpage
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    print(f"Additional OnPage calls: {client.request_count}, cost: ${client.spent_usd:.5f}")
    # Print summary of our 4 pilot pages + 10 competitor pages from OnPage Instant Pages
    all_urls = [
        "https://landclearingcharlotte.com/land-clearing-charlotte-nc/",
        "https://landclearingcharlotte.com/forestry-mulching-charlotte-nc/",
        "https://landclearingcharlotte.com/brush-clearing-charlotte-nc/",
        "https://landclearingcharlotte.com/land-clearing-huntersville-nc/",
    ] + COMPETITOR_URLS

    for u in all_urls:
        r = comp_onpage.get(u, {})
        items = (r.get("tasks", [{}])[0].get("result") or [{}])[0].get("items") or []
        if not items:
            print(f"[NO ITEMS] {u}: {r.get('error') or 'empty'}")
            continue
        it = items[0]
        meta = it.get("meta") or {}
        content = meta.get("content") or {}
        htags = meta.get("htags") or {}
        print(
            f"\nURL: {u} (status={it.get('status_code')}, score={it.get('onpage_score')}, words={content.get('plain_text_word_count')})"
        )
        print("  Title:", meta.get("title"))
        print("  H1:", htags.get("h1"))
        print("  H2:", (htags.get("h2") or [])[:8])
        print("  H3:", (htags.get("h3") or [])[:8])


if __name__ == "__main__":
    main()
