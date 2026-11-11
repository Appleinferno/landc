"""Render a Lot Clearing Tips blog article at /lot-clearing-tips/{slug}/index.html."""
import os, json, re, html as html_lib
from lib import ROOT, CLOSING, CSS_VER, IMG_SIZES, picture, SOCIAL_PROFILES
from apply_nav import PARTIAL_PATH
SITE = "https://landclearingcharlotte.com"

EXCLUDED_TOC_HEADINGS = re.compile(r"^(key takeaways|brief overview|overview)\b", re.I)
CORE_SERVICE_HREFS = {
    "../../land-clearing-charlotte-nc/",
    "../../forestry-mulching-charlotte-nc/",
    "../../brush-clearing-charlotte-nc/",
}


def validate_article_links(slug, html):
    m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S)
    assert m, f"{slug}: missing <article>"
    art_no_toc = re.sub(r'<nav class="article-toc"[^>]*>.*?</nav>', "", m.group(1), flags=re.S)
    hrefs = re.findall(r'<a\s+[^>]*href="([^"]+)"', art_no_toc)
    internal = []
    for h in hrefs:
        if h.startswith(("#", "tel:", "mailto:")):
            continue
        if h.startswith(("http://", "https://")) and "landclearingcharlotte.com" not in h:
            continue
        norm = h.split("#")[0].split("?")[0]
        internal.append(norm)
    dups = [u for u in set(internal) if internal.count(u) > 1]
    assert not dups, f"{slug}: duplicate internal links in <article>: {dups}"
    assert len(internal) <= 5, f"{slug}: {len(internal)} internal links exceeds max 5: {internal}"
    assert "../../" in internal, f"{slug}: missing homepage link ('../../') in <article>: {internal}"
    assert set(internal) & CORE_SERVICE_HREFS, (
        f"{slug}: missing core service link in <article>: {internal}"
    )
    return internal


def slugify_heading(text):
    plain = html_lib.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
    return slug or "section"


def header_for_article():
    raw = open(PARTIAL_PATH, encoding="utf-8").read().rstrip()
    nav = (
        raw.replace("{PREFIX}", "../../")
        .replace("{BRAND_HREF}", "../../")
        .replace("{ESTIMATE_HREF}", "../../free-estimate/")
    )
    for cls in ("site-navigation__menu-link--navy-hover", "hf-row"):
        t = f'<a class="{cls}" href="../../lot-clearing-tips/">'
        nav = nav.replace(t, f'<a class="{cls}" href="../../lot-clearing-tips/" aria-current="page">')
    top = open(os.path.join(ROOT, "land-clearing-charlotte-nc", "index.html"), encoding="utf-8").read()
    topbar = top[top.index('  <aside class="site-topbar"'):top.index('  <header class="site-navigation">')]
    topbar = topbar.replace('href="../', 'href="../../').replace('href="#estimate"', 'href="../../free-estimate/"')
    return topbar + nav + "\n"


def closing_for_article(cta_h2):
    c = CLOSING.replace('href="../', 'href="../../').replace('src="../', 'src="../../').replace('srcset="../', 'srcset="../../')
    c = c.replace('href="#estimate"', 'href="../../free-estimate/"')
    c = c.replace('<h2>Ready to clear your Charlotte property?</h2>', f'<h2>{cta_h2}</h2>')
    c = c.replace('<p>Free on-site walk-through and a firm written price.</p>', '<p>Walk your North Carolina property with the owner and get a firm written price.</p>')
    c = c.replace('  </main>\n', '', 1)
    return c


def article_schema(p):
    url = f"{SITE}/lot-clearing-tips/{p['slug']}/"
    graph = [
        {
            "@type": "LocalBusiness",
            "@id": f"{SITE}/#business",
            "name": "Land Clearing Charlotte",
            "url": f"{SITE}/",
            "telephone": "+1-704-741-6895",
            "email": "patrick@landclearingcharlotte.com",
            "openingHours": "Mo-Sa 06:00-18:00",
            "founder": {"@type": "Person", "name": "Patrick Dinehart"},
            "parentOrganization": {"@id": f"{SITE}/#organization"},
            "sameAs": SOCIAL_PROFILES,
        },
        {
            "@type": "Article",
            "headline": p["h1"],
            "description": p["meta_desc"],
            "image": f"{SITE}/images/{p.get('og_img', p['hero_img'])}.jpg",
            "datePublished": p["date_iso"],
            "dateModified": p.get("date_modified", p["date_iso"]),
            "author": {"@id": f"{SITE}/#business"},
            "publisher": {"@id": f"{SITE}/#business"},
            "mainEntityOfPage": url,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Lot Clearing Tips", "item": f"{SITE}/lot-clearing-tips/"},
                {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url},
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)


def render_article(p):
    slug = p["slug"]
    url = f"{SITE}/lot-clearing-tips/{slug}/"
    title = p["title"]
    desc = p["meta_desc"]
    hero_img = p["hero_img"]
    # Social/schema image must be a JPG; AVIF heroes keep a JPG og_img.
    og_img = p.get("og_img", hero_img)

    # First pass: assign H2 IDs for eligible sections (skip Key Takeaways / Brief Overview)
    toc_entries = []
    used_ids = set()
    section_ids = []
    for sec in p["sections"]:
        h2_plain = html_lib.unescape(re.sub(r"<[^>]+>", "", sec["h2"])).strip()
        if EXCLUDED_TOC_HEADINGS.match(h2_plain):
            section_ids.append(None)
        else:
            base_id = slugify_heading(sec["h2"])
            sec_id = base_id
            n = 2
            while sec_id in used_ids:
                sec_id = f"{base_id}-{n}"
                n += 1
            used_ids.add(sec_id)
            section_ids.append(sec_id)
            toc_entries.append((sec_id, sec["h2"]))

    toc_html = ""
    if toc_entries:
        first_id = toc_entries[0][0]
        li_items = "\n".join(
            f'              <li class="article-toc__item"><a class="article-toc__link" href="#{sid}">{stitle}</a></li>'
            for sid, stitle in toc_entries
        )
        toc_html = (
            '          <nav class="article-toc" aria-label="Table of Contents">\n'
            '            <div class="article-toc__header">\n'
            '              <p class="article-toc__title">Table of Contents</p>\n'
            f'              <a class="article-toc__skip" href="#{first_id}">Skip Table of Contents &darr;</a>\n'
            '            </div>\n'
            '            <ol class="article-toc__list">\n'
            f'{li_items}\n'
            '            </ol>\n'
            '          </nav>'
        )

    sections_html = []
    toc_inserted = False
    for sec, sec_id in zip(p["sections"], section_ids):
        if sec_id is not None and not toc_inserted and toc_html:
            sections_html.append(toc_html)
            toc_inserted = True
        if sec_id:
            blocks = [f'            <h2 class="legal-document__clause-title--navy-bold" id="{sec_id}">{sec["h2"]}</h2>']
        else:
            blocks = [f'            <h2 class="legal-document__clause-title--navy-bold">{sec["h2"]}</h2>']
        for item in sec["body"]:
            if item.startswith("<"):
                blocks.append("            " + item)
            else:
                blocks.append(f'            <p class="legal-document__clause-text--slate-regular">{item}</p>')
        sections_html.append(
            '          <section class="legal-document__clause-section">\n'
            + "\n".join(blocks)
            + "\n          </section>"
        )
    body_html = "\n\n".join(sections_html)

    rel_svc = p.get("related_service")
    if rel_svc:
        related_html = f'''          <div style="margin-top: 36px; padding-top: 28px; border-top: 2px solid #EDF2F7;">
            <span class="svc-eyebrow">Related Service</span>
            <div class="svc-areas" style="margin-top: 12px;">
              <a class="svc-area-card svc-area-card--pillar" href="../../{rel_svc['slug']}/">
                <span class="svc-area-card__label">{rel_svc['tag']}</span>
                <span class="svc-area-card__name">{rel_svc['title']}</span>
                <span class="svc-area-card__meta">{rel_svc['meta']}</span>
              </a>
            </div>
          </div>'''
    else:
        related_html = ""

    hero_pic = picture(hero_img, p["hero_alt"], lazy=False).replace('../images/', '../../images/')
    og_w, og_h = IMG_SIZES.get(og_img, (1600, 1200))
    og_alt = p["h1"]

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FQTE2PF67P"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-FQTE2PF67P');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="en_US">
  <meta property="og:site_name" content="Land Clearing Charlotte">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/{og_img}.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="{og_w}">
  <meta property="og:image:height" content="{og_h}">
  <meta property="og:image:alt" content="{og_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@landclearingcha">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/images/{og_img}.jpg">
  <meta name="twitter:image:alt" content="{og_alt}">
  <link rel="icon" href="../../favicon.ico" sizes="48x48">
  <link rel="icon" href="../../images/logo/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../../images/logo/apple-touch-icon.png">
  <link rel="stylesheet" href="../../style.css?v={CSS_VER}">
  <link rel="stylesheet" href="../../service-page.css">
  <script type="application/ld+json">
{article_schema(p)}
  </script>
</head>
<body>
{header_for_article()}
  <main>
    <div class="legal-document">
      <div class="legal-document__body-container">

        <div class="legal-document__hero-zone">
          <span class="legal-document__hero-eyebrow--gold-underline">{p["category"]}</span>
          <h1 class="legal-document__hero-title--navy-clamp" id="page-title">{p["h1"]}</h1>
          <div class="legal-document__hero-meta--slate-small">
            <span>Published {p["date_display"]}</span>
            <span>&bull;</span>
            <span>{p["read_time"]}</span>
            <span>&bull;</span>
            <span>North Carolina Field Guide</span>
          </div>
        </div>

        <article class="legal-document__card-wrapper--elevated-white">

          <figure class="svc-figure" style="margin: 0 0 32px;">
            {hero_pic}
            <figcaption>{p["hero_caption"]}</figcaption>
          </figure>

          <div class="legal-document__callout-box--highlight-gold-border">
            <strong>{p["callout_title"]}</strong>
            <p>{p["callout_text"]}</p>
          </div>

          <div class="svc-price-card" style="margin: 28px 0;" aria-label="Per-Acre Price Guide">
            <span class="svc-price-card__badge">Quick Price Guide</span>
            <strong class="svc-price-card__amount">$2,000 - $8,000 <span>per acre</span></strong>
            <span class="svc-price-card__sub">Typical North Carolina range depending on property conditions. Stump grinding and full stump removal are quoted separately.</span>
            <span class="svc-price-card__label">What Changes the Price:</span>
            <ul class="svc-price-card__list">
              <li><strong>Brush density:</strong> Light saplings vs. thick briars and vines.</li>
              <li><strong>Trees over 8&Prime; thick:</strong> How many larger trees need removal.</li>
              <li><strong>Slope &amp; terrain:</strong> Flat ground vs. steep banks or gullies.</li>
              <li><strong>Rocks &amp; obstacles:</strong> Surface rock, tight access, or structures to work around.</li>
            </ul>
            <a class="svc-price-card__link" href="../../land-clearing-cost-calculator/">Try the Cost Calculator &rarr;</a>
          </div>

{body_html}

{related_html}

        </article>

      </div>
    </div>
  </main>

{closing_for_article(p["cta_h2"])}'''

    validate_article_links(slug, html)

    out_dir = os.path.join(ROOT, "lot-clearing-tips", slug)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return out, html


def article_word_count(html):
    m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S)
    body = m.group(1) if m else html
    text = re.sub(r"<[^>]+>", " ", body)
    return len(text.split())
