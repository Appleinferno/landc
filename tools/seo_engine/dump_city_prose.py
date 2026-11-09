import os
from bs4 import BeautifulSoup

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
CITIES = ["huntersville-nc", "mint-hill-nc", "waxhaw-nc", "concord-nc", "mooresville-nc", "indian-trail-nc"]
SILOS = ["land-clearing", "forestry-mulching", "brush-clearing"]

out_lines = []
for silo in SILOS:
    for city in CITIES:
        slug = f"{silo}-{city}"
        if slug == "land-clearing-huntersville-nc":
            continue
        p = os.path.join(ROOT, slug, "index.html")
        html = open(p, encoding="utf-8").read()
        soup = BeautifulSoup(html, "html.parser")
        prose = soup.find("div", class_="svc-prose")
        out_lines.append(f"============================================================")
        out_lines.append(f"SLUG: {slug}")
        out_lines.append(f"============================================================")
        for el in prose.children:
            if getattr(el, "name", None) in ("h2", "h3", "p", "ul", "div"):
                out_lines.append(str(el))
                out_lines.append("")

with open(r"h:\Websites\landc\tools\seo_engine\data\city_pages_prose_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Dumped 17 city pages prose to city_pages_prose_dump.txt")
