"""Apply tools/gen/nav_partial.html to pages (preview subset or --all sitewide)."""
import os, re, sys, glob
from lib import ROOT, SILOS, SUBS

PARTIAL_PATH = os.path.join(os.path.dirname(__file__), "nav_partial.html")

def silo_for_folder(folder):
    if folder.startswith("land-clearing-"):
        return "land-clearing-charlotte-nc"
    if folder.startswith("forestry-mulching-"):
        return "forestry-mulching-charlotte-nc"
    if folder.startswith("brush-clearing-"):
        return "brush-clearing-charlotte-nc"
    sub = re.sub(r"-[a-z-]+-nc$", "", folder)
    for k, s in SILOS.items():
        if any(slug == sub for slug, _ in SUBS[k]):
            return s["pillar"]
    return None

def render_nav_for_page(page_path, html):
    raw = open(PARTIAL_PATH, encoding="utf-8").read().rstrip()
    rel = os.path.relpath(page_path, ROOT).replace("\\", "/")
    folder = os.path.dirname(rel)

    if rel == "404.html":
        prefix = "/"
        brand_href = "/"
        est_href = "/#estimate-form"
    elif folder in ("", "."):
        prefix = ""
        brand_href = "./"
        est_href = "#estimate-form"
    elif "/" not in folder:
        prefix = "../"
        brand_href = "../"
        est_href = "#estimate" if 'id="estimate"' in html else "../#estimate-form"
    else:
        prefix = "../../"
        brand_href = "../../"
        est_href = "../../#estimate-form"

    nav = (
        raw.replace("{PREFIX}", prefix)
        .replace("{BRAND_HREF}", brand_href)
        .replace("{ESTIMATE_HREF}", est_href)
    )

    # Set aria-current="page" on matching links
    if folder and folder != ".":
        exact_target = f'href="{prefix}{folder}/"'
        nav = nav.replace(exact_target, exact_target + ' aria-current="page"')

        pillar = silo_for_folder(folder)
        if pillar and pillar != folder:
            top_link = f'<li><a class="site-navigation__menu-link--navy-hover" href="{prefix}{pillar}/">'
            nav = nav.replace(
                top_link,
                f'<li><a class="site-navigation__menu-link--navy-hover" href="{prefix}{pillar}/" aria-current="page">',
                1,
            )
        if folder.startswith("lot-clearing-tips/"):
            for cls in ("site-navigation__menu-link--navy-hover", "site-navigation__mobile-link", "hf-row"):
                t = f'<a class="{cls}" href="{prefix}lot-clearing-tips/">'
                nav = nav.replace(t, f'<a class="{cls}" href="{prefix}lot-clearing-tips/" aria-current="page">')

    return nav, prefix

def apply_to_file(page_path):
    html = open(page_path, encoding="utf-8").read()
    nav, prefix = render_nav_for_page(page_path, html)
    new_html, n = re.subn(
        r'  <header class="site-navigation">.*?</header>',
        nav,
        html,
        count=1,
        flags=re.S,
    )
    assert n == 1, f"header not matched in {page_path}"

    # Remove old inline drawer script on homepage if present
    new_html = re.sub(
        r"\s*<!-- =+\s*INTERACTIVITY: Mobile Drawer.*?</script>",
        "",
        new_html,
        flags=re.S,
    )

    # Ensure site.js is included before </body>
    script_tag = f'<script src="{prefix}site.js"></script>'
    if "site.js" not in new_html:
        new_html = new_html.replace("</body>", f"  {script_tag}\n</body>")

    if new_html != html:
        with open(page_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_html)
        return True
    return False

def main():
    args = sys.argv[1:]
    if not args or "--all" in args:
        pages = sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True))
        pages = [p for p in pages if "_shot" not in p]
        f404 = os.path.join(ROOT, "404.html")
        if os.path.isfile(f404):
            pages.append(f404)
    else:
        pages = []
        for a in args:
            p = os.path.join(ROOT, a)
            if os.path.isdir(p):
                p = os.path.join(p, "index.html")
            pages.append(p)

    count = 0
    for p in pages:
        if apply_to_file(p):
            count += 1
            print("applied nav:", os.path.relpath(p, ROOT))
    print(f"Total updated: {count}")

if __name__ == "__main__":
    main()
