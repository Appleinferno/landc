import os
import json
import difflib
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "charlotte-land-clearing"))
STAGING_DIR = os.path.join(BASE_DIR, "staging")
DELIV_DIR = os.path.join(BASE_DIR, "deliverables")

from html import unescape
import re

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

    if city_override:
        for node in graph:
            if node.get("@type") == "LocalBusiness":
                node["areaServed"] = [
                    {"@type": "City", "name": "Charlotte", "containedInPlace": {"@type": "State", "name": "North Carolina"}},
                    {"@type": "City", "name": city_override, "containedInPlace": {"@type": "State", "name": "North Carolina"}},
                ]

    graph = [n for n in graph if n.get("@type") != "FAQPage"]
    faq_entities = extract_faqs_for_schema(html)
    if faq_entities:
        graph.append({"@type": "FAQPage", "mainEntity": faq_entities})
    data["@graph"] = graph

    formatted = "\n".join("  " + line for line in json.dumps(data, indent=2, ensure_ascii=False).splitlines())
    return html[: m.start()] + f'  <script type="application/ld+json">\n{formatted}\n  </script>' + html[m.end() :]

CITY_ENRICHMENTS = {
    # =========================================================================
    # 1. LAND CLEARING MINT HILL NC
    # =========================================================================
    "land-clearing-mint-hill-nc": {
        "city_name": "Mint Hill",
        "target": """<h3>Mint Hill UDO, the One-Acre Rule &amp; Typical Clearing Costs</h3>
            <p>Inside town limits, the <strong>Town of Mint Hill Unified Development Ordinance (UDO)</strong> regulates tree preservation and post-construction stormwater, and under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong>, disturbing <strong>one acre or more</strong> (including individual lots within a larger common plan of development exceeding one acre cumulatively) requires an approved Erosion and Sedimentation Control Plan before land-disturbing work begins. Land clearing in Mint Hill typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Your exact per-acre rate depends on thick brush density, the amount of tree removal involving trees thicker than 8 inches, steep banks or hilly terrain, and rocks that equipment must navigate around.</p>""",
        "replacement": """<h3>Mint Hill Land Clearing Methods by Property Zone</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mint Hill Property Zone</th>
                    <th scope="col">Recommended Clearing Approach</th>
                    <th scope="col">Ordinance &amp; Soil Considerations</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Back-Lot Custom Home Pads &amp; Long Driveways</strong> (Blair Rd / NC-51, Idlewild Rd, Lawyers Rd)</td>
                    <td>Full tree clearing + excavator stump removal (we can bring our excavator and haul off trees 8&Prime;+ if needed)</td>
                    <td>Delivers bare mineral soil free of buried wood for your grading contractor; call NC 811 3 business days before digging</td>
                  </tr>
                  <tr>
                    <td><strong>Pastures, Horse Acreage &amp; Wooded Perimeter Buffers</strong> (Brief Rd, Fairview Rd, NC-218)</td>
                    <td>Tracked forestry mulching in place (no minimum pass width needed; we work ourselves a path in)</td>
                    <td>Preserves feeder roots and Town of Mint Hill UDO tree-save buffers with zero dump-truck or open-burning costs</td>
                  </tr>
                  <tr>
                    <td><strong>Goose Creek &amp; McAlpine Creek Corridors</strong> (Stevens Creek, Duck Creek, Irvins Creek)</td>
                    <td>Selective upland mulching strictly outside flagged riparian buffer boundaries</td>
                    <td>Respects NCDEQ Goose Creek 100-ft / 200-ft undisturbed buffers (15A NCAC 02B .0607) &amp; Mecklenburg LUESA S.W.I.M. buffers</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Mint Hill UDO, the One-Acre Rule &amp; Per-Acre vs. Small-Lot Pricing</h3>
            <p>Inside municipal limits, the <strong>Town of Mint Hill Unified Development Ordinance (UDO)</strong> governs specimen tree preservation and post-construction stormwater controls, and under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong>, disturbing <strong>one acre or more</strong> (or a smaller parcel within a common plan of development exceeding one acre cumulatively) requires an approved Erosion and Sedimentation Control Plan before earthwork starts. Full-acreage land clearing in Mint Hill typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. If you only need a narrow driveway corridor cut off Brief Road or a fractional-acre backyard barn pad opened up, we price kindly and fairly based on equipment access, travel distance along I-485, and how many gullies, rocks, or tight keeper-tree obstacles take extra care—while larger trees 8 inches or wider can be excavated and hauled off with our excavator whenever your site requires it.</p>"""
    },

    # =========================================================================
    # 2. LAND CLEARING WAXHAW NC
    # =========================================================================
    "land-clearing-waxhaw-nc": {
        "city_name": "Waxhaw",
        "target": """<h3>Waxhaw Permits, the One-Acre Rule &amp; Per-Acre Costs</h3>
            <p>Inside town limits, the Town of Waxhaw UDO regulates tree preservation, specimen tree save, and perimeter buffers on development sites, while estate communities such as Providence Downs South, MillBridge, and Lawson require HOA architectural approval. Under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong> administered by NCDEQ, an approved Erosion and Sedimentation Control Plan is required before disturbing <strong>one acre or more</strong> (including individual lots within a larger common plan of development that exceeds one acre cumulatively). Land clearing in Waxhaw typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four factors drive where a parcel falls in that range: thick brush, the amount of tree removal involving trees thicker than 8 inches, steep banks or hilly terrain, and rocks that equipment must work around.</p>""",
        "replacement": """<h3>Comparing Waxhaw Land Clearing Methods Across Union County Tracts</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Waxhaw Property Type</th>
                    <th scope="col">Primary Equipment &amp; Method</th>
                    <th scope="col">Local Buffer &amp; Site Focus</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Custom Home Envelopes, Barn Pads &amp; Septic Sites</strong> (NC-16, Kensington Rd, Marvin &amp; Weddington borders)</td>
                    <td>Full tree clearing + excavator stump digging (excavator haul-off available for trees 8&Prime; or wider)</td>
                    <td>Prepares uncompacted, root-free Union County clay for your grading contractor; protects HOA perimeter tree-save zones</td>
                  </tr>
                  <tr>
                    <td><strong>Equestrian Paddocks, Bridle Trails &amp; Wooded Acreage</strong> (New Town Rd, Cuthbertson Rd, Crane Rd)</td>
                    <td>Tracked rotary drum mulching in place (no minimum pre-cleared width required)</td>
                    <td>Grinds eastern red cedar, wild cherry, and privet flush to the sod without gouging topsoil or leaving dirt windrows</td>
                  </tr>
                  <tr>
                    <td><strong>Deep Timber Tracts &amp; Creek Corridors</strong> (South of NC-75 toward Cane Creek Park &amp; Jaars Rd)</td>
                    <td>Phased access-road clearing + upland mulching outside stream buffers</td>
                    <td>Complies with Town of Waxhaw UDO &amp; Union County stream buffers along Twelve Mile Creek, Waxhaw Creek, and Cane Creek</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Waxhaw Permits, the One-Acre Rule &amp; Transparent Clearing Costs</h3>
            <p>Within municipal boundaries, the <strong>Town of Waxhaw Unified Development Ordinance (UDO)</strong> enforces tree preservation, heritage/specimen tree save, and streetscape buffers on development parcels, while gated and estate neighborhoods like Providence Downs South, MillBridge, and Lawson require architectural committee sign-off before tree removal. Whenever total soil disturbance reaches <strong>one acre or more</strong> (or involves a smaller lot inside a subdivision's common plan of development under <strong>NC G.S. 113A-57</strong>), an NCDEQ Erosion and Sedimentation Control Plan is required beforehand. Full-acreage land clearing in Waxhaw typically runs <strong>$2,000 to $8,000 per acre</strong>, with <strong>stump grinding and full stump removal quoted separately</strong>. For smaller Waxhaw building envelopes, paddock corners, or long gravel-driveway cuts where we work our own path into the woods, we price fairly by machine access, travel distance down NC-16, brush density, slope, rock outcrops, and how many trees 8 inches or wider need excavator removal and haul-off.</p>"""
    },

    # =========================================================================
    # 3. LAND CLEARING CONCORD NC
    # =========================================================================
    "land-clearing-concord-nc": {
        "city_name": "Concord",
        "target": """<h3>Concord Development Ordinance, the One-Acre Rule &amp; Per-Acre Pricing</h3>
            <p>Inside city limits, the <strong>City of Concord Development Ordinance (CDO Article 11)</strong> regulates tree preservation, floodplain protection, and stream buffers, while unincorporated parcels follow the <strong>Cabarrus County Development Ordinance</strong>. Under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong> administered by NCDEQ, an approved Erosion and Sedimentation Control Plan is required before disturbing <strong>one acre or more</strong> (including individual lots within a larger common plan of development exceeding one acre cumulatively). Land clearing in Concord typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. We calculate your per-acre rate based on four site factors: thick brush density, the amount of tree removal involving trees thicker than 8 inches, steep banks or hilly terrain, and rocks that equipment must navigate around.</p>""",
        "replacement": """<h3>Concord &amp; Cabarrus County Land Clearing Methods Compared</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Concord Corridor &amp; Parcel Type</th>
                    <th scope="col">Clearing Method</th>
                    <th scope="col">Soil, Slate-Belt &amp; Ordinance Notes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Wooded Residential Pads &amp; Driveways</strong> (Poplar Tent Rd, Odell School Rd, George Liles Pkwy, NC-73)</td>
                    <td>Selective tree clearing + excavator stump removal (trees 8&Prime;+ excavated and hauled off as needed)</td>
                    <td>Protects flagged shade oaks while delivering a stump-free footprint for your builder; follows CDO Article 11 tree rules</td>
                  </tr>
                  <tr>
                    <td><strong>Rolling Farm &amp; Timber Acreage</strong> (East of US-29 &amp; NC-49: Flowes Store Rd, Gold Hill Rd, Miami Church Rd)</td>
                    <td>Single-machine tracked forestry mulching (we cut our own entry path in; no minimum width required)</td>
                    <td>Leaves root webs intact on Carolina Slate Belt slopes and avoids pulling buried fieldstone to the surface</td>
                  </tr>
                  <tr>
                    <td><strong>Infill &amp; Commercial Sites</strong> (US-29 / Concord Pkwy, Church St, Branchview Dr)</td>
                    <td>Staked limit-of-disturbance clearing + debris haul-off</td>
                    <td>Coordinates with NC 811 locates, general contractor schedules, and Coddle Creek / Rocky River buffer setbacks</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Concord Development Ordinance, the One-Acre Rule &amp; Fair Project Pricing</h3>
            <p>Parcels inside municipal boundaries are governed by the <strong>City of Concord Development Ordinance (CDO Article 11)</strong> for tree preservation, floodplain management, and riparian buffers, while rural tracts follow the <strong>Cabarrus County Development Ordinance</strong>. Any project that uncovers <strong>one acre or more</strong> of soil—including sub-acre homesites that belong to a larger subdivision common plan under <strong>NC G.S. 113A-57</strong>—must have an approved Erosion and Sedimentation Control Plan prior to disturbance. Across Concord, full-acreage land clearing averages <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. If you have an in-town infill lot under an acre or a narrow shop-pad expansion, we price warmly and fairly around access, travel up I-85, steep ravines, Carolina Slate Belt rock outcrops, and whether trees 8 inches or wider require our excavator and haul-off trucks.</p>"""
    },

    # =========================================================================
    # 4. LAND CLEARING MOORESVILLE NC
    # =========================================================================
    "land-clearing-mooresville-nc": {
        "city_name": "Mooresville",
        "target": """<h3>Slopes, Red Clay &amp; Mooresville Land Clearing Costs</h3>
            <p>Land clearing in Mooresville typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four site conditions determine where your quote falls in that range: thick brush density, the amount of tree removal involving trees thicker than 8 inches, steep banks or hilly terrain, and rocks that equipment must work around. Lake-area lots and creek draws draining into Dye Creek, Reed Creek, and Back Creek drop over Piedmont red clay, so we use low-ground-pressure tracked equipment and leave shredded mulch cover outside the structural footprint to help slow surface runoff until your grading contractor installs silt fence.</p>""",
        "replacement": """<h3>Mooresville &amp; Lake Norman Land Clearing Methods by Zone</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mooresville / Southern Iredell Zone</th>
                    <th scope="col">Clearing Method</th>
                    <th scope="col">Shoreline &amp; Watershed Safeguards</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Lake Norman Peninsula Custom Home &amp; Pool Envelopes</strong> (Brawley School Rd, Perth Rd, The Point, Langtree Rd)</td>
                    <td>Precision tree removal + excavator stump digging inside staked footprints (excavator haul-off for trees 8&Prime;+)</td>
                    <td>Preserves view-framing canopy oaks; stays strictly landward of the Duke Energy 760-ft contour &amp; 50-ft shoreline buffer</td>
                  </tr>
                  <tr>
                    <td><strong>Sloped Lakefront View Corridors &amp; Wooded Buffers</strong> (Williamson Rd, Morrison Plantation, Cove lots)</td>
                    <td>Low-ground-pressure tracked forestry mulching (no minimum pass width required)</td>
                    <td>Leaves root webs intact in steep red clay draining to Dye Creek, Reed Creek, and Back Creek under Iredell watershed rules</td>
                  </tr>
                  <tr>
                    <td><strong>Rural Acreage, Pastures &amp; Shop Pads East of I-77</strong> (NC-150, Shearers Rd, Mazeppa Rd, NC-3)</td>
                    <td>Combined pad excavation + economical acreage mulching</td>
                    <td>Complies with Town of Mooresville UDO tree-save standards &amp; NC G.S. 113A-57 one-acre erosion control rules</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Slopes, Red Clay &amp; Mooresville Land Clearing Costs ($2,000 - $8,000 Per Acre)</h3>
            <p>Full-acreage land clearing in Mooresville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Because many Lake Norman peninsula parcels and in-town lots are under an acre or tucked between neighboring homes on Brawley School Road, we never force a one-size-fits-all acreage minimum—smaller residential lots are priced kindly and fairly based on gate/driveway access (we can work ourselves a path in), travel up I-77, steep cove banks, rock outcrops, and tight obstacles around keeper trees. When a build involves significant removal of trees 8 inches or wider, we bring in our excavator and haul off the trunks so your grading contractor gets a clean pad.</p>"""
    },

    # =========================================================================
    # 5. LAND CLEARING INDIAN TRAIL NC
    # =========================================================================
    "land-clearing-indian-trail-nc": {
        "city_name": "Indian Trail",
        "target": """<h3>Indian Trail Permits, the One-Acre Rule &amp; Per-Acre Clearing Costs</h3>
            <p>The Town of Indian Trail UDO sets tree-save and buffer standards for development projects, and under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong> administered by NCDEQ, disturbing <strong>one acre or more</strong> (including individual lots within a larger common plan of development exceeding one acre cumulatively) requires an approved Erosion and Sedimentation Control Plan prior to land disturbance. Land clearing in Indian Trail typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. Four site factors drive the per-acre quote: thick brush density, the amount of tree removal involving trees thicker than 8 inches, steep banks or hilly terrain, and rocks that equipment must navigate around. We do not perform finish grading or build house pads; we deliver a cleanly cleared envelope ready for your grading contractor.</p>""",
        "replacement": """<h3>Indian Trail Land Clearing Methods Across Residential &amp; US-74 Sites</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Indian Trail Parcel Type</th>
                    <th scope="col">Recommended Clearing Method</th>
                    <th scope="col">Buffer &amp; Construction Handoff</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Infill Homesites &amp; Detached Shop Pads</strong> (Chestnut Ln, Potter Rd, Old Monroe Rd, Poplin Rd)</td>
                    <td>Selective tree removal + excavator stump digging (trees 8&Prime;+ removed and hauled off when needed)</td>
                    <td>Protects neighbor boundary trees; leaves a root-free pad ready for your grading contractor (no finish grading performed)</td>
                  </tr>
                  <tr>
                    <td><strong>Multi-Acre Homesteads &amp; Trails</strong> (Faith Church Rd, Unionville-Indian Trail Rd, Secrest Short Cut Rd)</td>
                    <td>Phased pad excavation + tracked forestry mulching (no minimum pass width required; we cut our own path in)</td>
                    <td>Shreds pine and sweetgum thickets into erosion-resistant mulch cover with zero open burning or haul-off fees</td>
                  </tr>
                  <tr>
                    <td><strong>Goose Creek &amp; Crooked Creek Watershed Lots</strong> (Northern Indian Trail, Idlewild Rd, US-74 corridor)</td>
                    <td>Staked limit-of-disturbance clearing outside protected riparian zones</td>
                    <td>Respects NCDEQ Goose Creek 100-ft / 200-ft undisturbed buffers (15A NCAC 02B .0607) &amp; Town of Indian Trail UDO rules</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Indian Trail Permits, the One-Acre Rule &amp; Per-Acre vs. Infill Lot Pricing</h3>
            <p>The <strong>Town of Indian Trail Unified Development Ordinance (UDO)</strong> establishes tree-save and perimeter buffer standards for new development, and under North Carolina's <strong>Sedimentation Pollution Control Act of 1973 (G.S. 113A-57)</strong>, any land disturbance reaching <strong>one acre or more</strong> (or a smaller parcel inside a common subdivision plan exceeding one acre cumulatively) requires an approved Erosion and Sedimentation Control Plan prior to clearing. Across Indian Trail, full-acreage land clearing typically ranges from <strong>$2,000 to $8,000 per acre</strong>, with <strong>stump grinding and full stump removal quoted separately</strong>. For half-acre infill lots between Brandon Oaks and Bonterra or tight backyard access corridors, we price fairly by access, travel distance along US-74, hills, rocks, and obstacles—and when your footprint includes trees 8 inches or wider, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 6. FORESTRY MULCHING HUNTERSVILLE NC
    # =========================================================================
    "forestry-mulching-huntersville-nc": {
        "city_name": "Huntersville",
        "target": """<h3>Forestry Mulching Cost in Huntersville ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while any <strong>stump grinding or full stump removal is quoted separately</strong>. Four site factors drive where your project lands in that range: (1) <strong>thick brush density</strong> (solid privet, autumn olive, and briar walls vs. open understory), (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong> toward creek draws and lake coves, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves roots in the soil and lays down a two- to four-inch shredded wood-chip blanket that decomposes over 12 to 24 months, it is not a substitute for bare-dirt grading or full stump extraction under a future house foundation, concrete slab, or paved driveway—and hardy species like sweetgum and privet will need periodic mowing or rotary cutting to keep sprouts down.</p>""",
        "replacement": """<h3>Huntersville Forestry Mulching vs. Excavator Clearing &amp; Bush Hogging</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Huntersville Terrain &amp; Goal</th>
                    <th scope="col">Best Equipment Approach</th>
                    <th scope="col">Soil, Tree-Save &amp; Watershed Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Hardwood Understory &amp; Estate Woodlines</strong> (Gilead Rd, Hambright Rd, Ramah Church Rd, Birkdale)</td>
                    <td>Compact tracked drum mulcher (no minimum gate/pass width required; we cut our own path in)</td>
                    <td>Shreds privet, autumn olive, and saplings under 8&Prime; while protecting white oak Critical Root Zones under Town Zoning Article 7</td>
                  </tr>
                  <tr>
                    <td><strong>Pasture Edges, UTV Trails &amp; Lake Coves</strong> (Beatties Ford Rd, Bud Henderson Rd, Mountain Island Lake / Lake Norman)</td>
                    <td>Low-ground-pressure surface mulching (0.5&ndash;2 acres/day production)</td>
                    <td>Leaves feeder roots intact and spreads a 2&ndash;4&Prime; mulch blanket outside Duke Energy 50-ft shoreline &amp; LUESA S.W.I.M. buffers</td>
                  </tr>
                  <tr>
                    <td><strong>Trees 8&Prime;+ or Structural Pads</strong> (Home additions, detached garages, driveways)</td>
                    <td>Excavator tree removal &amp; stump digging (haul-off available; quoted separately)</td>
                    <td>Removes root balls where decomposing wood cannot stay under concrete or structural fill</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Huntersville ($2,000-$8,000 per Acre) &amp; Small-Lot Pricing</h3>
            <p>Full-acreage forestry mulching in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with any <strong>stump grinding or full stump removal quoted separately</strong>. If you have a smaller North Mecklenburg backyard under an acre or a narrow walking trail to open up, we don't apply a rigid acreage minimum—instead, we price warmly and fairly based on equipment access, travel distance up I-77, and how many steep creek banks, surface rock outcrops near Mountain Island Lake, or tight keeper-tree obstacles require slower passes. While brush and saplings under 8 inches are shredded in place into a two- to four-inch wood-fiber blanket that decomposes over 12 to 24 months, <strong>trees 8 inches or wider take a different approach</strong>—when your job involves significant larger tree removal or a structural pad, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 7. FORESTRY MULCHING MINT HILL NC
    # =========================================================================
    "forestry-mulching-mint-hill-nc": {
        "city_name": "Mint Hill",
        "target": """<h3>Forestry Mulching Cost in Mint Hill ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Mint Hill typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves root crowns in the soil and covers the surface with a two- to four-inch layer of shredded wood fiber that decomposes over 12 to 24 months, it is not a replacement for full stump grubbing under a house pad, workshop slab, or driveway—and species like sweetgum and privet will require occasional mowing to keep root sprouts down.</p>""",
        "replacement": """<h3>Mint Hill Forestry Mulching Applications &amp; Method Trade-Offs</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mint Hill Property Setting</th>
                    <th scope="col">Clearing Method</th>
                    <th scope="col">Finished Ground &amp; Buffer Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Deep Backyard Hardwood Stands</strong> (Lawyers Rd, Matthews-Mint Hill Rd / NC-51, Wilgrove-Mint Hill Rd)</td>
                    <td>Selective tracked rotary drum mulching (no minimum pass width needed; we work our own path in)</td>
                    <td>Turns autumn olive, privet, and vine tangles into a walkable park-like floor without burning under LUESA Air Quality rules</td>
                  </tr>
                  <tr>
                    <td><strong>Overgrown Pastures, Hayfields &amp; Survey Corridors</strong> (Brief Rd, Fairview Rd, NC-218, Lebanon Rd)</td>
                    <td>Single-pass field reclamation mulching (typically 0.5&ndash;2 acres/day)</td>
                    <td>Grinds eastern red cedar, locust, and briars flush to the sod outside Goose Creek 100-ft / 200-ft undisturbed buffers</td>
                  </tr>
                  <tr>
                    <td><strong>Workshop Slabs, Driveways &amp; Trees 8&Prime;+</strong> (Structural footprints across Mint Hill)</td>
                    <td>Excavator tree removal &amp; stump excavation (haul-off available; quoted separately)</td>
                    <td>Prevents slab settlement where decomposing mulch and root crowns are not suitable</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Mint Hill ($2,000-$8,000 per Acre) &amp; Flexible Lot Pricing</h3>
            <p>Full-acreage forestry mulching in Mint Hill typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. For Mint Hill homeowners who only want the back half-acre opened up behind the house or a narrow perimeter trail cut for a surveyor, we price kindly and fairly based on how easy the work area is to reach, travel distance off I-485, and how many gullies, rock outcrops, old wire fences, or closely spaced keeper oaks take extra time. Saplings and thick brush under 8 inches shred directly into a two- to four-inch mulch bed that breaks down over 12 to 24 months, whereas <strong>trees 8 inches or wider take a different approach</strong>—if your project requires taking out larger timber, we can bring in our excavator and haul off the trees as part of a clear written scope.</p>"""
    },

    # =========================================================================
    # 8. FORESTRY MULCHING WAXHAW NC
    # =========================================================================
    "forestry-mulching-waxhaw-nc": {
        "city_name": "Waxhaw",
        "target": """<h3>Forestry Mulching Cost in Waxhaw ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Waxhaw typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project lands in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves root crowns in place and blankets the surface with a two- to four-inch wood-chip layer that decomposes over 12 to 24 months, it is not a replacement for full stump excavation under a house pad, barn foundation, or driveway—and species like sweetgum and privet will need periodic bush-hogging or mowing to control resprouting.</p>""",
        "replacement": """<h3>Waxhaw Forestry Mulching vs. Pasture Dozing &amp; Pad Excavation</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Waxhaw / Western Union County Use Case</th>
                    <th scope="col">Recommended Method</th>
                    <th scope="col">Soil, Hoof-Safety &amp; Watershed Impact</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Wooded Estate Understory &amp; Privacy Buffers</strong> (NC-16 / Providence Rd S, Kensington Rd, Marvin &amp; Weddington borders)</td>
                    <td>Selective low-ground-pressure forestry mulching (no minimum pass width required)</td>
                    <td>Clears greenbrier, privet, and sweetgum beneath white oaks while honoring Town of Waxhaw UDO specimen tree rules</td>
                  </tr>
                  <tr>
                    <td><strong>Pasture Reclamation, Bridle Paths &amp; Hunting Trails</strong> (New Town Rd, Cuthbertson Rd, Crane Rd, south of NC-75 to Jaars Rd)</td>
                    <td>Rotary drum mulching flush to grade (0.5&ndash;2 acres/day)</td>
                    <td>Avoids dozer topsoil gouging along Twelve Mile Creek &amp; Cane Creek watersheds; inspect corridors before turning horses out</td>
                  </tr>
                  <tr>
                    <td><strong>Barn Pads, Riding Arenas &amp; Trees 8&Prime; or Wider</strong> (Structural &amp; heavy timber areas)</td>
                    <td>Excavator tree removal, haul-off &amp; separate stump excavation</td>
                    <td>Extracts root balls and large trunks where 2&ndash;4&Prime; surface mulch and decaying roots aren't appropriate</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Waxhaw ($2,000-$8,000 per Acre) &amp; Trail / Small-Lot Pricing</h3>
            <p>Full-acreage forestry mulching in Waxhaw typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, with <strong>stump grinding and full stump removal quoted separately</strong>. If you only need an eight-foot horse trail cut through the woods south of NC-75 or a fractional-acre woodline pushed back in Hunter Oaks or MillBridge, we price warmly and fairly based on equipment access (we need no minimum pre-cleared width because we can mulch our own path in), travel distance, hilly creek draws, rocks, and how selectively we are working around keeper trees. Brush and saplings under 8 inches are shredded in place into a two- to four-inch wood-chip blanket that decomposes over 12 to 24 months, while <strong>trees 8 inches or wider take a different approach</strong>—when significant tree removal is needed, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 9. FORESTRY MULCHING CONCORD NC
    # =========================================================================
    "forestry-mulching-concord-nc": {
        "city_name": "Concord",
        "target": """<h3>Forestry Mulching Cost in Concord ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Concord typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your parcel falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves root crowns in the soil and lays down a two- to four-inch layer of shredded wood that decomposes over 12 to 24 months, it is not a replacement for bare-dirt grading or full stump extraction under a future home foundation, concrete slab, or driveway—and species like sweetgum and privet will need periodic mowing or rotary cutting to control root sprouts.</p>""",
        "replacement": """<h3>Concord &amp; Cabarrus County Forestry Mulching Applications</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Concord Area &amp; Terrain</th>
                    <th scope="col">Equipment &amp; Method</th>
                    <th scope="col">Cabarrus Soil &amp; Ordinance Advantage</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Wooded Homesites &amp; Backyard Canopies</strong> (Poplar Tent Rd, Odell School Rd, Weddington Rd, George Liles Pkwy)</td>
                    <td>Selective tracked rotary drum mulching (we cut our own path in; no minimum width needed)</td>
                    <td>Removes Chinese privet and thorny greenbrier while protecting mature oaks and CDO Article 11 buffer zones</td>
                  </tr>
                  <tr>
                    <td><strong>Eastern Cabarrus Pastures &amp; Slate-Belt Acreage</strong> (Flowes Store Rd, Gold Hill Rd, Miami Church Rd, NC-49)</td>
                    <td>Top-down surface mulching (0.5&ndash;2 acres/day without burn piles)</td>
                    <td>Holds Piedmont clay and Carolina Slate Belt silt-loam on slopes draining to Rocky River &amp; Coddle Creek without pulling up fieldstone</td>
                  </tr>
                  <tr>
                    <td><strong>Detached Shops, Home Pads &amp; Trees 8&Prime;+</strong> (Structural footprints &amp; large timber)</td>
                    <td>Excavator tree removal &amp; stump digging (haul-off available; quoted separately)</td>
                    <td>Provides bare, root-free soil where decomposing wood fiber cannot remain beneath concrete or driveways</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Concord ($2,000-$8,000 per Acre) &amp; Small-Parcel Quotes</h3>
            <p>Full-acreage forestry mulching in Concord typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. For smaller Concord residential lots under an acre or narrow property-line trails, we price kindly and fairly around machine access, travel distance up I-85, brush thickness, steep creek banks, and exposed Carolina Slate Belt fieldstone that our operator must navigate around carefully. While brush and saplings under 8 inches shred directly into a two- to four-inch wood mulch layer that decomposes over 12 to 24 months, <strong>trees 8 inches or wider take a different approach</strong>—when your job requires removing larger trees or clearing a building pad, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 10. FORESTRY MULCHING MOORESVILLE NC
    # =========================================================================
    "forestry-mulching-mooresville-nc": {
        "city_name": "Mooresville",
        "target": """<h3>Forestry Mulching Cost in Mooresville ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Mooresville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your parcel lands in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong> along Lake Norman coves and creek draws, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves root crowns in the ground and creates a two- to four-inch shredded wood layer that decomposes over 12 to 24 months, it is not a substitute for full stump excavation under a house foundation, pool, or driveway—and species like sweetgum and privet will need periodic mowing or rotary cutting to control root sprouts.</p>""",
        "replacement": """<h3>Mooresville Forestry Mulching Across Lake Norman Slopes &amp; Iredell Acreage</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mooresville / Lake Norman Setting</th>
                    <th scope="col">Equipment &amp; Method</th>
                    <th scope="col">Erosion, Shoreline &amp; Site Benefit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Sloped Lake Norman Lots &amp; Pre-Build Walkability</strong> (Brawley School Rd, Perth Rd, Langtree Rd, Williamson Rd)</td>
                    <td>Low-ground-pressure tracked drum mulching (no minimum pass width required)</td>
                    <td>Keeps root webs intact in steep red clay and stays upland of the Duke Energy 760-ft contour &amp; 50-ft shoreline buffer</td>
                  </tr>
                  <tr>
                    <td><strong>Southern Iredell Pastures, Trails &amp; Timber</strong> (East of I-77: NC-150, Shearers Rd, Mazeppa Rd, NC-3)</td>
                    <td>Single-machine acreage mulching (0.5&ndash;2 acres/day; zero haul-off fees)</td>
                    <td>Reclaims fields from cedar and sweetgum while respecting Town of Mooresville UDO &amp; Iredell watershed rules</td>
                  </tr>
                  <tr>
                    <td><strong>Custom Home Pads, Pools &amp; Trees 8&Prime; or Wider</strong> (Structural footprints)</td>
                    <td>Excavator tree removal &amp; stump extraction (haul-off available; quoted separately)</td>
                    <td>Removes large trunks and root balls where a 2&ndash;4&Prime; decomposing mulch layer cannot stay under foundations</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Mooresville ($2,000-$8,000 per Acre) &amp; Lake-Lot Pricing</h3>
            <p>Full-acreage forestry mulching in Mooresville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Because many Mooresville lake lots and pre-purchase wooded parcels are under an acre or have tight access between homes, we price smaller jobs kindly and fairly based on access (we can work ourselves a path in without a pre-cleared lane), travel up I-77, steep cove slopes, rock outcrops, and careful selectivity around keeper oaks. Saplings and underbrush under 8 inches are shredded in place into a two- to four-inch wood blanket that breaks down over 12 to 24 months, while <strong>trees 8 inches or wider take a different approach</strong>—when your project involves larger tree removal, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 11. FORESTRY MULCHING INDIAN TRAIL NC
    # =========================================================================
    "forestry-mulching-indian-trail-nc": {
        "city_name": "Indian Trail",
        "target": """<h3>Forestry Mulching Cost in Indian Trail ($2,000-$8,000 per Acre) &amp; Method Trade-Offs</h3>
            <p>Forestry mulching in Indian Trail typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project lands in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Because forestry mulching leaves root crowns in the ground and blankets the surface with a two- to four-inch layer of shredded wood that decomposes over 12 to 24 months, it is not a replacement for bare-dirt grading or full stump extraction under a future home foundation, pool, or driveway—and species like sweetgum and privet will require occasional mowing or rotary cutting to keep sprouts down.</p>""",
        "replacement": """<h3>Indian Trail Forestry Mulching by Property Type &amp; Watershed</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Indian Trail Property Setting</th>
                    <th scope="col">Clearing Approach</th>
                    <th scope="col">Root-Zone &amp; Watershed Benefit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Half-Acre to Two-Acre Wooded Backyards</strong> (Idlewild Rd, Chestnut Ln, Potter Rd, Wesley Chapel-Stouts Rd)</td>
                    <td>Compact tracked rotary drum mulching (no minimum pass width needed; we cut our own path in)</td>
                    <td>Shreds Chinese privet, honeysuckle, and sweetgum saplings without compacting feeder roots of flagged canopy oaks</td>
                  </tr>
                  <tr>
                    <td><strong>5&ndash;20 Acre Tracts, Pastures &amp; ATV Trails</strong> (Faith Church Rd, Unionville-Indian Trail Rd, Secrest Short Cut Rd)</td>
                    <td>Single-machine acreage &amp; trail mulching (0.5&ndash;2 acres/day)</td>
                    <td>Stays upland of Crooked Creek &amp; NCDEQ Goose Creek 100-ft / 200-ft undisturbed buffers (15A NCAC 02B .0607)</td>
                  </tr>
                  <tr>
                    <td><strong>Home Pads, Detached Shops &amp; Trees 8&Prime;+</strong> (Structural footprints across Union County)</td>
                    <td>Excavator tree removal &amp; stump digging (haul-off available; quoted separately)</td>
                    <td>Clears bare soil where decomposing mulch and buried roots cannot remain beneath slabs or driveways</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Forestry Mulching Cost in Indian Trail ($2,000-$8,000 per Acre) &amp; Backyard Pricing</h3>
            <p>Full-acreage forestry mulching in Indian Trail typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. If you have a half-acre wooded backyard near Brandon Oaks or Bonterra or a narrow fence corridor, we don't apply a rigid per-acre minimum—instead, we price warmly and fairly based on equipment access, travel distance along US-74, hills or drainage swales, rocks, and tight obstacles around keeper trees. While brush and saplings under 8 inches shred directly into a two- to four-inch wood mulch layer that decomposes over 12 to 24 months, <strong>trees 8 inches or wider take a different approach</strong>—when your job involves larger tree removal, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 12. BRUSH CLEARING HUNTERSVILLE NC
    # =========================================================================
    "brush-clearing-huntersville-nc": {
        "city_name": "Huntersville",
        "target": """<h3>Brush Clearing Cost in Huntersville ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project lands in that range: (1) <strong>thick brush density</strong> (solid walls of privet, briars, and vines vs. light undergrowth), (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. While a tractor bush hog can mow open grass and light weeds, it cannot safely handle dense woody stems or tight residential woodlines; our tracked drum mulcher shreds saplings and brambles flush to the soil in one pass, and if a project requires hauling debris off site or removing larger trees, we scope those items clearly in your written estimate.</p>""",
        "replacement": """<h3>Huntersville Brush Clearing Methods: Tracked Mulcher vs. Hand Detail &amp; Excavator</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Huntersville Brush Scenario</th>
                    <th scope="col">Our Mechanical Method</th>
                    <th scope="col">Finished Result &amp; Local Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Overgrown Backyard Woodlines &amp; Fence Rows</strong> (Gilead Rd, Sam Furr Rd / NC-73, Birkdale, Northstone)</td>
                    <td>Tracked drum mulcher up to the fence line + hand saws/trimmers right against panels and pedestals</td>
                    <td>Reclaims 20&ndash;30 ft of yard into a mowable mulch transition with zero open burning under LUESA Air Quality rules</td>
                  </tr>
                  <tr>
                    <td><strong>HOA Stormwater Ponds &amp; Vacant Lots</strong> (Skybrook, Vermillion, Monteith Park, NC-115, Hambright Rd)</td>
                    <td>Low-ground-pressure bank mulching + hand clearing over riprap and concrete risers</td>
                    <td>Clears willow and sweetgum saplings per Mecklenburg Storm Water Services standards; photo documentation provided</td>
                  </tr>
                  <tr>
                    <td><strong>Heavy Saplings &amp; Trees 8&Prime; or Wider</strong> (Dense neglected lots &amp; future building areas)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Removes trunks 8&Prime;+ cleanly outside Duke Energy 50-ft shoreline &amp; LUESA S.W.I.M. creek buffers</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Huntersville ($2,000-$8,000 per Acre) &amp; Backyard / Fence Pricing</h3>
            <p>Full-acreage brush clearing in Huntersville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. For smaller Huntersville backyards, narrow fence corridors, or HOA pond embankments, we price kindly and fairly based on equipment access (no minimum pass width is required—we can work ourselves a path in), travel up I-77, steep pond or cove slopes, surface rocks, and hand-detail time around fences and utility boxes. Unlike a tractor bush hog that bounces off woody stems, our tracked mulcher shreds briars and saplings under 8 inches flush to grade in one pass—and when a job involves <strong>trees 8 inches or wider</strong>, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 13. BRUSH CLEARING MINT HILL NC
    # =========================================================================
    "brush-clearing-mint-hill-nc": {
        "city_name": "Mint Hill",
        "target": """<h3>Brush Clearing Cost in Mint Hill ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Mint Hill typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Unlike a tractor bush hog that bounces off woody stems and leaves ragged stobs, our tracked mulcher shreds saplings and briars into a flat wood-fiber mat—and right against standing fences, gates, sheds, and culvert heads, we switch to hand saws and brush cutters so structures aren't bumped.</p>""",
        "replacement": """<h3>Mint Hill Brush Clearing Methods by Property Feature</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mint Hill Brush &amp; Overgrowth Area</th>
                    <th scope="col">Mechanical Clearing Method</th>
                    <th scope="col">Site Safety &amp; Watershed Protection</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Deep Backyard Thickets &amp; Woodlines</strong> (Matthews-Mint Hill Rd / NC-51, Wilgrove-Mint Hill Rd, Lebanon Rd)</td>
                    <td>Tracked rotary drum mulcher (no minimum pass width needed; we cut our own path in)</td>
                    <td>Grinds blackberry briars, sumac, and privet into a mowable mulch bed while preserving mature white oaks</td>
                  </tr>
                  <tr>
                    <td><strong>Old Farm Wire, Fence Lines &amp; Driveway Ditches</strong> (Brief Rd, Lawyers Rd, Fairview Rd)</td>
                    <td>Pre-walk wire flagging + tracked mulching + hand saws along posts, culverts, and well heads</td>
                    <td>Prevents wire entanglement, restores storm runoff visibility without regrading channels or spraying chemicals</td>
                  </tr>
                  <tr>
                    <td><strong>Overgrown Lots with Trees 8&Prime; or Wider</strong> (Eastern &amp; Western Mint Hill acreage)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Removes larger trunks outside Goose Creek 100-ft / 200-ft buffers (15A NCAC 02B .0607) &amp; LUESA S.W.I.M. buffers</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Mint Hill ($2,000-$8,000 per Acre) &amp; Small-Corridor Quotes</h3>
            <p>Full-acreage brush clearing in Mint Hill typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. If you only need a narrow fence line rescued, a driveway ditch cleared off Brief Road, or the back third of a residential lot opened up, we price warmly and fairly based on equipment access, travel distance along I-485, hills or gullies, rocks, hidden farm wire, and hand-trimming time around sheds and fences. While our tracked drum mulcher shreds brush and saplings under 8 inches into a flat wood-fiber mat with no ragged bush-hog stobs, <strong>trees 8 inches or wider take a different approach</strong>—when your property involves significant larger tree removal, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 14. BRUSH CLEARING WAXHAW NC
    # =========================================================================
    "brush-clearing-waxhaw-nc": {
        "city_name": "Waxhaw",
        "target": """<h3>Brush Clearing Cost in Waxhaw ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Waxhaw typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Unlike a tractor bush hog that leaves jagged sapling stobs that can puncture tractor tires or injure horses, our rotary drum mulcher grinds stems flush with the ground—and where larger deadfall, tree removal over 8 inches, or haul-away is needed near formal entryways, we scope those items clearly in your written estimate.</p>""",
        "replacement": """<h3>Waxhaw Brush Clearing Methods: Horse Pastures, Estate Lots &amp; HOA Ponds</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Waxhaw Property Feature</th>
                    <th scope="col">Our Mechanical Method</th>
                    <th scope="col">Equine Safety &amp; Union County Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Board Fences, Woven Wire &amp; Paddock Edges</strong> (New Town Rd, Cuthbertson Rd, Billy Howey Rd, Marvin Rd)</td>
                    <td>Tracked mulcher along the woodline + hand-clearing right against rails, gates, and T-posts</td>
                    <td>Removes toxic wild cherry limbs, privet, and briars without leaving jagged bush-hog stobs that injure horses</td>
                  </tr>
                  <tr>
                    <td><strong>Wooded Estate Lots, Farm Lanes &amp; HOA Ponds</strong> (NC-16, Kensington Rd, MillBridge, Lawson, Jaars Rd)</td>
                    <td>Low-ground-pressure drum mulching (no minimum pass width required) + hand tools on pond riprap</td>
                    <td>100% mechanical finish with zero chemical sprays outside Twelve Mile Creek &amp; Cane Creek watershed buffers</td>
                  </tr>
                  <tr>
                    <td><strong>Heavy Windfall &amp; Trees 8&Prime; or Wider</strong> (Entryways, barn corridors, neglected tracts)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Clears larger trunks and deadfall cleanly while respecting Town of Waxhaw UDO specimen tree rules</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Waxhaw ($2,000-$8,000 per Acre) &amp; Fence-Line Pricing</h3>
            <p>Full-acreage brush clearing in Waxhaw typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. When you only need a pasture fence line cleared off Cuthbertson Road, an HOA pond bank cut back, or a half-acre backyard thicket mulched, we price kindly and fairly based on gate/corridor access (we can work ourselves a path in), travel down NC-16, rolling hills, rocks, and hand-detail work along board fencing. Unlike a tractor bush hog that leaves sharp sapling stubs, our rotary drum mulcher grinds brush and saplings under 8 inches flush with the soil—and when a job involves <strong>trees 8 inches or wider</strong>, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 15. BRUSH CLEARING CONCORD NC
    # =========================================================================
    "brush-clearing-concord-nc": {
        "city_name": "Concord",
        "target": """<h3>Brush Clearing Cost in Concord ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Concord typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project lands in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong> (including Carolina Slate Belt fieldstone in eastern Cabarrus County). While a tractor bush hog can handle open pasture grass, our tracked rotary drum mulcher grinds dense briars and saplings flush to the ground in one pass—and right next to fences, gates, utility boxes, and culverts, we switch to hand saws and trimmers so structures stay safe.</p>""",
        "replacement": """<h3>Concord Brush Clearing Methods Across In-Town Lots &amp; Cabarrus Acreage</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Concord Site Condition</th>
                    <th scope="col">Mechanical Method</th>
                    <th scope="col">Code Compliance &amp; Soil Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Vacant Infill Lots &amp; City Overgrowth Notices</strong> (Downtown Concord, McGill Ave, Branchview Dr, US-29)</td>
                    <td>Tracked rotary drum mulching (no minimum pass width required; we cut our own path in)</td>
                    <td>Turns head-high privet, pokeweed, and sweetgum into a neat, mowable mulch bed before your City code deadline</td>
                  </tr>
                  <tr>
                    <td><strong>Residential Fence Lines &amp; Stormwater Basins</strong> (Poplar Tent Rd, George Liles Pkwy, Odell School Rd, NC-73)</td>
                    <td>Tracked mulcher + hand saws/trimmers along fences, culverts, and concrete pond risers</td>
                    <td>Protects structures and riprap aprons with zero herbicide sprays; stays outside Coddle Creek &amp; Rocky River buffers</td>
                  </tr>
                  <tr>
                    <td><strong>Eastern Cabarrus Farm Edges &amp; Trees 8&Prime;+</strong> (Flowes Store Rd, Miami Church Rd, Gold Hill Rd)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Handles trunks 8&Prime; or wider and navigates carefully around Carolina Slate Belt fieldstone outcrops</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Concord ($2,000-$8,000 per Acre) &amp; Infill / Fence Pricing</h3>
            <p>Full-acreage brush clearing in Concord typically runs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. For smaller in-town vacant lots, backyard fence lines off Poplar Tent Road, or commercial detention basins, we don't apply a rigid acreage minimum—instead, we price warmly and fairly based on equipment access, travel distance up I-85, steep banks, Carolina Slate Belt fieldstone rocks, and hand work around fences and utility pedestals. While brush and saplings under 8 inches shred flush to the ground in one pass, <strong>trees 8 inches or wider take a different approach</strong>—when your project involves significant larger tree removal, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 16. BRUSH CLEARING MOORESVILLE NC
    # =========================================================================
    "brush-clearing-mooresville-nc": {
        "city_name": "Mooresville",
        "target": """<h3>Brush Clearing Cost in Mooresville ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Mooresville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your parcel falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong> along Lake Norman coves and creek draws, and (4) <strong>rocks that equipment must navigate around</strong>. Unlike a tractor bush hog that cannot handle steep lakefront slopes or thick saplings, our tracked rotary drum mulcher shreds woody brush in place with low ground pressure—and right next to fences, riprap, seawall edges, and utility pedestals, we switch to hand saws and trimmers so structures stay protected.</p>""",
        "replacement": """<h3>Mooresville Brush Clearing Methods: Lake Slopes, Pastures &amp; HOA Ponds</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Mooresville / Lake Norman Area</th>
                    <th scope="col">Our Mechanical Method</th>
                    <th scope="col">Shoreline &amp; Slope Protection</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Vacant Lake Lots &amp; Steep Cove Margins</strong> (Brawley School Rd, Perth Rd, Williamson Rd, Morrison Plantation)</td>
                    <td>Low-ground-pressure tracked mulcher (no minimum pass width needed) + hand trimming near riprap/seawalls</td>
                    <td>Opens walkable sightlines from street to buffer while respecting the Duke Energy 760-ft contour &amp; 50-ft shoreline buffer</td>
                  </tr>
                  <tr>
                    <td><strong>Farm Fences, Ditches &amp; HOA Ponds East of I-77</strong> (NC-150, NC-115, Shearers Rd, Mazeppa Rd, NC-3)</td>
                    <td>Pre-walk wire/utility flagging + rotary mulching + hand tools around concrete outlet risers</td>
                    <td>Clears willow, sweetgum, and briars with zero chemical sprays or burn piles near Dye, Reed, and Back Creeks</td>
                  </tr>
                  <tr>
                    <td><strong>Heavy Saplings &amp; Trees 8&Prime; or Wider</strong> (Overgrown holdings &amp; future building footprints)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Removes larger trunks cleanly while complying with Town of Mooresville UDO &amp; Iredell County watershed rules</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Mooresville ($2,000-$8,000 per Acre) &amp; Lake-Lot Pricing</h3>
            <p>Full-acreage brush clearing in Mooresville typically runs <strong>$2,000 to $8,000 per acre</strong> depending on site conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. If you have a sub-acre lake lot off Brawley School Road that needs to be opened up for a surveyor or buyer, or a farm fence line east of I-77, we price kindly and fairly based on access (we can work ourselves a path in without a pre-cleared lane), travel up I-77, steep cove banks, rocks, and hand-detail work along seawalls, riprap, and fences. Our tracked drum mulcher shreds brush and saplings under 8 inches in place, and when a job involves <strong>trees 8 inches or wider</strong>, we can bring in our excavator and haul off the trees if needed.</p>"""
    },

    # =========================================================================
    # 17. BRUSH CLEARING INDIAN TRAIL NC
    # =========================================================================
    "brush-clearing-indian-trail-nc": {
        "city_name": "Indian Trail",
        "target": """<h3>Brush Clearing Cost in Indian Trail ($2,000-$8,000 per Acre) &amp; Method Comparison</h3>
            <p>Brush clearing in Indian Trail typically costs <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. Four site factors determine where your project falls in that range: (1) <strong>thick brush density</strong>, (2) <strong>the amount of tree removal involving trees thicker than 8 inches</strong>, (3) <strong>steep banks or hilly terrain</strong>, and (4) <strong>rocks that equipment must navigate around</strong>. Unlike a tractor bush hog that leaves jagged sapling stubs, our rotary drum mulcher shreds woody stems and briars flush to the ground in a single pass—and if your job requires removing larger trees over 8 inches or hauling debris off site, we scope those items clearly in your written estimate.</p>""",
        "replacement": """<h3>Indian Trail Brush Clearing Methods: Fence Lines, Vacant Lots &amp; HOA Basins</h3>
            <div class="legal-document__table-container">
              <table class="legal-document__clause-table">
                <thead>
                  <tr>
                    <th scope="col">Indian Trail Site Condition</th>
                    <th scope="col">Mechanical Method</th>
                    <th scope="col">Finished Result &amp; Buffer Care</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Backyard Briar Thickets &amp; Fence Corridors</strong> (Idlewild Rd, Chestnut Ln, Wesley Chapel-Stouts Rd, Poplin Rd)</td>
                    <td>Compact tracked mulcher (no minimum pass width required) + hand tools right next to fences and pedestals</td>
                    <td>Opens a clean, walkable mulch lane for fence installation or mowing while protecting mature boundary oaks</td>
                  </tr>
                  <tr>
                    <td><strong>US-74 Vacant Lots, Code Notices &amp; HOA Ponds</strong> (US-74, Old Monroe Rd, Brandon Oaks, Bonterra, Sun Valley)</td>
                    <td>Tracked bank/lot mulching + hand clearing over riprap aprons and concrete outlet risers</td>
                    <td>Meets Town of Indian Trail code deadlines and HOA stormwater inspection standards with zero chemical sprays</td>
                  </tr>
                  <tr>
                    <td><strong>Rural Ditches, Acreage &amp; Trees 8&Prime; or Wider</strong> (Faith Church Rd, Unionville-Indian Trail Rd)</td>
                    <td>Excavator tree removal &amp; optional haul-off (stump grinding/removal quoted separately)</td>
                    <td>Removes trunks 8&Prime;+ outside Crooked Creek &amp; NCDEQ Goose Creek 100-ft / 200-ft buffers (15A NCAC 02B .0607)</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3>Brush Clearing Cost in Indian Trail ($2,000-$8,000 per Acre) &amp; Backyard / Fence Pricing</h3>
            <p>Full-acreage brush clearing in Indian Trail typically ranges from <strong>$2,000 to $8,000 per acre</strong> depending on property conditions, while <strong>stump grinding and full stump removal are quoted separately</strong>. For smaller neighborhood backyards, narrow fence-installation corridors, or HOA detention basins, we don't apply a rigid acreage minimum—instead, we price warmly and fairly based on equipment access (we can work ourselves a path in), travel distance along US-74, drainage slopes, rocks, hidden wire, and hand work around fences and utility boxes. While brush and saplings under 8 inches shred flush to the ground in a single pass, <strong>trees 8 inches or wider take a different approach</strong>—when your project involves significant larger tree removal, we can bring in our excavator and haul off the trees if needed.</p>"""
    },
}

def main():
    os.makedirs(STAGING_DIR, exist_ok=True)
    os.makedirs(DELIV_DIR, exist_ok=True)
    all_diffs = []
    stats = []

    for slug, cfg in CITY_ENRICHMENTS.items():
        orig_path = os.path.join(ROOT, slug, "index.html")
        orig_html = open(orig_path, encoding="utf-8").read()
        target = cfg["target"]
        replacement = cfg["replacement"]

        assert target in orig_html, f"Target not found in {slug}"
        new_html = orig_html.replace(target, replacement, 1)
        new_html = inject_faq_schema(new_html, city_override=cfg["city_name"])

        stage_dir = os.path.join(STAGING_DIR, slug)
        os.makedirs(stage_dir, exist_ok=True)
        with open(os.path.join(stage_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(new_html)

        diff_lines = list(
            difflib.unified_diff(
                orig_html.splitlines(keepends=True),
                new_html.splitlines(keepends=True),
                fromfile=f"a/charlotte-land-clearing/{slug}/index.html",
                tofile=f"b/charlotte-land-clearing/{slug}/index.html",
                n=3,
            )
        )
        all_diffs.append("".join(diff_lines))

        soup_b = BeautifulSoup(orig_html, "html.parser")
        soup_a = BeautifulSoup(new_html, "html.parser")
        wb = len(soup_b.get_text(" ", strip=True).split())
        wa = len(soup_a.get_text(" ", strip=True).split())
        stats.append({
            "slug": f"/{slug}/",
            "city": cfg["city_name"],
            "words_before": wb,
            "words_after": wa,
            "delta_words": wa - wb,
            "tables_after": len(soup_a.find_all("table")),
            "faqs_after": len(soup_a.find_all("details", class_="svc-faq__item")),
        })

    diff_path = os.path.join(DELIV_DIR, "city_batch_proposed_patches.diff")
    with open(diff_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_diffs))

    stats_path = os.path.join(BASE_DIR, "data", "city_batch_stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"Staged {len(stats)} Wave 1 city pages and wrote {diff_path}.")
    for s in stats:
        print(f"  {s['slug']}: {s['words_before']} -> {s['words_after']} (+{s['delta_words']} words), tables={s['tables_after']}, faqs={s['faqs_after']}")

if __name__ == "__main__":
    main()
