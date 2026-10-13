# Land Clearing Charlotte — Website Architecture & Style Guide

This website was built using the **Modern Blue-Collar / Premium Trade** design system and the **Tree Node BEM naming architecture**.

---

## 1. Tree Node BEM Architecture

In this system, classes mirror an abstract computer science tree node structure:

```
        [ Root Node: Overall Purpose ]          <-- Block
                 /            \
  [ Child: Location A ]    [ Child: Location B ] <-- Element (__child)
          /        \
  [ Leaf: Styling 1 ]  [ Leaf: Styling 2 ]       <-- Modifier (--leaf)
```

### Tree Node Schema Mapping

| Level | Role in Tree | BEM Equivalent | Purpose / Meaning | Real Example in Site |
| :--- | :--- | :--- | :--- | :--- |
| **Root Node** | Root Container | **Block** | The overall purpose of the component/feature | `service-catalog`, `work-process`, `hero-intro` |
| **Child Node** | Internal Node | **Element** (`__`) | The anatomical location of the sub-element | `__head-zone`, `__grid-card`, `__card-action`, `__foot-actions` |
| **Leaf Node** | Terminal Leaf | **Modifier** (`--`) | The visual styling variant or role | `--gold-underline`, `--elevated-white`, `--pill-gold`, `--arrow-slide-link` |

### Concrete Code Examples from the Site

1. **Services Grid Item:**
   - **Root (Purpose):** `service-catalog`
   - **Child (Location):** `service-catalog__grid-card`
   - **Leaf (Styling):** `service-catalog__grid-card--elevated-white`

2. **Section Eyebrow:**
   - **Root (Purpose):** `service-catalog`
   - **Child (Location):** `service-catalog__head-eyebrow`
   - **Leaf (Styling):** `service-catalog__head-eyebrow--gold-underline`

3. **Call-to-Action Button:**
   - **Root (Purpose):** `service-catalog`
   - **Child (Location):** `service-catalog__action-btn`
   - **Leaf (Styling):** `service-catalog__action-btn--pill-gold`

---

## 2. Design System Tokens

- **Navy (`--clc-navy`):** `#1B2B48` (Primary brand color, dark typography, button borders)
- **Gold (`--clc-gold`):** `#F2C84B` (Safety gold, card accent bars, primary pill buttons, underlines)
- **Gold Dark (`--clc-gold-dark`):** `#E0B431` (Hover state for gold buttons and accents)
- **Slate Text (`--clc-text`):** `#51607A` (Body paragraphs and descriptions)
- **Background Tint (`--clc-tint`):** `#F8F9FB` (Soft cool background surface)
- **Card Surface (`--clc-white`):** `#FFFFFF` (Card background with 5px top gold accent strip)
- **Card Shadows:**
  - Base: `0 14px 34px rgba(27, 43, 72, 0.10)`
  - Hover: `0 22px 46px rgba(27, 43, 72, 0.18)` with `transform: translateY(-5px)`

---

## 3. Canonical Business & Contact Details

All site pages, templates, scripts, and AI-generated content must use these standardized contact details:

- **Business Name:** Land Clearing Charlotte
- **Primary Phone (Display):** `(828) 576-3931`
- **Call Anchor (tel link):** `href="tel:8285763931"`
- **Schema JSON-LD (`telephone`):** `"+1-828-576-3931"`
- **Meta Description Format:** `Free estimates: (828) 576-3931.`
- **Operating Hours:** Mon - Sat: 7:00 AM - 6:30 PM
- **Primary Service Counties:** Charlotte, Mecklenburg, Union, Cabarrus & Gaston Counties, NC

---

## 4. Directory Layout

```
charlotte-land-clearing/
├── images/
│   ├── after-land-clearing.png
│   ├── before-land-clearing.png
│   ├── finished-site-prep.png
│   ├── forestry-mulcher-active.png
│   ├── full-lot-clearing.png
│   └── work-in-progress.png
├── lot-clearing-tips/
│   └── index.html             # Resources & Blog Category page (/lot-clearing-tips/)
├── privacy-policy/
│   └── index.html             # Privacy Policy page (/privacy-policy/)
├── cookies-policy/
│   └── index.html             # Cookies & Tracking Policy page (/cookies-policy/)
├── terms-and-conditions/
│   └── index.html             # Terms & Conditions page (/terms-and-conditions/)
├── index.html                 # Homepage using Tree Node BEM
├── style.css                  # Unified design system & responsive styling
└── README.md                  # Documentation and design system overview
```

### Specialized Tree Node BEM Modules:
- **`legal-document`:** Standardized legal policy container (`--elevated-white`, `--highlight-gold-border`) with interactive tab switcher, clause headings, data tracking tables, and contact details.
- **`resource-hero`:** Search bar, eyebrow, and hero value proposition.
- **`topic-filter`:** Interactive category filter chips (`--active-gold`, `--pill-outline-navy`).
- **`featured-article`:** High-priority spotlight card with 2-column media & content.
- **`article-catalog`:** 3-column responsive card grid displaying 12 educational articles with category badges, reading times, dates, and sliding arrow links.
- **`catalog-pagination`:** Page numbering controls (`--active-gold`, `--pill-shape`).
- **`resource-cta`:** Bottom consultation trigger banner.

---

## 5. Templated Prompt to Build New Sections

To build any additional section (e.g. FAQ, Pricing, Equipment Specs) matching this exact style and Tree Node BEM structure, fill out the following template:

```markdown
Build a new section for the Land Clearing Charlotte website using the exact design system and Tree Node BEM naming structure (Root Node = Purpose, Child Node = Location, Leaf Node = Styling).

- **Section Purpose (Root Node):** [e.g., equipment-fleet / faq-accordion / pricing-estimator]
- **Section Eyebrow:** [e.g., "HEAVY-DUTY MACHINERY"]
- **Section Heading:** [e.g., "Commercial Mulching & Clearing Equipment Built for Any Terrain"]
- **Description:** [Brief 1-2 sentence overview]
- **Layout & Location Elements (Child Nodes):** [e.g., __head-zone, __grid-wrapper, __spec-card, __card-title, __foot-actions]
- **Styling Leaves (Leaf Nodes):** [e.g., --gold-underline, --elevated-white, --pill-gold]
- **Number of Cards / Items:** [e.g., 3 equipment cards with horsepower, cutting diameter, and application]
- **CTA Action:** [e.g., "Reserve Equipment for Your Job" button]
```
