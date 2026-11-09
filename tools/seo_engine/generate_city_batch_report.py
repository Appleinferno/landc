import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DELIV_DIR = os.path.join(BASE_DIR, "deliverables")

def main():
    bundle = json.load(open(os.path.join(DATA_DIR, "city_batch_raw_bundle.json"), encoding="utf-8"))
    stats = json.load(open(os.path.join(DATA_DIR, "city_batch_stats.json"), encoding="utf-8"))
    qa = json.load(open(os.path.join(DATA_DIR, "city_batch_qa_results.json"), encoding="utf-8"))

    stats_by_slug = {s["slug"]: s for s in stats}
    qa_by_slug = {r["slug"]: r for r in qa["results"]}

    lines = [
        "# Wave 1 City Pages Batch — SERP Research, Enrichments & QA Report (17 Pages)",
        "",
        "## 1. Executive Summary",
        "- **Scope:** 17 remaining Wave 1 Location-Service pages across `Huntersville`, `Mint Hill`, `Waxhaw`, `Concord`, `Mooresville`, and `Indian Trail` (`/land-clearing-huntersville-nc/` was already enriched and deployed in the Pilot batch).",
        "- **DataForSEO Collection:** Executed 17 city-targeted Google Organic SERP Advanced queries + 17 city-targeted Google Maps SERP Advanced queries (`34` API requests total, cached in `tools/seo_engine/data/cache/` and bundled in `tools/seo_engine/data/city_batch_raw_bundle.json`).",
        f"- **Phase 6 QA Status:** **{qa['all_passed_count']}/{qa['total_staged_pages']} PASS** across all 8 automated checks.",
        f"- **Pairwise 4-gram Jaccard Similarity Reduction (18 City Pages):**",
        f"  - Maximum pairwise similarity dropped from **`{qa['similarity_stats']['max_pairwise_4gram_before']}`** (`21.85%`) to **`{qa['similarity_stats']['max_pairwise_4gram_after']}`** (`17.61%`).",
        f"  - Average pairwise similarity dropped from **`{qa['similarity_stats']['avg_pairwise_4gram_before']}`** (`12.01%`) to **`{qa['similarity_stats']['avg_pairwise_4gram_after']}`** (`8.93%`) — a **25.6% relative reduction** in cross-city boilerplate.",
        "",
        "## 2. Live City-Level SERP Baseline & Word-Count Delta (All 17 Pages)",
        "",
        "| Page Slug | Primary Keyword | Location Code | Our Organic Rank | Top Local Pack #1 | Words Before | Words After | Delta | Tables | FAQ Schema | QA |",
        "| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for page_key, pdata in bundle["pages"].items():
        slug = pdata["slug"]
        st = stats_by_slug.get(slug, {})
        qr = qa_by_slug.get(slug, {})
        rank_str = f"#{pdata['our_organic_rank']}" if pdata.get("our_organic_rank") else "Not in Top 20"
        maps_top1 = pdata["maps_top5"][0]["title"] if pdata.get("maps_top5") else "N/A"
        lines.append(
            f"| `{slug}` | `{pdata['keyword']}` | `{pdata['location_code']}` | {rank_str} | {maps_top1} | {st.get('words_before')} | {st.get('words_after')} | `+{st.get('delta_words')}` | `{st.get('tables_after')}` | `{st.get('faqs_after')}/8` | {'PASS' if qr.get('all_passed') else 'FAIL'} |"
        )

    lines.extend([
        "",
        "## 3. Page-by-Page SERP Insights & PAA Opportunities",
        ""
    ])

    for page_key, pdata in bundle["pages"].items():
        slug = pdata["slug"]
        lines.append(f"### `{slug}` (`{pdata['keyword']}` @ `{pdata['location_name']}`)")
        org3 = [f"#{x['rank_group']} `{x['domain']}` ({x['title']})" for x in pdata.get("organic_top10", [])[:3]]
        maps3 = [f"#{x['rank_group']} {x['title']} ({x.get('rating', 'N/A')}★, {x.get('reviews_count', 0)} reviews)" for x in pdata.get("maps_top5", [])[:3]]
        paas = pdata.get("paa_questions", [])[:5]
        lines.append(f"- **Top 3 Organic Competitors:** {'; '.join(org3) if org3 else 'None'}")
        lines.append(f"- **Top 3 Google Maps Pack:** {'; '.join(maps3) if maps3 else 'None'}")
        lines.append(f"- **People Also Ask (PAA):** {'; '.join(paas) if paas else 'None returned'}")
        lines.append("")

    report_path = os.path.join(DELIV_DIR, "11_wave1_city_batch_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {report_path}")

if __name__ == "__main__":
    main()
