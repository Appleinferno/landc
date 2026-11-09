"""Phase 3-7 Complete Pilot Engine for LandClearingCharlotte.com.

Generates all 10 required Phase 7 deliverables in `tools/seo_engine/deliverables/` and staging previews in `tools/seo_engine/staging/` without modifying production files (`charlotte-land-clearing/`):
1. 01_complete_url_inventory.md (and JSON)
2. 02_keyword_to_page_map.md
3. 03_serp_competitor_research_packs.md
4. 04_pilot_content_briefs.md
5. 05_proposed_source_code_patches.diff (unified git-style diffs for the 4 pilot pages)
6. 06_before_after_comparison_report.md
7. 07_cannibalisation_report.md
8. 08_fact_check_and_verification_log.md
9. 09_validation_and_qa_results.md
10. 10_implementation_and_measurement_log.md
"""
import os
import re
import json
import difflib
from html import unescape
from datetime import datetime, timezone

ROOT = r"h:\Websites\landc\charlotte-land-clearing"
ENGINE_DIR = r"h:\Websites\landc\tools\seo_engine"
DATA_DIR = os.path.join(ENGINE_DIR, "data")
DELIV_DIR = os.path.join(ENGINE_DIR, "deliverables")
STAGING_DIR = os.path.join(ENGINE_DIR, "staging")

os.makedirs(DELIV_DIR, exist_ok=True)
os.makedirs(STAGING_DIR, exist_ok=True)


def extract_faqs_for_schema(html: str) -> list:
    items = re.findall(
        r'<details class="svc-faq__item">\s*<summary class="svc-faq__q">(.*?)</summary>\s*<div class="svc-faq__a">(.*?)</div>\s*</details>',
        html,
        re.S,
    )
    faq_entities = []
    for q_raw, a_raw in items:
        q = unescape(re.sub(r"<[^>]+>", "", q_raw).strip())
        a = unescape(re.sub(r"<[^>]+>", " ", a_raw).strip())
        a = re.sub(r"\s+", " ", a)
        faq_entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    return faq_entities


def inject_faq_schema(html: str, city_override: str = None) -> str:
    m = re.search(r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', html, re.S)
    if not m:
        return html
    prefix, raw_json, suffix = m.groups()
    data = json.loads(raw_json)
    graph = data.get("@graph", [])

    # Update LocalBusiness areaServed on city pages if specified
    if city_override:
        for node in graph:
            if node.get("@type") == "LocalBusiness":
                node["areaServed"] = [
                    {"@type": "City", "name": "Charlotte", "containedInPlace": {"@type": "State", "name": "North Carolina"}},
                    {"@type": "City", "name": city_override, "containedInPlace": {"@type": "State", "name": "North Carolina"}},
                ]

    # Remove existing FAQPage if any, then append fresh FAQPage matching visible FAQs
    graph = [n for n in graph if n.get("@type") != "FAQPage"]
    faq_entities = extract_faqs_for_schema(html)
    if faq_entities:
        graph.append({"@type": "FAQPage", "mainEntity": faq_entities})
    data["@graph"] = graph

    formatted = "\n".join("  " + line for line in json.dumps(data, indent=2, ensure_ascii=False).splitlines())
    return html[: m.start()] + f'  <script type="application/ld+json">\n{formatted}\n  </script>' + html[m.end() :]


def build_proposed_pilot_pages() -> dict:
    results = {}

    # =========================================================================
    # PILOT 1: /land-clearing-charlotte-nc/
    # =========================================================================
    p1_orig_path = os.path.join(ROOT, "land-clearing-charlotte-nc", "index.html")
    p1_orig = open(p1_orig_path, encoding="utf-8").read()
    p1_new = p1_orig

    # 1a. Enrich Continuing Copy (Section 6) on /land-clearing-charlotte-nc/
    p1_target_prose = """            <h3>Charlotte Soils, Slopes &amp; Erosion</h3>
            <p>Charlotte sits on Piedmont red clay. Once the vegetation is gone, that clay sheds water fast and washes into streets, storm drains, and creeks. We use tracked machines with low ground pressure, avoid working soaked ground, and where it makes sense we leave a mulch layer or vegetated buffer to hold the soil until your next phase starts.</p>

            <h3>Permits &amp; Rules to Know Before You Clear</h3>
            <p>North Carolina requires an approved erosion and sedimentation control plan for most land-disturbing projects over one acre, and Charlotte and Mecklenburg County enforce it locally. Charlotte's tree ordinance mainly applies to commercial and new development projects, and trees in the public right-of-way belong to the city. Creeks are protected by stream buffer rules. We'll point out anything on your property that may need a permit or approval before clearing begins, but always confirm the requirements with the city or county for your specific parcel.</p>

            <h3>What Affects the Cost of Land Clearing in Charlotte</h3>
            <ul>
              <li><strong>Size of the area:</strong> square footage or acreage being cleared.</li>
              <li><strong>Vegetation density:</strong> light brush and saplings versus mature, dense woods.</li>
              <li><strong>Tree size:</strong> larger trees take more time and handling.</li>
              <li><strong>Finish level:</strong> mulched in place, cleared to grade, or stumps removed.</li>
              <li><strong>Access and slope:</strong> tight infill lots and steep ground slow production.</li>
              <li><strong>Keeper trees and buffers:</strong> selective work is more careful work.</li>
            </ul>
            <p>Because every property is different, we price after we've walked it. That's how you get a number you can hold us to.</p>"""

    p1_replacement_prose = """            <h3>Choosing the Right Clearing Method for Your Charlotte Parcel</h3>
            <p>Not every property in Mecklenburg County needs the same machine or finish. Matching the method to what happens next on the ground keeps your budget in check and prevents rework for your builder or grading contractor:</p>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Clearing Method</th>
                    <th scope="col">Best For</th>
                    <th scope="col">Stump &amp; Root Handling</th>
                    <th scope="col">Surface Finish</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Forestry Mulching in Place</strong></td>
                    <td>Wooded buffers, underbrush, trails, pastures &amp; lot perimeters (trees under 8&Prime; diameter)</td>
                    <td>Feeder roots and low-cut stumps stay in the ground to hold soil</td>
                    <td>Shredded hardwood/pine mulch blanket; zero burn piles or haul-off</td>
                  </tr>
                  <tr>
                    <td><strong>Full Clearing &amp; Stump Removal</strong></td>
                    <td>House footprints, foundations, driveways, pools &amp; outbuilding pads (including trees 8&Prime;+ wide)</td>
                    <td>Stumps and root balls excavated with our excavator so ground will not settle</td>
                    <td>Bare mineral soil ready for your grading contractor (haul-off available)</td>
                  </tr>
                  <tr>
                    <td><strong>Selective Clearing &amp; Tree Save</strong></td>
                    <td>Custom home lots &amp; infill parcels keeping mature oaks, hickories, and poplars</td>
                    <td>Mulching outside Critical Root Zones (CRZs); full removal only inside build envelope</td>
                    <td>Protected canopy perimeter with a clean, builder-ready home site</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p>We do not perform finish grading or house-pad dirt work, apply herbicides, or offer invasive-vine eradication programs. Instead, <strong>Land Clearing Charlotte</strong> focuses strictly on mechanical clearing, forestry mulching, and stump removal so we can hand a clean, accurately cleared site directly to your grading contractor or builder.</p>

            <h3>Charlotte Piedmont Red Clay, Slopes &amp; Drainage</h3>
            <p>Most Charlotte parcels sit on Cecil and Pacolet series Piedmont Ultisols—heavy red clay subsoils beneath a thin topsoil layer. How that soil behaves after clearing depends on compaction, slope gradient, soil saturation, and surface cover. When heavy wheeled machines rut wet clay or strip vegetation down to bare mineral soil on a slope, stormwater runoff accelerates and can wash sediment toward streets, storm drains, and creeks. We run low-ground-pressure tracked loaders and excavators, pause operations when ground is saturated, and leave a shredded mulch blanket outside structural footprints to help slow surface runoff until your grader installs silt fencing or seed.</p>

            <h3>Charlotte &amp; Mecklenburg County Permits, Tree Save &amp; Stream Buffers</h3>
            <p>Regulatory requirements in Charlotte depend on your parcel's zoning, watershed, and total disturbed area:</p>
            <ul>
              <li><strong>One-Acre Erosion &amp; Sedimentation Control Threshold:</strong> Under the <strong>North Carolina Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong>, administered locally by the City of Charlotte and <strong>Mecklenburg County Land Use &amp; Environmental Services Agency (LUESA)</strong>, any land-disturbing activity of <strong>one acre or more</strong>—including disturbance under one acre if the lot is part of a larger common plan of development exceeding one acre cumulatively—requires an approved Erosion and Sedimentation Control Plan before ground disturbance begins.</li>
              <li><strong>City of Charlotte Unified Development Ordinance (UDO) Tree Protection:</strong> Articles 20 and 40 of the Charlotte UDO govern Heritage Trees, specimen tree save, green areas, and street trees on commercial sites, subdivisions, and regulated infill development, and any tree in the public right-of-way is regulated by the City of Charlotte Urban Forestry program.</li>
              <li><strong>S.W.I.M. &amp; Post-Construction Stream Buffers:</strong> Creeks and tributaries draining to the Catawba River, Lake Norman, Mountain Island Lake, Lake Wylie, McAlpine Creek, and Sugar Creek are protected by Mecklenburg County Surface Water Improvement and Management (S.W.I.M.) and Post-Construction Stormwater buffer widths (typically 30 to 200 feet depending on drainage area and watershed overlay).</li>
              <li><strong>NC 811 Utility Locate Before Digging:</strong> When stump excavation or root grubbing is part of your scope, North Carolina law requires a free utility locate ticket through <strong>NC 811</strong> at least three full business days before excavation starts.</li>
            </ul>
            <p>During our walk-through, owner Patrick Dinehart flags visible buffer edges, easements, and keeper trees with you, and we always recommend verifying parcel-specific permit requirements with the City of Charlotte or Mecklenburg County before clearing begins.</p>

            <h3>2026 Land Clearing Cost Guide in Charlotte ($2,000 - $8,000 Per Acre)</h3>
            <p>Full-acreage land clearing in Charlotte typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. For smaller residential lots under an acre or narrow driveway corridors, we don't penalize homeowners with a rigid per-acre formula—instead, we look at how easy it is to access the work area (we need no minimum pre-cleared pass width because we can work ourselves a path in), travel distance, and how many hills, rocks, or tight obstacles take extra care to work around.</p>
            <ul>
              <li><strong>Brush &amp; understory density:</strong> Open woods with light saplings clear much faster than head-high briars, privet, and tangled vines.</li>
              <li><strong>Trees 8 inches or wider:</strong> While brush and smaller saplings are mulched in place, trees 8 inches or wider take a different approach—and when a job involves significant tree removal, we can bring in our excavator and haul off the trees if needed.</li>
              <li><strong>Steep banks &amp; hilly terrain:</strong> Ravines, creek banks, and sloped lots require slower, deliberate tracked passes.</li>
              <li><strong>Rocks &amp; site obstacles:</strong> Surface rock outcrops, tight infill property lines, fences, and flagged keeper trees require careful maneuvering around obstacles.</li>
              <li><strong>Stump finish:</strong> You can choose <strong>full stump removal</strong> (essential under house pads, footings, and driveways) or <strong>grinding stumps down and leaving the remains</strong> as a surface cover where site conditions allow.</li>
            </ul>"""

    assert p1_target_prose in p1_new, "p1_target_prose not found"
    p1_new = p1_new.replace(p1_target_prose, p1_replacement_prose, 1)

    # 1b. Update FAQ #1 & #2 on /land-clearing-charlotte-nc/ to include exact $2,000-$8,000 price and statutory citations
    p1_faq_target = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does land clearing cost in Charlotte, NC?</summary>
            <div class="svc-faq__a"><p>It depends on the size of the area, how dense the vegetation is, the size of the trees, access, slope, and the finish you need. A lightly wooded backyard costs far less per square foot than dense hardwoods on a slope. We give a firm written price after a free on-site walk-through.</p></div>
          </details>
          <details class="svc-faq__item">
            <summary class="svc-faq__q">Do I need a permit to clear land in Charlotte?</summary>
            <div class="svc-faq__a"><p>Projects that disturb more than one acre generally need an approved erosion and sedimentation control plan. Commercial and new development projects may also fall under Charlotte's tree ordinance, and work near creeks is limited by stream buffer rules. We'll flag what we see on your property, but confirm the requirements for your parcel with the city or county.</p></div>
          </details>"""

    p1_faq_replacement = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does land clearing cost in Charlotte, NC?</summary>
            <div class="svc-faq__a"><p>Land clearing in Charlotte typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four main site factors shape the quote: thick brush density, the number of trees 8 inches or wider (where we can bring in our excavator and haul off trees if needed), steep banks or hilly terrain, and rocks or tight obstacles to work around. Smaller residential lots under an acre are priced fairly by access, travel distance, and obstacles after a free on-site walk-through.</p></div>
          </details>
          <details class="svc-faq__item">
            <summary class="svc-faq__q">Do I need a permit to clear land in Charlotte?</summary>
            <div class="svc-faq__a"><p>Under North Carolina's Sedimentation Pollution Control Act (G.S. 113A-57), disturbing one acre or more—or clearing a smaller lot that is part of a larger common plan of development exceeding one acre—requires an approved Erosion and Sedimentation Control Plan through the City of Charlotte or Mecklenburg County LUESA. Commercial sites and regulated developments must also comply with the City of Charlotte Unified Development Ordinance (UDO) tree-save and Heritage Tree rules, and work near creeks is restricted by S.W.I.M. and watershed stream buffers. Always verify parcel-specific rules with the city or county before starting.</p></div>
          </details>"""

    assert p1_faq_target in p1_new, "p1_faq_target not found"
    p1_new = p1_new.replace(p1_faq_target, p1_faq_replacement, 1)
    p1_new = inject_faq_schema(p1_new)
    results["/land-clearing-charlotte-nc/"] = (p1_orig, p1_new, p1_orig_path)

    # =========================================================================
    # PILOT 2: /forestry-mulching-charlotte-nc/
    # =========================================================================
    p2_orig_path = os.path.join(ROOT, "forestry-mulching-charlotte-nc", "index.html")
    p2_orig = open(p2_orig_path, encoding="utf-8").read()
    p2_new = p2_orig

    p2_target_prose = """            <h3>No Burn Piles, No Haul-Off</h3>
            <p>Open burning of land-clearing debris is heavily restricted in Mecklenburg County, and hauling it away means truck fees and dump fees. Mulching skips both. The material stays on your property as a natural ground cover that breaks down over time and feeds the soil.</p>

            <h3>Better for Red Clay and Slopes</h3>
            <p>Bulldozing scrapes away topsoil and pulls up root systems, which leaves Charlotte's red clay bare and ready to wash out with the next storm. Mulching leaves the roots in the ground and lays a protective blanket over the surface, so soil stays put and erosion is far less of a concern, especially on sloped lots and near creeks.</p>"""

    p2_replacement_prose = """            <h3>No Burn Piles &amp; Mecklenburg County Air Quality Rules</h3>
            <p>Under the <strong>Mecklenburg County Air Pollution Control Ordinance</strong> enforced by <strong>Mecklenburg County Land Use &amp; Environmental Services Agency (LUESA) Air Quality</strong>, open burning of land-clearing debris and brush is strictly prohibited inside Charlotte and Mecklenburg County (with narrow agricultural exceptions requiring permits outside municipal limits). Traditional dozer clearing therefore forces you to pay dump-truck hauling and landfill tipping fees. Forestry mulching eliminates both: brush and saplings under 8 inches are shredded on the spot into a knit ground-cover mulch layer, leaving zero burn piles or windrows behind.</p>

            <h3>How Mulching Protects Piedmont Red Clay &amp; Mature Tree Root Zones</h3>
            <p>Bulldozing scrapes away topsoil and rips up feeder roots, exposing Charlotte's Cecil and Pacolet red clay subsoils to raindrop impact and sheet runoff. Forestry mulching leaves the soil profile intact and spreads shredded wood fibers across the surface, which helps slow surface runoff on moderate slopes while operating low-ground-pressure tracked equipment outside the Critical Root Zones (CRZs) of flagged keeper oaks, hickories, and poplars. Steep banks, concentrated drainage channels, or land disturbance reaching one acre or more under <strong>NC G.S. 113A-57</strong> may still require dedicated erosion controls or county verification, and Mecklenburg County S.W.I.M. stream buffer rules still restrict cutting inside protected creek corridors.</p>"""

    assert p2_target_prose in p2_new, "p2_target_prose not found"
    p2_new = p2_new.replace(p2_target_prose, p2_replacement_prose, 1)

    p2_target_cost = """            <h3>When Mulching Isn't the Right Fit</h3>
            <p>Mulching leaves stumps at or near ground level and a layer of mulch on the surface. That's ideal for woods, fields, trails, and corridors, but a house foundation, driveway base, or graded building pad usually needs the stumps removed and the soil prepared differently. If that's your goal, we'll tell you upfront and recommend a land clearing approach instead.</p>

            <h3>What Affects the Cost of Forestry Mulching</h3>
            <ul>
              <li><strong>Acreage:</strong> mulching is usually priced by the area covered.</li>
              <li><strong>Density:</strong> light brush moves quickly; thick thickets and vines take longer.</li>
              <li><strong>Tree size:</strong> how large the trees are that you want removed.</li>
              <li><strong>Terrain:</strong> steep, rocky, or wet ground slows production.</li>
              <li><strong>Selectivity:</strong> working carefully around many keeper trees adds time.</li>
            </ul>"""

    p2_replacement_cost = """            <h3>Forestry Mulching vs. Dozer Clearing vs. Bush Hogging</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Method</th>
                    <th scope="col">Target Vegetation</th>
                    <th scope="col">Soil &amp; Root Impact</th>
                    <th scope="col">Debris &amp; Aftermath</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Forestry Mulching</strong></td>
                    <td>Thick briars, privet, vines, saplings &amp; trees up to ~6&ndash;8&Prime; diameter</td>
                    <td>Minimal disturbance; feeder roots stay in place under a 2&ndash;4&Prime; mulch blanket</td>
                    <td>No brush piles, no burning, no dump trucks; walkable immediately</td>
                  </tr>
                  <tr>
                    <td><strong>Excavator &amp; Full Clearing</strong></td>
                    <td>Trees 8&Prime; or wider &amp; structural footprints (home pads, driveways, pools)</td>
                    <td>Excavates stumps and root balls so foundations and slabs will not settle</td>
                    <td>Bare soil ready for your grading contractor; log/debris haul-off available</td>
                  </tr>
                  <tr>
                    <td><strong>Tractor Bush Hogging</strong></td>
                    <td>Tall pasture grass, weeds, and light 1&ndash;2&Prime; field sprouts on open ground</td>
                    <td>Surface mowing only; cannot safely process dense woods or larger saplings</td>
                    <td>Rough-cut stalks left on pasture surface for routine mowing upkeep</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>When Mulching Isn't the Right Fit (And How We Handle Trees 8&Prime;+)</h3>
            <p>Forestry mulching grinds stumps flush to grade and leaves roots in the soil. That is ideal for wooded backyards, trails, pastures, and easements, but a house foundation, concrete driveway, or building pad requires full stump and root removal so decomposing wood does not cause settlement. In addition, while brush and saplings under 8 inches are mulched in place, <strong>trees 8 inches or wider get a different approach</strong>—when your project involves significant tree removal, <strong>Land Clearing Charlotte</strong> can bring in our excavator and haul off the trees if needed, leaving the pad ready for your grading contractor.</p>

            <h3>2026 Forestry Mulching Cost in Charlotte ($2,000 - $8,000 Per Acre)</h3>
            <p>Forestry mulching in Charlotte typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. For smaller residential lots under an acre or narrow trail and fence corridors, we price warmly and fairly based on equipment access (no minimum pass width is required—we can mulch our own path in), travel distance, and how many hills, rocks, or tight obstacles around keeper trees take extra time:</p>
            <ul>
              <li><strong>Brush &amp; thicket density:</strong> Light understory under mature oaks moves faster than impenetrable Chinese privet, autumn olive, and briar thickets.</li>
              <li><strong>Trees over 8 inches thick:</strong> An 8-inch diameter is our pricing benchmark where heavier stems or excavator tree removal and haul-off change the scope.</li>
              <li><strong>Slope &amp; terrain:</strong> Steep ravines, creek banks, and gullies slow machine travel compared to level ground.</li>
              <li><strong>Rocks &amp; selective obstacles:</strong> Navigating around surface boulders, septic repair areas, fences, and closely spaced keeper trees requires slower, careful passes.</li>
            </ul>"""

    assert p2_target_cost in p2_new, "p2_target_cost not found"
    p2_new = p2_new.replace(p2_target_cost, p2_replacement_cost, 1)

    p2_faq_target = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does forestry mulching cost in Charlotte?</summary>
            <div class="svc-faq__a"><p>Mulching is usually priced by the acre or by the area, adjusted for vegetation density, tree size, terrain, and how selective the work needs to be. We give a firm written price after walking the property with you.</p></div>
          </details>
          <details class="svc-faq__item">
            <summary class="svc-faq__q">What size trees can a forestry mulcher handle?</summary>
            <div class="svc-faq__a"><p>Mulchers are built for brush, saplings, and small to mid-size trees. Very large trees are usually handled differently. During the walk-through we'll tell you exactly what can be mulched and what can't.</p></div>
          </details>"""

    p2_faq_replacement = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does forestry mulching cost in Charlotte?</summary>
            <div class="svc-faq__a"><p>Forestry mulching in Charlotte typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Pricing depends on brush density, how many trees 8 inches or wider require removal, steep banks or hilly terrain, and rocks or tight obstacles around keeper trees. Smaller residential lots under an acre are priced fairly by access, travel distance, and site obstacles after a free on-site walk-through.</p></div>
          </details>
          <details class="svc-faq__item">
            <summary class="svc-faq__q">What size trees can a forestry mulcher handle, and what about trees 8&Prime; or wider?</summary>
            <div class="svc-faq__a"><p>Forestry mulchers efficiently shred brush, vines, saplings, and trees under 8 inches in diameter in place. Trees 8 inches or wider take a different approach and shift the quote—when a job involves significant larger tree removal, we can bring in our excavator and haul off the trees if needed.</p></div>
          </details>"""

    assert p2_faq_target in p2_new, "p2_faq_target not found"
    p2_new = p2_new.replace(p2_faq_target, p2_faq_replacement, 1)
    p2_new = inject_faq_schema(p2_new)
    results["/forestry-mulching-charlotte-nc/"] = (p2_orig, p2_new, p2_orig_path)

    # =========================================================================
    # PILOT 3: /brush-clearing-charlotte-nc/
    # =========================================================================
    p3_orig_path = os.path.join(ROOT, "brush-clearing-charlotte-nc", "index.html")
    p3_orig = open(p3_orig_path, encoding="utf-8").read()
    p3_new = p3_orig

    p3_target_prose = """            <h3>Keeping Brush From Coming Back</h3>
            <p>Brush in the Charlotte area grows back fast, especially privet and sweetgum that resprout from the stump. Regular mowing after we clear is the simplest way to keep it in check. For larger areas, a once-a-year or every-other-year cutback is often cheaper than letting it go and paying for a full clearing again. We'll recommend a schedule that fits your property and budget.</p>

            <h3>What Affects the Cost of Brush Clearing in Charlotte</h3>
            <ul>
              <li><strong>Area size:</strong> square footage or acreage being cleared.</li>
              <li><strong>Brush density and height:</strong> waist-high weeds versus head-high privet and saplings.</li>
              <li><strong>Sapling size:</strong> larger stems take more time to grind.</li>
              <li><strong>Hidden debris:</strong> old fencing, tires, or dumped material slow the job.</li>
              <li><strong>Access and slope:</strong> pond banks, ditches, and gated backyards need smaller equipment.</li>
              <li><strong>Hand work:</strong> detail work around fences, sheds, and keeper trees.</li>
            </ul>
            <p>We price after seeing the property, so the number you get is the number you pay.</p>"""

    p3_replacement_prose = """            <h3>Matching the Right Brush Clearing Method to Your Property</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Site Condition</th>
                    <th scope="col">Our Mechanical Method</th>
                    <th scope="col">Finished Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Open Overgrown Lots &amp; Wooded Thickets</strong></td>
                    <td>Tracked rotary drum mulcher (no minimum pass width needed; we cut our own path in)</td>
                    <td>Briars, privet, and saplings shredded into a flat, walkable mulch layer</td>
                  </tr>
                  <tr>
                    <td><strong>Fence Lines, Sheds &amp; Keeper Tree Edges</strong></td>
                    <td>Tracked mulcher up to the buffer zone + careful hand-clearing right along wire/wood fences</td>
                    <td>Clean inspection and fence-replacement lane without machine damage to posts</td>
                  </tr>
                  <tr>
                    <td><strong>Heavy Saplings &amp; Trees 8&Prime; or Wider</strong></td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Larger trunks removed cleanly so the lot is ready for fencing, mowing, or building</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Pre-Work Checklist: Utilities, Buffers &amp; Code Notices</h3>
            <p>Before any brush clearing begins in Charlotte, we walk through four practical checks with you:</p>
            <ul>
              <li><strong>City of Charlotte Code Enforcement Notices:</strong> If you received a nuisance or overgrown-lot notice from City of Charlotte Code Enforcement (Housing &amp; Neighborhood Services), share the compliance deadline when you call so we can confirm scheduling and provide before-and-after photo documentation.</li>
              <li><strong>Mecklenburg County S.W.I.M. &amp; Stormwater Rules:</strong> Clearing along creeks is restricted by Mecklenburg County LUESA S.W.I.M. and watershed stream buffers, and woody brush removal on HOA detention/retention pond embankments should follow your community's recorded <strong>Charlotte-Mecklenburg Storm Water Services</strong> maintenance agreement.</li>
              <li><strong>Open-Burning Prohibition:</strong> Mecklenburg County Air Quality regulations prohibit open burning of brush and land-clearing debris in Charlotte, making on-site mechanical mulching the cleanest, compliant alternative.</li>
              <li><strong>Survey Lines &amp; NC 811:</strong> Equipment operates strictly inside your verified property boundaries, and any stump excavation requires an <strong>NC 811</strong> utility locate ticket beforehand.</li>
            </ul>

            <h3>Keeping Brush From Coming Back (Mechanical Upkeep Only)</h3>
            <p>Piedmont brush—especially Chinese privet, sweetgum sprouts, and blackberry briars—resprouts vigorously during the growing season. Because <strong>Land Clearing Charlotte</strong> performs strictly mechanical clearing and never applies herbicides or chemical treatments, we cut stems down to a smooth, low mulch bed so you can maintain the area with a regular lawn mower, string trimmer, or annual rotary-cutter pass before woody stems harden again.</p>

            <h3>2026 Brush Clearing Cost in Charlotte ($2,000 - $8,000 Per Acre)</h3>
            <p>Full-acreage brush clearing in Charlotte typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. For smaller residential backyards, vacant infill lots, or narrow fence corridors, we don't apply a rigid acreage minimum—instead, we price kindly and fairly based on how easy it is to access the work area, travel distance, and how many hills, rocks, old wire fences, or tight obstacles take extra time to work around:</p>
            <ul>
              <li><strong>Brush density &amp; height:</strong> Waist-high brambles clear much faster than ten-foot privet and sweetgum thickets.</li>
              <li><strong>Trees 8 inches or wider:</strong> Saplings and brush under 8 inches are mulched in place, while trees 8 inches or wider take a different approach (we can bring in our excavator and haul off larger trees when needed).</li>
              <li><strong>Steep banks &amp; pond slopes:</strong> Ditch banks, detention pond embankments, and gullies require slower, careful passes on tracks.</li>
              <li><strong>Rocks, hidden wire &amp; hand work:</strong> Surface rock, buried wire fencing, and hand-trimming along existing fences or structures add detail time.</li>
            </ul>"""

    assert p3_target_prose in p3_new, "p3_target_prose not found"
    p3_new = p3_new.replace(p3_target_prose, p3_replacement_prose, 1)

    p3_faq_target = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does brush clearing cost in Charlotte?</summary>
            <div class="svc-faq__a"><p>Cost depends on the size of the area, how thick and tall the brush is, the size of any saplings, access, and how much hand work is needed around fences and trees. We give a firm written price after a free walk-through.</p></div>
          </details>"""

    p3_faq_replacement = """          <details class="svc-faq__item">
            <summary class="svc-faq__q">How much does brush clearing cost in Charlotte?</summary>
            <div class="svc-faq__a"><p>Brush clearing in Charlotte typically costs <strong>$2,000 to $8,000 per acre</strong> for full-acreage work depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four main factors drive the price: brush density, the number of trees 8 inches or wider (where we can bring our excavator and haul off trees if needed), steep banks or slopes, and rocks, hidden wire, or fence-line obstacles. Smaller residential lots and fence corridors are priced fairly by access, travel distance, and obstacles after a free walk-through.</p></div>
          </details>"""

    assert p3_faq_target in p3_new, "p3_faq_target not found"
    p3_new = p3_new.replace(p3_faq_target, p3_faq_replacement, 1)
    p3_new = inject_faq_schema(p3_new)
    results["/brush-clearing-charlotte-nc/"] = (p3_orig, p3_new, p3_orig_path)

    # =========================================================================
    # PILOT 4: /land-clearing-huntersville-nc/
    # =========================================================================
    p4_orig_path = os.path.join(ROOT, "land-clearing-huntersville-nc", "index.html")
    p4_orig = open(p4_orig_path, encoding="utf-8").read()
    p4_new = p4_orig

    p4_target_prose = """            <h3>Huntersville Land Clearing Costs &amp; Red Clay Care</h3>
            <p>Land clearing in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong>, depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four site factors move a quote toward the lower or upper end of that range: thick brush density, the amount of tree removal involving trees thicker than 8 inches (a pricing factor rather than an equipment cutoff), steep banks or hilly terrain, and rocks that equipment must navigate around. North Mecklenburg red clay also gets slick after rain, so we run low-ground-pressure tracked equipment and wait out saturated ground rather than rutting your lot.</p>"""

    p4_replacement_prose = """            <h3>Huntersville Clearing Methods: On-Site Mulching vs. Pad &amp; Driveway Excavation</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Huntersville Project Area</th>
                    <th scope="col">Recommended Method</th>
                    <th scope="col">Regulatory &amp; Soil Considerations</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Home Pad, Foundation &amp; Driveway</strong> (Gilead Rd, Hambright Rd, Verhoeff Dr)</td>
                    <td>Full tree clearing + excavator stump removal (haul-off available for trees 8&Prime;+)</td>
                    <td>Leaves bare mineral soil ready for your grading contractor; call NC 811 3 business days before digging</td>
                  </tr>
                  <tr>
                    <td><strong>Wooded Acreage, Trails &amp; Tree-Save Buffers</strong> (Beatties Ford Rd, Bud Henderson Rd, Rural Transitional)</td>
                    <td>Tracked forestry mulching in place (no minimum pass width required)</td>
                    <td>Protects Critical Root Zones (CRZs) under Town of Huntersville Zoning Ordinance Article 7</td>
                  </tr>
                  <tr>
                    <td><strong>Lake Norman &amp; Mountain Island Lake Slopes</strong> (Coves &amp; McDowell Creek tributaries)</td>
                    <td>Selective low-ground-pressure mulching outside protected buffer lines</td>
                    <td>Respects Duke Energy Lake Services 760-ft contour + 50-ft shoreline buffer &amp; Mecklenburg LUESA S.W.I.M. buffers</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Huntersville Land Clearing Costs ($2,000 - $8,000 Per Acre) &amp; Small-Lot Pricing</h3>
            <p>Full-acreage land clearing in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. For smaller Huntersville infill lots under an acre, backyard pool/outbuilding footprints, or driveway corridors, we don't force a rigid per-acre minimum—instead, we price fairly based on equipment access (we need no minimum pre-cleared pass width because we can work ourselves a path in), travel distance up I-77, and how many hills, rocks, or careful obstacles around keeper trees take extra time. Four main factors shape every quote: thick brush density, the number of trees 8 inches or wider (where we can bring in our excavator and haul off the trees if needed), steep banks or gullies, and surface rock outcrops common on ridges near Mountain Island Lake.</p>"""

    assert p4_target_prose in p4_new, "p4_target_prose not found"
    p4_new = p4_new.replace(p4_target_prose, p4_replacement_prose, 1)
    p4_new = inject_faq_schema(p4_new, city_override="Huntersville")
    results["/land-clearing-huntersville-nc/"] = (p4_orig, p4_new, p4_orig_path)

    return results


def main():
    inv_data = json.load(open(os.path.join(DATA_DIR, "master_url_inventory.json"), encoding="utf-8"))
    dry_plan = json.load(open(os.path.join(DATA_DIR, "dry_run_plan.json"), encoding="utf-8"))
    pilot_bundle = json.load(open(os.path.join(DATA_DIR, "pilot_raw_bundle.json"), encoding="utf-8"))
    loc_data = json.load(open(os.path.join(DATA_DIR, "verified_nc_locations.json"), encoding="utf-8"))

    proposed = build_proposed_pilot_pages()

    # Save staged HTML files and unified diff patch
    all_diffs = []
    before_after_stats = []
    for slug, (orig_html, new_html, orig_path) in proposed.items():
        clean_slug = slug.strip("/")
        stage_dir = os.path.join(STAGING_DIR, clean_slug)
        os.makedirs(stage_dir, exist_ok=True)
        with open(os.path.join(stage_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(new_html)

        diff_lines = list(
            difflib.unified_diff(
                orig_html.splitlines(keepends=True),
                new_html.splitlines(keepends=True),
                fromfile=f"a/charlotte-land-clearing/{clean_slug}/index.html",
                tofile=f"b/charlotte-land-clearing/{clean_slug}/index.html",
                n=3,
            )
        )
        all_diffs.append("".join(diff_lines))

        # Word counts & schema comparison
        orig_main = re.search(r"<main[^>]*>(.*?)</main>", orig_html, re.S).group(1)
        new_main = re.search(r"<main[^>]*>(.*?)</main>", new_html, re.S).group(1)
        orig_words = len(re.sub(r"<[^>]+>", " ", orig_main).split())
        new_words = len(re.sub(r"<[^>]+>", " ", new_main).split())
        orig_tables = len(re.findall(r"<table", orig_main))
        new_tables = len(re.findall(r"<table", new_main))
        orig_h3 = len(re.findall(r"<h3", orig_main))
        new_h3 = len(re.findall(r"<h3", new_main))

        before_after_stats.append(
            {
                "slug": slug,
                "orig_words": orig_words,
                "new_words": new_words,
                "word_delta": new_words - orig_words,
                "orig_h3": orig_h3,
                "new_h3": new_h3,
                "orig_tables": orig_tables,
                "new_tables": new_tables,
                "orig_schemas": ["LocalBusiness", "Service", "BreadcrumbList"],
                "new_schemas": ["LocalBusiness", "Service", "BreadcrumbList", "FAQPage"],
            }
        )

    diff_path = os.path.join(DELIV_DIR, "05_proposed_source_code_patches.diff")
    with open(diff_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_diffs))

    print("Staged 4 pilot pages and wrote unified diff:", diff_path)
    print("Before/After stats:", json.dumps(before_after_stats, indent=2))


if __name__ == "__main__":
    main()
