"""Inspect the cached Organic SERP, Maps SERP, Keyword Overview, and Keyword Ideas responses."""
import os
import json

DATA_DIR = r"h:\Websites\landc\tools\seo_engine\data"
bundle = json.load(open(os.path.join(DATA_DIR, "pilot_raw_bundle.json"), encoding="utf-8"))

# 1. Inspect Keyword Overview
kw_items = (bundle["keyword_overview"].get("tasks", [{}])[0].get("result") or [{}])[0].get("items") or []
print(f"Keyword Overview returned {len(kw_items)} items with search volume:")
for it in sorted(kw_items, key=lambda x: (x.get("keyword_info", {}).get("search_volume") or 0), reverse=True)[:30]:
    info = it.get("keyword_info", {})
    props = it.get("keyword_properties", {})
    intent = (it.get("search_intent_info") or {}).get("main_intent")
    print(f"  {it['keyword']:42} | vol={str(info.get('search_volume')):6} | cpc={str(info.get('cpc')):6} | kd={str(props.get('keyword_difficulty')):4} | intent={intent}")

# 2. Inspect Organic SERP items for each pilot page
for slug, pdata in bundle["pilot_pages"].items():
    print("\n==========================================")
    print("PILOT PAGE:", slug, "| Keyword:", pdata["meta"]["primary_keyword"])
    res = (pdata["organic_serp"].get("tasks", [{}])[0].get("result") or [{}])[0]
    items = res.get("items") or []
    for it in items:
        t = it.get("type")
        if t == "organic":
            print(f"  [ORG #{it.get('rank_group')}] domain={it.get('domain')} | title={it.get('title')} | url={it.get('url')[:60]} | breadcrumb={it.get('breadcrumb')}")
        elif t == "people_also_ask":
            paa = [q.get("title") for q in (it.get("items") or [])]
            print(f"  [PAA] {paa}")
        elif t == "related_searches":
            print(f"  [RELATED] {it.get('items')}")
        elif t == "local_pack":
            print(f"  [LOCAL PACK] title={it.get('title')} domain={it.get('domain')} rating={it.get('rating')}")

    # Maps SERP
    mres = (pdata["maps_serp"].get("tasks", [{}])[0].get("result") or [{}])[0]
    mitems = mres.get("items") or []
    print("  --- MAPS TOP 5 ---")
    for mit in mitems[:5]:
        print(f"    [MAPS #{mit.get('rank_group')}] {mit.get('title')} | cat={mit.get('category')} | add_cats={mit.get('additional_categories')} | rating={mit.get('rating')} | domain={mit.get('domain')} | url={mit.get('url')}")
