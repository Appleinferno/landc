"""Sync Section 7 (Other Services) across all *-nc service pages using lib.other_services_groups()."""
import glob, os, re
from lib import ROOT, TOWNS, other_services_groups

CITY_MAP = {"charlotte-nc": "Charlotte"}
for ts, tn in TOWNS:
    CITY_MAP[f"{ts}-nc"] = tn

pat = re.compile(
    r'(<!-- 7\. OTHER SERVICES[^\n]*\n\s*<section class="svc-section svc-section--white" aria-labelledby="other-title">\s*<div class="svc-container">\s*<div class="svc-head">.*?</div>\n\n)'
    r'(.*?)'
    r'(\n      </div>\n    </section>)',
    re.S,
)

updated = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*-nc", "index.html"))):
    slug = os.path.basename(os.path.dirname(path))
    city_slug = next((cs for cs in CITY_MAP if slug.endswith("-" + cs)), None)
    if not city_slug:
        continue
    city = CITY_MAP[city_slug]
    groups = other_services_groups(slug, city=city, city_slug=city_slug)
    src = open(path, encoding="utf-8").read()
    m = pat.search(src)
    if not m:
        print(f"WARN: no Section 7 match in {slug}")
        continue
    head_block = re.sub(
        r"<!-- 7\. OTHER SERVICES[^\n]*",
        f"<!-- 7. OTHER SERVICES IN {city.upper()} (fixed order: Land, Forestry, Brush) -->",
        m.group(1),
    )
    new_src = src[:m.start()] + head_block + groups + m.group(3) + src[m.end():]
    if new_src != src:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_src)
        updated += 1
        print(f"updated: {slug}")

print(f"Total updated: {updated}")
