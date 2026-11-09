"""Phase 1 — Website Inventory & Technical SEO Audit for LandClearingCharlotte.com.

Discovers all indexable and non-indexable URLs from sitemap.xml, local HTML files, and internal link crawl.
Extracts titles, meta descriptions, H1-H3 headings, main content metrics, canonical tags, schema, internal links, and CTAs.
Classifies pages into homepage, core_service, specialised_service, location_service, informational, and utility.
Identifies potential duplicates, content overlap (3-gram Jaccard similarity), broken links, and metadata issues.
"""
import os
import re
import glob
import json
import hashlib
from html import unescape
from collections import Counter

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
BASE = "https://landclearingcharlotte.com"
OUT_DIR = r"h:\Websites\landc\tools\seo_engine\data"

LEGAL = {"privacy-policy", "cookies-policy", "terms-and-conditions"}
CORE_PILLARS = {
    "land-clearing-charlotte-nc",
    "forestry-mulching-charlotte-nc",
    "brush-clearing-charlotte-nc",
}
CITIES = {
    "concord-nc",
    "huntersville-nc",
    "indian-trail-nc",
    "mint-hill-nc",
    "mooresville-nc",
    "waxhaw-nc",
}


def clean_text(html_fragment: str) -> str:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html_fragment, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def resolve_href(page_path: str, href: str):
    href_clean = href.split("#")[0].split("?")[0].strip()
    if not href_clean or href_clean.startswith(("http://", "https://", "tel:", "mailto:", "javascript:", "data:")):
        return None
    if href_clean.startswith("/"):
        rel = href_clean.lstrip("/")
        return os.path.normpath(os.path.join(ROOT, rel))
    target = os.path.normpath(os.path.join(os.path.dirname(page_path), href_clean))
    return target


def get_shingles(text: str, k: int = 4) -> set:
    words = [w.lower() for w in re.findall(r"[a-z0-9]+", text)]
    if len(words) < k:
        return set(words)
    return {" ".join(words[i : i + k]) for i in range(len(words) - k + 1)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    sm_path = os.path.join(ROOT, "sitemap.xml")
    sm_xml = open(sm_path, encoding="utf-8").read()
    sm_entries = re.findall(
        r"<url>\s*<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>\s*<priority>(.*?)</priority>\s*</url>",
        sm_xml,
        re.S,
    )
    sm_map = {loc.strip(): {"lastmod": lastmod.strip(), "priority": prio.strip()} for loc, lastmod, prio in sm_entries}

    html_files = sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True))
    html_files = [p for p in html_files if "_shot" not in p]
    other_html_files = [
        os.path.relpath(p, ROOT).replace("\\", "/")
        for p in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
        if os.path.basename(p) != "index.html" and "_shot" not in p
    ]

    inventory = []
    shingle_map = {}
    all_broken_links = []
    inbound_links = Counter()

    # First pass: collect inbound links across site
    for p in html_files:
        c = open(p, encoding="utf-8").read()
        for attr, h in re.findall(r'(?<![\w-])(href)="([^"]+)"', c):
            t = resolve_href(p, h)
            if t:
                if os.path.isdir(t) and os.path.isfile(os.path.join(t, "index.html")):
                    rel_t = os.path.relpath(t, ROOT).replace("\\", "/")
                    inbound_links["/" if rel_t == "." else f"/{rel_t}/"] += 1
                elif os.path.isfile(t) and os.path.basename(t) == "index.html":
                    rel_t = os.path.relpath(os.path.dirname(t), ROOT).replace("\\", "/")
                    inbound_links["/" if rel_t == "." else f"/{rel_t}/"] += 1

    for p in html_files:
        c = open(p, encoding="utf-8").read()
        rel_file = os.path.relpath(p, ROOT).replace("\\", "/")
        rel_dir = os.path.relpath(os.path.dirname(p), ROOT).replace("\\", "/")
        slug = "/" if rel_dir == "." else f"/{rel_dir}/"
        dir_key = "" if rel_dir == "." else rel_dir
        url = f"{BASE}/" if dir_key == "" else f"{BASE}/{dir_key}/"

        # Classify page
        if dir_key == "":
            ptype = "homepage"
        elif dir_key in CORE_PILLARS:
            ptype = "core_service"
        elif any(dir_key.endswith(city) for city in CITIES):
            ptype = "location_service"
        elif dir_key.endswith("-charlotte-nc"):
            ptype = "specialised_service"
        elif dir_key.startswith("lot-clearing-tips") or dir_key == "land-clearing-cost-calculator":
            ptype = "informational"
        else:
            ptype = "utility"

        title_m = re.search(r"<title>(.*?)</title>", c, re.S)
        title = unescape(title_m.group(1).strip()) if title_m else ""

        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', c) or re.search(
            r'<meta\s+content="([^"]*)"\s+name="description"', c
        )
        desc = unescape(desc_m.group(1).strip()) if desc_m else ""

        canon_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', c)
        canon = canon_m.group(1).strip() if canon_m else ""

        robots_m = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', c)
        robots = robots_m.group(1).strip() if robots_m else "index,follow (implicit)"
        is_noindex = "noindex" in robots.lower()

        h1s = [clean_text(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", c, re.S)]
        h2s = [clean_text(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", c, re.S)]
        h3s = [clean_text(h) for h in re.findall(r"<h3[^>]*>(.*?)</h3>", c, re.S)]

        main_m = re.search(r"<main[^>]*>(.*?)</main>", c, re.S)
        main_html = main_m.group(1) if main_m else c
        main_text = clean_text(main_html)
        word_count = len(main_text.split())

        # Remove shared boilerplate sections (Where We Serve, Other Services) for prose similarity check
        prose_html = re.sub(
            r'<section[^>]*id="(where-we-serve|other-services)"[^>]*>.*?</section>',
            " ",
            main_html,
            flags=re.S | re.I,
        )
        prose_text = clean_text(prose_html)
        prose_word_count = len(prose_text.split())
        shingle_map[slug] = get_shingles(prose_text, k=4)

        # Schema extraction
        schemas = []
        schema_errors = []
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.S):
            try:
                jd = json.loads(blk)
                if isinstance(jd, dict):
                    if "@graph" in jd:
                        schemas.extend([g.get("@type") for g in jd["@graph"]])
                    else:
                        schemas.append(jd.get("@type"))
                elif isinstance(jd, list):
                    schemas.extend([g.get("@type") for g in jd])
            except Exception as e:
                schema_errors.append(str(e))

        # Internal links & broken link check
        page_broken = []
        main_links = []
        proposed_data_hrefs = re.findall(r'data-href="([^"]+)"', c)
        for attr, h in re.findall(r'(?<![\w-])(href)="([^"]+)"', c):
            t = resolve_href(p, h)
            if t:
                ok = os.path.isfile(t) or os.path.isfile(os.path.join(t, "index.html"))
                if not ok:
                    page_broken.append(h)
                    all_broken_links.append({"page": slug, "href": h})

        for attr, h in re.findall(r'(?<![\w-])(href)="([^"]+)"', main_html):
            if not h.startswith(("http", "tel:", "mailto:", "#")):
                main_links.append(h)

        # CTAs and forms
        forms = re.findall(r'<form[^>]*action="([^"]*)"', c)
        tel_links = re.findall(r'href="tel:([^"]+)"', c)
        price_qmark_bug = "$2,000 ? $8,000" in c
        has_price_range = bool(re.search(r"\$2,000\s*[-–—?]\s*\$8,000", c))

        sm_info = sm_map.get(url)
        inventory.append(
            {
                "slug": slug,
                "file": rel_file,
                "url": url,
                "page_type": ptype,
                "in_sitemap": sm_info is not None,
                "sitemap_lastmod": sm_info["lastmod"] if sm_info else None,
                "sitemap_priority": sm_info["priority"] if sm_info else None,
                "indexable": not is_noindex,
                "robots_meta": robots,
                "canonical": canon,
                "canonical_valid": canon == url,
                "title": title,
                "title_length": len(title),
                "meta_description": desc,
                "meta_description_length": len(desc),
                "h1_count": len(h1s),
                "h1": h1s[0] if h1s else "",
                "h2_count": len(h2s),
                "h2s": h2s,
                "h3_count": len(h3s),
                "h3s": h3s,
                "main_word_count": word_count,
                "prose_word_count": prose_word_count,
                "schema_types": schemas,
                "schema_errors": schema_errors,
                "form_actions": forms,
                "tel_cta_count": len(tel_links),
                "main_internal_links_count": len(main_links),
                "inbound_internal_links_count": inbound_links[slug],
                "broken_links": page_broken,
                "has_price_range_2k_8k": has_price_range,
                "has_price_qmark_encoding_bug": price_qmark_bug,
            }
        )

    # Calculate pairwise 4-gram Jaccard similarity on prose to detect near-duplicates / overlap
    overlaps = []
    slugs = [item["slug"] for item in inventory if item["page_type"] not in ("utility",)]
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            s1, s2 = slugs[i], slugs[j]
            sh1, sh2 = shingle_map[s1], shingle_map[s2]
            if not sh1 or not sh2:
                continue
            inter = len(sh1 & sh2)
            union = len(sh1 | sh2)
            jaccard = inter / union if union else 0.0
            if jaccard >= 0.08:
                overlaps.append({"page_a": s1, "page_b": s2, "jaccard_4gram": round(jaccard, 4)})
    overlaps.sort(key=lambda x: x["jaccard_4gram"], reverse=True)

    # Title and meta description duplicates
    title_counts = Counter(x["title"] for x in inventory)
    desc_counts = Counter(x["meta_description"] for x in inventory)
    h1_counts = Counter(x["h1"] for x in inventory)

    summary = {
        "generated_at": "2026-11-07T21:30:00-05:00",
        "total_local_html_pages": len(inventory),
        "total_sitemap_urls": len(sm_map),
        "indexable_pages": sum(1 for x in inventory if x["indexable"]),
        "counts_by_type": dict(Counter(x["page_type"] for x in inventory)),
        "duplicate_titles": {k: v for k, v in title_counts.items() if v > 1},
        "duplicate_meta_descriptions": {k: v for k, v in desc_counts.items() if v > 1},
        "duplicate_h1s": {k: v for k, v in h1_counts.items() if v > 1},
        "missing_titles": [x["slug"] for x in inventory if not x["title"]],
        "missing_meta_descriptions": [x["slug"] for x in inventory if not x["meta_description"]],
        "invalid_canonicals": [x["slug"] for x in inventory if not x["canonical_valid"]],
        "broken_links": all_broken_links,
        "price_qmark_encoding_bug_pages": [x["slug"] for x in inventory if x["has_price_qmark_encoding_bug"]],
        "pages_missing_price_benchmark": [
            x["slug"]
            for x in inventory
            if x["page_type"] in ("core_service", "specialised_service", "location_service")
            and not x["has_price_range_2k_8k"]
        ],
        "top_prose_overlaps": overlaps[:20],
    }

    with open(os.path.join(OUT_DIR, "master_url_inventory.json"), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "pages": inventory}, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
