import os
import re
import json
from html import unescape
from inventory import get_shingles, clean_text
from build_city_batch import CITY_ENRICHMENTS

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
ENGINE_DIR = r"h:\Websites\landc\tools\seo_engine"
DATA_DIR = os.path.join(ENGINE_DIR, "data")
DELIV_DIR = os.path.join(ENGINE_DIR, "deliverables")
STAGING_DIR = os.path.join(ENGINE_DIR, "staging")

FORBIDDEN_PATTERNS = [
    (r"we\s+(offer|provide|do|perform)\s+(finish\s+)?grading", "Forbidden claim: offering grading"),
    (r"we\s+(apply|spray|use)\s+(herbicides?|chemicals?)", "Forbidden claim: chemical/herbicide application"),
    (r"kudzu\s+removal\s+service", "Forbidden claim: kudzu removal service"),
    (r"\$2,000\s*\?\s*\$8,000", "Encoding bug: ? in price range"),
]

def main():
    city_slugs = list(CITY_ENRICHMENTS.keys())
    qa_results = []

    # Also compute pairwise 4-gram Jaccard similarity across all 18 Wave 1 city pages BEFORE vs AFTER
    all_18_slugs = ["land-clearing-huntersville-nc"] + city_slugs
    shingles_before = {}
    shingles_after = {}

    for s in all_18_slugs:
        orig_p = os.path.join(ROOT, s, "index.html")
        staged_p = os.path.join(STAGING_DIR, s, "index.html")
        orig_c = open(orig_p, encoding="utf-8").read()
        staged_c = open(staged_p, encoding="utf-8").read() if os.path.exists(staged_p) else orig_c
        # Extract .svc-prose text
        pb_orig = re.search(r'<div class="[^"]*svc-prose[^"]*">(.*?)</div>\s*</div>\s*</section>', orig_c, re.S)
        pb_staged = re.search(r'<div class="[^"]*svc-prose[^"]*">(.*?)</div>\s*</div>\s*</section>', staged_c, re.S)
        t_orig = clean_text(pb_orig.group(1)) if pb_orig else clean_text(orig_c)
        t_staged = clean_text(pb_staged.group(1)) if pb_staged else clean_text(staged_c)
        shingles_before[s] = get_shingles(t_orig, 4)
        shingles_after[s] = get_shingles(t_staged, 4)

    pairs_before = []
    pairs_after = []
    for i in range(len(all_18_slugs)):
        for j in range(i + 1, len(all_18_slugs)):
            s1, s2 = all_18_slugs[i], all_18_slugs[j]
            jb = len(shingles_before[s1] & shingles_before[s2]) / len(shingles_before[s1] | shingles_before[s2])
            ja = len(shingles_after[s1] & shingles_after[s2]) / len(shingles_after[s1] | shingles_after[s2])
            pairs_before.append((jb, s1, s2))
            pairs_after.append((ja, s1, s2))

    max_before = max(pairs_before, key=lambda x: x[0])
    max_after = max(pairs_after, key=lambda x: x[0])
    avg_before = sum(x[0] for x in pairs_before) / len(pairs_before)
    avg_after = sum(x[0] for x in pairs_after) / len(pairs_after)

    for slug in city_slugs:
        staged_path = os.path.join(STAGING_DIR, slug, "index.html")
        orig_path = os.path.join(ROOT, slug, "index.html")
        c = open(staged_path, encoding="utf-8").read()
        orig_c = open(orig_path, encoding="utf-8").read()

        checks = {}

        # 1. Single H1 & Title consistency
        h1s = [clean_text(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", c, re.S)]
        title_m = re.search(r"<title>(.*?)</title>", c, re.S)
        title = unescape(title_m.group(1).strip()) if title_m else ""
        checks["single_h1_and_title"] = {
            "passed": len(h1s) == 1 and h1s[0] in title,
            "h1": h1s[0] if h1s else None,
            "title": title,
        }

        # 2. Canonical & og:url match
        expected_url = f"https://landclearingcharlotte.com/{slug}/"
        canon_m = re.search(r'rel="canonical" href="([^"]+)"', c)
        og_m = re.search(r'property="og:url" content="([^"]+)"', c)
        checks["canonical_and_indexability"] = {
            "passed": bool(canon_m and canon_m.group(1) == expected_url and og_m and og_m.group(1) == expected_url and "noindex" not in c.lower()),
            "canonical": canon_m.group(1) if canon_m else None,
        }

        # 3. No internal links inside .svc-prose body copy
        from bs4 import BeautifulSoup
        soup_c = BeautifulSoup(c, "html.parser")
        prose_links = []
        for pb in soup_c.find_all("div", class_="svc-prose"):
            for a_tag in pb.find_all("a", href=True):
                prose_links.append(a_tag["href"])
        checks["zero_links_in_body_prose"] = {
            "passed": len(prose_links) == 0,
            "links_found": prose_links,
        }

        # 4. Internal links resolve against production ROOT
        broken = []
        for _, h in re.findall(r'(?<![\w-])(href|src|srcset)="([^"]+)"', c):
            if h.startswith(("http", "tel:", "mailto:", "#", "data:")):
                continue
            h_clean = h.split("#")[0].split("?")[0].strip()
            t = os.path.normpath(os.path.join(os.path.dirname(orig_path), h_clean))
            if not (os.path.isfile(t) or os.path.isfile(os.path.join(t, "index.html"))):
                broken.append(h)
        checks["zero_broken_links"] = {"passed": len(broken) == 0, "broken": broken}

        # 5. Schema JSON-LD validity & 1:1 FAQPage alignment + multi-city areaServed
        ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.S)
        schema_ok = True
        faq_schema_count = 0
        schema_types = []
        area_served_cities = []
        for blk in ld_blocks:
            try:
                jd = json.loads(blk)
                for node in jd.get("@graph", []):
                    schema_types.append(node.get("@type"))
                    if node.get("@type") == "FAQPage":
                        faq_schema_count = len(node.get("mainEntity", []))
                    if node.get("@type") == "LocalBusiness":
                        areas = node.get("areaServed", [])
                        if isinstance(areas, list):
                            area_served_cities = [a.get("name") for a in areas if isinstance(a, dict)]
            except Exception:
                schema_ok = False
        visible_faqs = len(re.findall(r'<details class="svc-faq__item">', c))
        expected_city = CITY_ENRICHMENTS[slug]["city_name"]
        checks["schema_and_faq_parity"] = {
            "passed": schema_ok and faq_schema_count == visible_faqs and faq_schema_count == 8 and expected_city in area_served_cities,
            "schema_types": schema_types,
            "visible_faq_count": visible_faqs,
            "schema_faq_count": faq_schema_count,
            "area_served_cities": area_served_cities,
        }

        # 6. Form & CTA integrity
        form_ok = (
            'action="https://formcarry.com/s/za8glfgKic_"' in c
            and "data-estimate-form" in c
            and 'href="tel:7047416895"' in c
            and "(704) 741-6895" in c
            and '"+1-704-741-6895"' in c
        )
        checks["form_and_phone_integrity"] = {"passed": form_ok}

        # 7. Accessibility & Responsive Table wrapper
        tables = re.findall(r'<div class="legal-document__table-container">\s*<table class="legal-document__clause-table">(.*?)</table>\s*</div>', c, re.S)
        th_scopes = re.findall(r'<th\s+scope="col">', c)
        checks["responsive_table_and_a11y"] = {
            "passed": len(tables) == 1 and len(th_scopes) == 3,
            "responsive_tables_count": len(tables),
            "th_scope_col_count": len(th_scopes),
        }

        # 8. Fact-check & forbidden service scan
        violations = []
        for pat, msg in FORBIDDEN_PATTERNS:
            if re.search(pat, c, re.I):
                violations.append(msg)
        checks["fact_and_scope_guardrails"] = {
            "passed": len(violations) == 0,
            "violations": violations,
        }

        all_passed = all(v["passed"] for v in checks.values())
        qa_results.append({
            "slug": f"/{slug}/",
            "all_passed": all_passed,
            "checks": checks
        })

    summary = {
        "total_staged_pages": len(qa_results),
        "all_passed_count": sum(1 for r in qa_results if r["all_passed"]),
        "similarity_stats": {
            "max_pairwise_4gram_before": round(max_before[0], 4),
            "max_pair_before": [max_before[1], max_before[2]],
            "max_pairwise_4gram_after": round(max_after[0], 4),
            "max_pair_after": [max_after[1], max_after[2]],
            "avg_pairwise_4gram_before": round(avg_before, 4),
            "avg_pairwise_4gram_after": round(avg_after, 4),
        },
        "results": qa_results,
    }

    out_p = os.path.join(DATA_DIR, "city_batch_qa_results.json")
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"QA Passed: {summary['all_passed_count']}/{summary['total_staged_pages']} Wave 1 city pages.")
    print(f"Pairwise 4-gram Jaccard across 18 city pages:")
    print(f"  Max before: {summary['similarity_stats']['max_pairwise_4gram_before']} ({max_before[1]} vs {max_before[2]})")
    print(f"  Max after:  {summary['similarity_stats']['max_pairwise_4gram_after']} ({max_after[1]} vs {max_after[2]})")
    print(f"  Avg before: {summary['similarity_stats']['avg_pairwise_4gram_before']} -> Avg after: {summary['similarity_stats']['avg_pairwise_4gram_after']}")

if __name__ == "__main__":
    main()
