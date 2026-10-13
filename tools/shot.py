"""Screenshot helper: python shot.py <url-path> <name> [desktop_h] [mobile_h]
Desktop 1440 wide; mobile 390 via iframe wrapper (headless Chrome can't go below ~500px)."""
import os, sys, subprocess
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = os.path.join(os.path.dirname(__file__), "..", "screenshots")
SITE = r"h:\Websites\landc\charlotte-land-clearing"
os.makedirs(OUT, exist_ok=True)
path, name = sys.argv[1], sys.argv[2]
dh = int(sys.argv[3]) if len(sys.argv) > 3 else 2200
mh = int(sys.argv[4]) if len(sys.argv) > 4 else 2400
url = "http://localhost:8765/" + path.lstrip("/")

def run(target, out, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=15000",
                    f"--screenshot={out}", target], check=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

run(url, os.path.abspath(os.path.join(OUT, f"{name}-1440.png")), 1440, dh)
wrap = os.path.join(SITE, "_shot-wrapper.html")
with open(wrap, "w", encoding="utf-8") as f:
    f.write(f'<!doctype html><html><body style="margin:0;background:#888">'
            f'<iframe src="{url}" style="width:390px;height:{mh}px;border:0;display:block;background:#fff"></iframe></body></html>')
run("http://localhost:8765/_shot-wrapper.html", os.path.abspath(os.path.join(OUT, f"{name}-390.png")), 500, mh)
os.remove(wrap)
print("ok", name)
