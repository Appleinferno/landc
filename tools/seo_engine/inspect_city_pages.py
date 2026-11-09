import os
import re
from bs4 import BeautifulSoup

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
CITIES = ["huntersville-nc", "mint-hill-nc", "waxhaw-nc", "concord-nc", "mooresville-nc", "indian-trail-nc"]
SILOS = ["land-clearing", "forestry-mulching", "brush-clearing"]

for silo in SILOS:
    for city in CITIES:
        slug = f"{silo}-{city}"
        if slug == "land-clearing-huntersville-nc":
            continue
        p = os.path.join(ROOT, slug, "index.html")
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        prose = soup.find("div", class_="svc-prose")
        h3s = [h.get_text(" ", strip=True) for h in prose.find_all("h3")] if prose else []
        paras = [el.get_text(" ", strip=True) for el in prose.find_all("p")] if prose else []
        print(f"=== {slug} ===")
        print("H3s:", h3s)
        print("Last 2 paragraphs:")
        for idx, pt in enumerate(paras[-2:]):
            print(f"  P[-{2-idx}]: {pt[:180]}...")
        faqs = soup.find_all("details", class_="svc-faq__item")
        print(f"FAQs count: {len(faqs)}")
