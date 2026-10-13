"""Charlotte sub-service pillar renderer (9-section skeleton, as lot-clearing-charlotte-nc/)."""
from lib import *

ORDER = {"land": ["land", "forestry", "brush"], "forestry": ["forestry", "land", "brush"], "brush": ["brush", "land", "forestry"]}

def render_sub(p, silo_key, built):
    s = SILOS[silo_key]
    slug = f'{p["slug"]}-charlotte-nc'
    name = p["name"]
    url = f"{BASE}/{slug}/"
    title = f"{strip_tags(name)} in Charlotte, NC | Land Clearing Charlotte".replace("&", "&amp;")
    pillar_url = f'{BASE}/{s["pillar"]}/'
    ld = ld_block([
        business("Charlotte"),
        {"@type": "Service", "name": strip_tags(f"{name} in Charlotte, NC"), "serviceType": strip_tags(p.get("service_type", name)),
         "provider": {"@id": f"{BASE}/#business"}, "areaServed": {"@type": "City", "name": "Charlotte"}, "url": url},
        crumbs([("Home", f"{BASE}/"), (f'{s["name"]} in Charlotte, NC', pillar_url), (f"{name} in Charlotte, NC", url)]),
    ])

    lead = "\n".join(f"            <p>{x}</p>" for x in p["lead"])
    checks = "\n".join(f"            <li>{x}</li>" for x in p["checks"])
    trust = trust_bar([
        ("person", "Owner on Every Job", p["trust_sub"][0]),
        ("shield", "Licensed &amp; Insured", p["trust_sub"][1]),
        ("doc", "Free On-Site Estimates", p["trust_sub"][2]),
        tuple(p["trust4"]),
    ])
    towns = "\n".join(f'''          <div class="svc-area-card svc-area-card--proposed" data-href="../{p["slug"]}-{ts}-nc/">
            <span class="svc-area-card__label">Service Area</span>
            <span class="svc-area-card__name">{name} in {tn}, NC</span>
            <span class="svc-area-card__meta">{TOWN_META[ts]}</span>
          </div>''' for ts, tn in TOWNS)
    depth = "\n\n".join(f"            <h3>{h}</h3>\n            <p>{b}</p>" for h, b in p["depth"])
    figs = "\n".join(f'''            <figure class="svc-figure">
              {picture(img, alt)}
              <figcaption>{cap}</figcaption>
            </figure>''' for img, alt, cap in p["figures"])
    co = p["callout"]

    groups = []
    for key in ORDER[silo_key]:
        chips = "\n".join(chip(f"{sl}-charlotte-nc", lbl, current=(key == silo_key and sl == p["slug"]), built=built)
                          for sl, lbl in SUBS[key])
        groups.append(group(key, "Parent Service" if key == silo_key else "Core Service", chips))
    groups = "\n\n".join(groups)

    html = head(title, p["meta"], url, p["hero_img"], ld) + header_for(silo_key) + f'''  <main>
    <!-- 2. HERO -->
    <section class="svc-hero" aria-labelledby="page-title">
      <div class="svc-hero__bg">{picture(p["hero_img"], hero=True)}</div>
      <div class="svc-container svc-hero__inner">
        <div>
          <span class="svc-hero__eyebrow">{p["eyebrow"]}</span>
          <h1 class="svc-hero__title" id="page-title">{name} in <span>Charlotte, NC</span></h1>
          <div class="svc-hero__lead">
{lead}
          </div>
          <div class="svc-hero__actions">
            <a class="svc-btn svc-btn--gold" href="#estimate">Get My Free Estimate</a>
            <a class="svc-btn svc-btn--ghost" href="tel:8285763931">Call (828) 576-3931</a>
          </div>
          <ul class="svc-hero__checks">
{checks}
          </ul>
        </div>

{form_card(p, s["option"])}
      </div>
    </section>

{trust}
    <!-- 4. WHAT OUR PROCESS IS (sub-service: compact) -->
    <section class="svc-section svc-section--tint" aria-labelledby="process-title">
      <div class="svc-container">
        <div class="svc-head">
          <span class="svc-eyebrow">How It Works</span>
          <h2 class="svc-h2" id="process-title">What Our {p.get("process_name", name)} Process Is</h2>
          <p>{p["process_intro"]}</p>
        </div>
        <ol class="svc-steps svc-steps--compact">
{steps_html(p["steps"])}
        </ol>
      </div>
    </section>

    <!-- 5. WHERE WE SERVE (pillar card FIRST, then town pages, proposed until built) -->
    <section class="svc-section svc-section--white" aria-labelledby="areas-title">
      <div class="svc-container">
        <div class="svc-head">
          <span class="svc-eyebrow">Service Area</span>
          <h2 class="svc-h2" id="areas-title">Where We Serve for {p.get("areas_name", name)}</h2>
          <p>{p["areas_intro"]}</p>
        </div>
        <div class="svc-areas">
          <a class="svc-area-card svc-area-card--pillar" href="../{s["pillar"]}/">
            <span class="svc-area-card__label">Main Service Page</span>
            <span class="svc-area-card__name">{s["name"]} in Charlotte, NC</span>
            <span class="svc-area-card__meta">All of Charlotte &amp; Mecklenburg County</span>
          </a>
{towns}
        </div>
      </div>
    </section>

    <!-- 6. CONTINUING COPY (unique to this sub-service, no links in body copy) -->
    <section class="svc-section svc-section--tint" aria-labelledby="depth-title">
      <div class="svc-container">
        <div class="svc-head">
          <span class="svc-eyebrow">{p["depth_eyebrow"]}</span>
          <h2 class="svc-h2" id="depth-title">{p["depth_h2"]}</h2>
        </div>
        <div class="svc-split">
          <div class="svc-prose">
{depth}
          </div>
          <div class="svc-split__media">
{figs}
            <div class="svc-callout">
              <h3>{co[0]}</h3>
              <p>{co[1]}</p>
              <a class="svc-btn svc-btn--gold" href="#estimate">{co[2]}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. OTHER SERVICES IN CHARLOTTE (parent silo first, then the other two) -->
    <section class="svc-section svc-section--white" aria-labelledby="other-title">
      <div class="svc-container">
        <div class="svc-head">
          <span class="svc-eyebrow">Everything We Do in Charlotte</span>
          <h2 class="svc-h2" id="other-title">Other Services We Provide in Charlotte</h2>
          <p>{p["other_intro"]}</p>
        </div>

{groups}
      </div>
    </section>

    <!-- 8. WHY CHOOSE US -->
    <section class="svc-section svc-section--tint" aria-labelledby="why-title">
      <div class="svc-container">
        <div class="svc-head">
          <span class="svc-eyebrow">Why Us</span>
          <h2 class="svc-h2" id="why-title">{p["why_h2"]}</h2>
        </div>
        <div class="svc-reasons">
{reasons_html(p["reasons"])}
        </div>
        <div class="svc-why-copy svc-prose">
          <p>{p["why_copy"]}</p>
        </div>
      </div>
    </section>

    <!-- 9. FAQs (FAQPage schema built from this list by site.js) -->
    <section class="svc-section svc-section--white" aria-labelledby="faq-title">
      <div class="svc-container">
        <div class="svc-head svc-head--center">
          <span class="svc-eyebrow">Questions</span>
          <h2 class="svc-h2" id="faq-title">Charlotte {p.get("faq_name", name)} FAQs</h2>
        </div>
        <div class="svc-faq">
{faq_html(p["faqs"])}
        </div>
      </div>
    </section>

{CLOSING}'''
    write(slug, html)
    return slug, word_count(html)
