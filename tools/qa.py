"""Site QA: broken internal links, stale proposed items, sitemap sync, canonical/title/H1/phone checks."""
import os, re, glob, json, sys
from urllib.parse import urlparse
ROOT = r"h:\Websites\landc\charlotte-land-clearing"
BASE = "https://landclearingcharlotte.com"
LEGAL = {"privacy-policy", "cookies-policy", "terms-and-conditions"}

pages = sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True))
pages = [p for p in pages if "_shot" not in p]
broken, stale, issues = [], [], []
proposed = set()

def resolve(page, href):
    href = href.split("#")[0].split("?")[0]
    if not href:
        return None
    t = os.path.normpath(os.path.join(os.path.dirname(page), href))
    return t

for p in pages:
    c = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    for attr, h in re.findall(r'(?<![\w-])(href|src|srcset)="([^"]+)"', c):
        if h.startswith(("http", "tel:", "mailto:", "#", "data:")):
            continue
        t = resolve(p, h)
        if t is None:
            continue
        ok = os.path.isfile(t) or os.path.isfile(os.path.join(t, "index.html"))
        if not ok:
            broken.append((rel, h))
    for h in re.findall(r'data-href="([^"]+)"', c):
        t = resolve(p, h)
        proposed.add(os.path.relpath(t, ROOT))
        if os.path.isfile(os.path.join(t, "index.html")):
            stale.append((rel, h))
    # per-page checks
    if len(re.findall(r"<h1[ >]", c)) != 1:
        issues.append((rel, "h1 count"))
    folder = os.path.relpath(os.path.dirname(p), ROOT).replace("\\", "/")
    want = BASE + "/" if folder == "." else f"{BASE}/{folder}/"
    m = re.search(r'rel="canonical" href="([^"]+)"', c)
    if not m or m.group(1) != want:
        issues.append((rel, f"canonical {m.group(1) if m else None}"))
    og = re.search(r'property="og:url" content="([^"]+)"', c)
    if not og or og.group(1) != want:
        issues.append((rel, "og:url"))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.S):
        try:
            json.loads(blk)
        except Exception as e:
            issues.append((rel, f"JSON-LD: {e}"))
    for bad in re.findall(r"\(?\d{3}\)?[ .-]?\d{3}-\d{4}", re.sub(r'placeholder="[^"]*"', "", c)):
        if bad not in ("(828) 576-3931",) and not bad.endswith("576-3931"):
            issues.append((rel, f"phone {bad}"))
    for t in re.findall(r'href="tel:([^"]+)"', c):
        if t != "8285763931":
            issues.append((rel, f"tel {t}"))
    for t in re.findall(r'"telephone":\s*"([^"]+)"', c):
        if t != "+1-828-576-3931":
            issues.append((rel, f"schema tel {t}"))
    title = re.search(r"<title>(.*?)</title>", c, re.S).group(1)
    if folder.endswith("-nc") and not re.match(r".+ in .+, NC \| Land Clearing Charlotte$", title):
        issues.append((rel, f"title {title}"))
    if 'name="description"' not in c:
        issues.append((rel, "no meta description"))

# sitemap
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
folders = set()
for p in pages:
    f = os.path.relpath(os.path.dirname(p), ROOT).replace("\\", "/")
    folders.add(BASE + "/" if f == "." else f"{BASE}/{f}/")
sm_missing = sorted(u for u in folders - set(locs) if not any(l in u for l in LEGAL))
sm_extra = sorted(set(locs) - folders)
sm_legal = [u for u in locs if any(l in u for l in LEGAL)]
dups = [u for u in locs if locs.count(u) > 1]

print(f"pages: {len(pages)} | sitemap urls: {len(locs)} | distinct proposed targets: {len(proposed)}")
print("BROKEN:", len(broken)); [print("  ", b) for b in broken]
print("STALE PROPOSED:", len(stale)); [print("  ", s) for s in stale]
print("SITEMAP missing:", sm_missing, "extra:", sm_extra, "legal listed:", sm_legal, "dups:", set(dups))
print("ISSUES:", len(issues)); [print("  ", i) for i in issues]
