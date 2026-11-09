import os
import re
import shutil
from build_city_batch import CITY_ENRICHMENTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "charlotte-land-clearing"))
STAGING_DIR = os.path.join(BASE_DIR, "staging")
SITEMAP_PATH = os.path.join(ROOT, "sitemap.xml")
TODAY = "2026-11-08"

def main():
    deployed = []
    for slug in CITY_ENRICHMENTS.keys():
        src = os.path.join(STAGING_DIR, slug, "index.html")
        dst = os.path.join(ROOT, slug, "index.html")
        assert os.path.isfile(src), f"Missing staged file: {src}"
        shutil.copyfile(src, dst)
        deployed.append(slug)

    sitemap_xml = open(SITEMAP_PATH, encoding="utf-8").read()
    updated_urls = 0
    for slug in deployed:
        loc_url = f"https://landclearingcharlotte.com/{slug}/"
        pattern = rf"(<loc>{re.escape(loc_url)}</loc>\s*<lastmod>)(\d{{4}}-\d{{2}}-\d{{2}})(</lastmod>)"
        new_xml, count = re.subn(pattern, rf"\g<1>{TODAY}\g<3>", sitemap_xml)
        assert count == 1, f"Did not find {loc_url} in sitemap.xml"
        sitemap_xml = new_xml
        updated_urls += count

    with open(SITEMAP_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap_xml)

    print(f"Deployed {len(deployed)} Wave 1 city pages to {ROOT} and updated {updated_urls} <lastmod> entries to {TODAY} in sitemap.xml.")

if __name__ == "__main__":
    main()
