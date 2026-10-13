"""Full-page capture + split: python fullshot.py <url-path> <name> [desk_h] [mob_h]
Saves <name>-1440-full.png, <name>-390-full.png and 1440/390 chunk crops for review."""
import os, sys, subprocess
from PIL import Image
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
SITE = r"h:\Websites\landc\charlotte-land-clearing"
os.makedirs(OUT, exist_ok=True)
path, name = sys.argv[1], sys.argv[2]
dh = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
mh = int(sys.argv[4]) if len(sys.argv) > 4 else 14000
url = "http://localhost:8765/" + path.lstrip("/")

def run(target, out, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=15000",
                    f"--screenshot={out}", target], check=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def trim(fn, skip=0):
    im = Image.open(fn).convert("RGB")
    # trim trailing blank area (identical rows at the bottom)
    w, h = im.size
    px = im.load()
    y = h - 1 - skip
    ref = [px[x, y] for x in range(0, w, 7)]
    while y > 0 and [px[x, y] for x in range(0, w, 7)] == ref:
        y -= 1
    im = im.crop((0, 0, w, min(h, y + 2)))
    im.save(fn)
    return im

d = os.path.join(OUT, f"{name}-1440-full.png")
run(url, d, 1440, dh)
trim(d)
wrap = os.path.join(SITE, "_shot-wrapper.html")
with open(wrap, "w", encoding="utf-8") as f:
    f.write(f'<!doctype html><html><body style="margin:0;background:#fff">'
            f'<iframe src="{url}" style="width:390px;height:{mh}px;border:0;display:block"></iframe></body></html>')
m = os.path.join(OUT, f"{name}-390-full.png")
run("http://localhost:8765/_shot-wrapper.html", m, 500, mh)
os.remove(wrap)
im = Image.open(m).crop((0, 0, 390, mh)); im.save(m); trim(m, 140)
print("ok", name, Image.open(d).size, Image.open(m).size)
