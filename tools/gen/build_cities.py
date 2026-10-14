"""Build core city child pages and sync proposed area cards, Other Services, and footer Service Areas links."""
import glob, os, re, sys
from lib import ROOT, TOWNS, exists, other_services_groups
from gen_city import render_city
import content_cities as cc

only = set(sys.argv[1:])
pages = [
    p for p in cc.PAGES
    if not only or f'{p["silo"]}-{p["town_slug"]}' in only or f'{p["silo"]}-clearing-{p["town_slug"]}-nc' in only or f'{p["town_slug"]}' in only
]

for p in pages:
    slug, wc = render_city(p)
    print(f"{slug}: ~{wc} words")

# 1. Turn any proposed area cards whose target now exists into live <a> cards
area_pat = re.compile(
    r'<div class="svc-area-card svc-area-card--proposed" data-href="([^"]+)">\s*(.*?)\s*</div>',
    re.S,
)

# 2. Footer Service Areas block pattern
footer_pat = re.compile(
    r'(<h4 class="site-footer__col-heading--white-uppercase">Service Areas</h4>\s*<ul class="site-footer__links-list">\n)(.*?)(\n\s*</ul>)',
    re.S,
)

def pick_town_target(ts):
    for prefix in ("land-clearing", "forestry-mulching", "brush-clearing"):
        cand = f"{prefix}-{ts}-nc"
        if exists(cand):
            return cand
    return None

all_html = sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True))
all_html = [p for p in all_html if "_shot" not in p]

for path in all_html:
    src = open(path, encoding="utf-8").read()
    orig = src
    rel_dir = os.path.relpath(os.path.dirname(path), ROOT).replace("\\", "/")
    prefix = "" if rel_dir == "." else "../" * len(rel_dir.split("/"))

    def repl_area(m):
        href, inner = m.group(1), m.group(2)
        target_dir = os.path.normpath(os.path.join(os.path.dirname(path), href))
        if os.path.isfile(os.path.join(target_dir, "index.html")):
            return f'<a class="svc-area-card" href="{href}">\n            {inner}\n          </a>'
        return m.group(0)

    src = area_pat.sub(repl_area, src)

    def repl_footer(m):
        indent = "            "
        items = []
        for ts, tn in TOWNS:
            t_slug = pick_town_target(ts)
            if t_slug:
                items.append(f'{indent}<li><a class="site-footer__link-item--gold-hover" href="{prefix}{t_slug}/">{tn}, NC</a></li>')
            else:
                items.append(f'{indent}<li><span class="site-footer__link-item--muted">{tn}, NC</span></li>')
        return m.group(1) + "\n".join(items) + m.group(3)

    src = footer_pat.sub(repl_footer, src)

    if src != orig:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)

# 3. Sync Section 7 (Other Services) across all *-nc pages
import sync_other_services
