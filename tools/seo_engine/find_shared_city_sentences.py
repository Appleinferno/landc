import os
import re
from bs4 import BeautifulSoup

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
CITIES = ["huntersville-nc", "mint-hill-nc", "waxhaw-nc", "concord-nc", "mooresville-nc", "indian-trail-nc"]
SILOS = ["land-clearing", "forestry-mulching", "brush-clearing"]

sent_pages = {}
for silo in SILOS:
    for city in CITIES:
        slug = f"{silo}-{city}"
        p = os.path.join(ROOT, slug, "index.html")
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        prose = soup.find("div", class_="svc-prose")
        if not prose:
            continue
        city_pretty = city.replace("-nc", "").replace("-", " ").title()
        for idx, para in enumerate(prose.find_all("p")):
            txt = para.get_text(" ", strip=True)
            for s in re.split(r"(?<=[.!?])\s+", txt):
                if len(s) < 40:
                    continue
                norm = re.sub(re.escape(city_pretty), "{CITY}", s, flags=re.IGNORECASE)
                sent_pages.setdefault(norm, []).append((slug, idx))

print("Sentences shared across >=2 pages:")
for norm, locs in sorted(sent_pages.items(), key=lambda x: -len(x[1])):
    if len(locs) >= 2:
        print(f"\n[{len(locs)} pages] {[x[0] for x in locs]}")
        print(f"  Sentence: {norm}")
