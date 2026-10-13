"""Shared building blocks for Land Clearing Charlotte page generation.
Header, closing CTA band, footer and sticky CTA are copied verbatim from land-clearing-charlotte-nc/index.html."""
import os, re, json

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
BASE = "https://landclearingcharlotte.com"
EMAIL = "patrick@landclearingcharlotte.com"
FORM_ENDPOINT = "https://formcarry.com/s/za8glfgKic_"

_pillar = open(os.path.join(ROOT, "land-clearing-charlotte-nc", "index.html"), encoding="utf-8").read()
_HEADER_RAW = _pillar[_pillar.index('  <aside class="site-topbar"'):_pillar.index('  <main>')]
CLOSING = _pillar[_pillar.index('    <section class="svc-cta"'):]
HEAD_ICONS = re.search(r'(  <link rel="icon" href="\.\./favicon\.ico".*?\n  <link rel="apple-touch-icon"[^>]*>\n)', _pillar, re.S).group(1)

IMG_SIZES = {
    "after-land-clearing": (1600, 1200), "before-land-clearing": (1600, 1200),
    "finished-site-prep": (1600, 900), "forestry-mulcher-active": (1600, 900),
    "full-lot-clearing": (1600, 1200), "work-in-progress": (1600, 900),
}

SILOS = {
    "land": dict(pillar="land-clearing-charlotte-nc", name="Land Clearing", nav="Land Clearing", head="land", option="Land Clearing"),
    "forestry": dict(pillar="forestry-mulching-charlotte-nc", name="Forestry Mulching", nav="Forestry Mulching", head="forestry", option="Forestry Mulching"),
    "brush": dict(pillar="brush-clearing-charlotte-nc", name="Brush Clearing", nav="Brush Clearing", head="brush", option="Brush Clearing"),
}
SUBS = {
    "land": [
        ("lot-clearing", "Residential Lot Clearing"),
        ("acreage-clearing", "Acreage Clearing"),
        ("commercial-land-clearing", "Commercial Land Clearing"),
        ("selective-clearing", "Selective Clearing &amp; Tree Preservation"),
        ("driveway-clearing", "Driveway &amp; Access Road Clearing"),
        ("outbuilding-site-clearing", "Clearing for Pools, Barns &amp; Outbuildings"),
        ("lakefront-lot-clearing", "Lakefront &amp; Shoreline Lot Clearing"),
        ("stump-grinding", "Stump Grinding &amp; Removal"),
    ],
    "forestry": [
        ("underbrush-clearing", "Underbrush Clearing"),
        ("pasture-clearing", "Pasture &amp; Field Reclamation"),
        ("trail-cutting", "Trail Cutting"),
        ("food-plot-clearing", "Hunting Land &amp; Food Plot Clearing"),
        ("right-of-way-clearing", "Right-of-Way &amp; Easement Clearing"),
        ("survey-line-clearing", "Survey Line Clearing"),
        ("woodland-thinning", "Woodland Thinning"),
        ("firebreak-clearing", "Firebreak &amp; Fuel Reduction"),
    ],
    "brush": [
        ("overgrown-lot-cleanup", "Overgrown Lot Cleanup"),
        ("briar-clearing", "Briar &amp; Thicket Clearing"),
        ("fence-line-clearing", "Fence Line &amp; Property Line Clearing"),
        ("retention-pond-clearing", "Retention &amp; Detention Pond Clearing"),
        ("ditch-clearing", "Ditch &amp; Drainage Clearing"),
        ("storm-debris-cleanup", "Storm Debris &amp; Downed Tree Cleanup"),
    ],
}
TOWNS = [("huntersville", "Huntersville"), ("mint-hill", "Mint Hill"), ("waxhaw", "Waxhaw"),
         ("concord", "Concord"), ("mooresville", "Mooresville"), ("indian-trail", "Indian Trail")]
TOWN_META = {
    "huntersville": "North Mecklenburg &middot; Lake Norman", "mint-hill": "East Mecklenburg",
    "waxhaw": "Western Union County", "concord": "Cabarrus County",
    "mooresville": "Iredell County &middot; Lake Norman", "indian-trail": "Union County",
}

def _svg(inner, size=20):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2.2" aria-hidden="true">{inner}</svg>')

ICONS = {
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "shield": '<path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6z"/>',
    "doc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    "leaf": '<path d="M5 21c0-9 6-15 15-16-1 9-7 15-15 16z"/><path d="M5 21l8-8"/>',
    "pin": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "tree": '<path d="M12 2v20M5 9l7-7 7 7"/>',
    "terrain": '<path d="M3 17h18M6 17l3-8 3 5 3-3 3 6"/>',
    "lines": '<path d="M4 12h16M4 6h16M4 18h10"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "path": '<path d="M4 20c4-2 4-6 8-8s4-6 8-8"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 1v4M12 19v4M1 12h4M19 12h4"/>',
    "gate": '<path d="M4 21V5M20 21V5M4 9h16M4 15h16M8 9l8 6"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "drop": '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/>',
    "home": '<path d="M3 17h18M5 17V9l7-5 7 5v8"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "check": '<path d="M4 12l5 5L20 6"/>',
}

def exists(slug):
    return os.path.isfile(os.path.join(ROOT, slug, "index.html"))

def header_for(silo_key):
    nav = SILOS[silo_key]["nav"] if silo_key else None
    h = _HEADER_RAW.replace(' aria-current="page"', "")
    if nav:
        h = h.replace(f'class="site-navigation__menu-link--navy-hover" href="../{SILOS[silo_key]["pillar"]}/">',
                      f'class="site-navigation__menu-link--navy-hover" href="../{SILOS[silo_key]["pillar"]}/" aria-current="page">', 1)
    return h

def picture(img, alt="", lazy=True, hero=False, prefix="../"):
    w, h = IMG_SIZES[img]
    a = ' alt="" aria-hidden="true"' if hero else f' alt="{alt}"'
    l = ' loading="lazy"' if lazy and not hero else ""
    return (f'<picture><source type="image/webp" srcset="{prefix}images/{img}.webp">'
            f'<img src="{prefix}images/{img}.jpg"{a}{l} width="{w}" height="{h}"></picture>')

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")

def ld_block(graph):
    txt = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return "\n".join("  " + l for l in txt.splitlines())

def business(city="Charlotte"):
    return {
        "@type": "LocalBusiness", "@id": f"{BASE}/#business", "name": "Land Clearing Charlotte",
        "url": f"{BASE}/", "telephone": "+1-828-576-3931",
        "address": {"@type": "PostalAddress", "streetAddress": "1930 Camden Rd Ste 238", "addressLocality": "Charlotte",
                    "addressRegion": "NC", "postalCode": "28203", "addressCountry": "US"},
        "openingHours": "Mo-Sa 07:00-18:30",
        "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "North Carolina"}},
    }

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": strip_tags(n), "item": u} for i, (n, u) in enumerate(items, 1)]}

def head(title, meta, url, og_image, ld, extra_css=True, og_type="website"):
    t = title.replace('"', "&quot;")
    css = '  <link rel="stylesheet" href="../style.css">\n' + ('  <link rel="stylesheet" href="../service-page.css">\n' if extra_css else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Land Clearing Charlotte">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{meta}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/images/{og_image}.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{meta}">
  <meta name="twitter:image" content="{BASE}/images/{og_image}.jpg">
{HEAD_ICONS}{css}  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>

'''

def form_card(p, option, city="Charlotte"):
    opts = ["Land Clearing", "Forestry Mulching", "Brush Clearing", "Right-of-Way Clearing", "Not sure yet"]
    o = "\n".join(f'                  <option{" selected" if x == option else ""}>{x}</option>' for x in opts)
    return f'''        <div class="svc-form-card" id="estimate">
          <h2 class="svc-form-card__title">{p["form_title"]}</h2>
          <p class="svc-form-card__sub">{p["form_sub"]}</p>
          <form action="{FORM_ENDPOINT}" method="POST" data-estimate-form>
            <div class="svc-form__grid">
              <div class="svc-form__field">
                <label class="svc-form__label" for="f-name">Full Name</label>
                <input class="svc-form__input" id="f-name" name="name" type="text" autocomplete="name" required>
              </div>
              <div class="svc-form__field">
                <label class="svc-form__label" for="f-phone">Phone</label>
                <input class="svc-form__input" id="f-phone" name="phone" type="tel" autocomplete="tel" required>
              </div>
              <div class="svc-form__field">
                <label class="svc-form__label" for="f-service">Service Needed</label>
                <select class="svc-form__select" id="f-service" name="service">
{o}
                </select>
              </div>
              <div class="svc-form__field">
                <label class="svc-form__label" for="f-size">{p.get("size_label", "Property Size")}</label>
                <select class="svc-form__select" id="f-size" name="size">
                  <option>Under 1 acre</option>
                  <option>1 to 3 acres</option>
                  <option>3 to 10 acres</option>
                  <option>10+ acres</option>
                  <option>Not sure</option>
                </select>
              </div>
              <div class="svc-form__field svc-form__field--full">
                <label class="svc-form__label" for="f-address">Property Address or Area</label>
                <input class="svc-form__input" id="f-address" name="address" type="text" placeholder="Street, neighborhood, or ZIP in {city}">
              </div>
              <div class="svc-form__field svc-form__field--full">
                <label class="svc-form__label" for="f-notes">{p["notes_label"]}</label>
                <textarea class="svc-form__textarea" id="f-notes" name="notes" placeholder="{p["notes_ph"]}"></textarea>
              </div>
            </div>
            <div class="svc-form__hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
            <button class="svc-form__submit" type="submit">Request My Free Estimate</button>
            <p class="svc-form__fine">No obligation. Prefer to talk? Call <a href="tel:8285763931">(828) 576-3931</a>.</p>
          </form>
          <div class="svc-form__success" role="status">
            <h3>Thanks, we've got it.</h3>
            <p>{p["form_success"]}</p>
          </div>
          <div class="svc-form__error" role="alert" hidden>
            <p><strong>Sorry, your request didn't go through.</strong> Please call <a href="tel:8285763931">(828) 576-3931</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
          </div>
        </div>'''

def trust_bar(items):
    li = "\n".join(f'''        <li class="svc-trust__item">
          <span class="svc-trust__icon">{_svg(ICONS[i])}</span>
          <span class="svc-trust__text"><strong>{s}</strong><span>{t}</span></span>
        </li>''' for i, s, t in items)
    return f'''    <!-- 3. TRUST BAR -->
    <!-- TODO: real Google rating. Add rating + review count as the first item once available. -->
    <section class="svc-trust" aria-label="Why customers trust us">
      <ul class="svc-container svc-trust__list">
{li}
      </ul>
    </section>
'''

def steps_html(steps):
    return "\n".join(f'''          <li class="svc-step">
            <span class="svc-step__num">{n:02d}</span>
            <h3 class="svc-step__title">{t}</h3>
            <p class="svc-step__text">{x}</p>
          </li>''' for n, (t, x) in enumerate(steps, 1))

def chip(href_slug, label, current=False, built=None):
    href = f"../{href_slug}/"
    if current:
        return f'            <span class="svc-chip svc-chip--current" aria-current="page">{label}</span>'
    if (built is not None and href_slug in built) or exists(href_slug):
        return f'            <a class="svc-chip" href="{href}">{label}</a>'
    return f'            <div class="svc-chip svc-chip--proposed" data-href="{href}">{label}</div>'

def group(silo_key, tag, chips_html, city="Charlotte", city_slug="charlotte-nc", head_live=True):
    s = SILOS[silo_key]
    core_slug = f'{s["pillar"].rsplit("-charlotte-nc", 1)[0]}-{city_slug}'
    title = f'{s["name"]} in {city}, NC'
    if head_live:
        head = f'''          <a class="svc-group__head svc-group__head--{s["head"]}" href="../{core_slug}/">
            <span class="svc-group__tag">{tag}</span>
            <span class="svc-group__title">{title}</span>
            <span class="svc-group__cta">View service &rarr;</span>
          </a>'''
    else:
        head = f'''          <div class="svc-group__head svc-group__head--{s["head"]} svc-group__head--proposed" data-href="../{core_slug}/">
            <span class="svc-group__tag">{tag}</span>
            <span class="svc-group__title">{title}</span>
          </div>'''
    return f'''        <div class="svc-group">
{head}
          <div class="svc-chips">
{chips_html}
          </div>
        </div>'''

def faq_html(faqs):
    return "\n".join(f'''          <details class="svc-faq__item">
            <summary class="svc-faq__q">{q}</summary>
            <div class="svc-faq__a"><p>{a}</p></div>
          </details>''' for q, a in faqs)

def reasons_html(reasons):
    return "\n".join(f'''          <div class="svc-reason">
            <span class="svc-reason__icon">{_svg(ICONS[i], 22)}</span>
            <h3>{h}</h3>
            <p>{x}</p>
          </div>''' for i, h, x in reasons)

def write(slug, html):
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

def word_count(html):
    body = html[html.index("<main>"):html.index('<section class="svc-cta"')]
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    body = re.sub(r'<div class="svc-form-card".*?</form>', " ", body, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", body).split())
