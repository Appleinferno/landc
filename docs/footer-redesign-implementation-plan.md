# Land Clearing Charlotte — Footer Redesign Implementation Plan (AI Handoff Spec)

**Target site directory:** `charlotte-land-clearing/` (54 static HTML files across 3 folder depths)  
**Stylesheet:** `charlotte-land-clearing/style.css`  
**Generator dependency:** `charlotte-land-clearing/land-clearing-charlotte-nc/index.html` (which `tools/gen/lib.py` reads dynamically via `CLOSING`)  
**Reference mockup:** `RECOMMENDED FOOTER (PRIMARY)` (Desktop) + `MOBILE FOOTER (EXAMPLE)` (Mobile)

> **Status (2026-11-08): implemented locally, not yet committed or deployed.** Old footer rules were removed from `style.css` and replaced in place by the Step 1 block; Steps 3–4 were run (54 live + 21 staged pages); `tools/gen/build_cities.py` was updated to sync the Service Areas list in the new `<details>` markup. `tools/qa.py`: BROKEN 0, same 43 pre-existing issues as before the change.

---

## 1. Architecture & Design Decisions

1. **Single Responsive DOM (No Duplicate Menus for Googlebot):**
   - Instead of rendering two separate sets of navigation links (one for desktop, one for mobile), each of the three link columns (`Core Services`, `Service Areas`, `Resources & Legal`) uses a native `<details class="site-footer__accordion">` element **without** the `open` attribute.
   - **On Desktop (`> 900px`):** CSS forces the group content visible via `::details-content`, disables pointer events on `<summary>`, and hides the mobile down-chevron, so the lists are permanently expanded.
   - **On Mobile (`<= 900px`):** the groups start collapsed natively, exactly as in the `MOBILE FOOTER (EXAMPLE)` mockup, while remaining keyboard-accessible and crawlable.
   - **No runtime JavaScript** in modern browsers. A one-line inline fallback (inside the footer markup) covers only pre-2025 browsers without `::details-content`. See Step 2.
   - **Layout tiers:** 5 columns at `>= 1440px`; the same 5 columns with tighter type at `1280–1439px`; tablet (brand row + 3 link columns + full-width card with a 2-column contact list) at `901–1279px`; mobile accordions at `<= 900px`.
2. **Direct-Mail Address Preserved in Footer Only:**
   - Per operator instructions, `1930 Camden Rd Ste 238, Charlotte, NC 28203` **must remain in the footer** for direct mail verification, and **must not** be added to headers, body copy, or JSON-LD schema.
   - On desktop, the full street address displays inside the `"Get in Touch"` card. On mobile, it stays in the DOM inside the contact block so direct-mail crawlers and mobile users both have access.
3. **Zero External Image Dependencies Required:**
   - The brand logo (`images/logo/lockup-on-navy.svg`) and all 9 social/Trustpilot SVG icons already exist in the codebase.
   - All new icons (Pine Tree, Forestry Mulcher, Brush Leaf, Shield Check, Down Chevron, Phone, Mobile Phone, Map Pin, Envelope, Document for Quotes, Clock, Quote Calendar, Arrow) are provided below as **inline SVGs**. The gold link chevrons are drawn in CSS (`.site-footer__link-item::after`), and the decorative background layers (topographic contour lines + pine-forest silhouette) are **CSS data-URIs**. No external `.png` or `.webp` downloads are needed.
4. **Mobile Sticky CTA Clearance:**
   - Pages have a fixed bottom bar (`aside.mobile-sticky-cta`, height ~74px) on viewports `<= 768px`. The CSS below preserves `padding-bottom: calc(26px + 74px + env(safe-area-inset-bottom, 0px))` on `.site-footer` at `<= 768px` so the bottom social icons and copyright are never covered.

---

## 2. Step-by-Step Instructions for the Implementing Agent

Follow these steps in exact order. **Do not** manually edit 54 HTML files by hand—use the Python propagation script in Step 3.

### Step 1: Update `charlotte-land-clearing/style.css`

Open `charlotte-land-clearing/style.css` and **append** the following self-contained CSS block at the very end of the file (this cleanly overrides the legacy `.site-footer` rules at lines 1359–1445, 2004–2075, and 3039–3083 without breaking any other component):

```css
/* ==========================================================================
   REDESIGNED SITE FOOTER (Desktop 5-Col + "Get in Touch" Card + Mobile Accordions)
   Zero runtime JS: desktop keeps the <details> groups expanded via
   ::details-content; mobile starts collapsed because the HTML has no `open`.
   Built and verified in land-clearing-charlotte/footer-preview/.
   ========================================================================== */

/* Footer-scoped tokens (scoped to .site-footer so nothing else is affected).
   --clc-gold, --clc-navy and --clc-font-family already exist in :root. */
.site-footer {
  --clc-navy-ink: #0E192D;
  --clc-gold-deep: #E7B227;
  --font-display: var(--clc-font-family);
  --ft-bg: #0c1628;
  --ft-text: rgba(226, 232, 240, 0.88);
  --ft-text-dim: rgba(226, 232, 240, 0.74);
  --ft-rule: rgba(255, 255, 255, 0.13);
  --ft-gutter: clamp(20px, 3vw, 40px);
}

.site-footer {
  position: relative;
  background-color: var(--ft-bg);
  background-image:
    /* Top-left topographic contour lines */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='420' height='300' viewBox='0 0 420 300' fill='none' stroke='%23ffffff' stroke-opacity='.05' stroke-width='1.2'%3E%3Cpath d='M-20 250C40 236 80 170 140 142S250 120 320 40 400 -10 420 -20'/%3E%3Cpath d='M-20 220C35 206 70 150 125 124S230 100 296 28 370 -20 390 -30'/%3E%3Cpath d='M-20 190C30 176 62 128 110 106S205 84 268 18 340 -26 360 -36'/%3E%3Cpath d='M-20 160C24 148 54 108 96 88S182 68 240 8 310 -30 330 -40'/%3E%3Cpath d='M-20 128C18 118 44 86 80 70S156 52 208 0'/%3E%3Cpath d='M-20 96C14 88 34 64 62 52S128 38 172 -4'/%3E%3Cpath d='M-20 64C8 58 24 42 46 34S98 24 132 -6'/%3E%3Cpath d='M-20 280C46 266 96 196 160 166S276 144 350 60 420 10 440 0'/%3E%3C/svg%3E"),
    /* Pine forest silhouette, clustered center-right like the mockup */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 220' preserveAspectRatio='xMidYMax meet'%3E%3Cdefs%3E%3ClinearGradient id='f' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%230a1424' stop-opacity='.5'/%3E%3Cstop offset='1' stop-color='%23070e1b' stop-opacity='.95'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath fill='%2314243f' fill-opacity='.55' d='M38 127L45 140L40 137L47 153L41 150L49 166L42 164L51 180L42 177L53 193L43 190L54 206L40 219L36 219L21 206L32 190L23 193L33 177L25 180L34 164L26 166L34 150L28 153L35 137L30 140ZM99 122L107 136L102 133L109 149L103 147L111 163L103 160L113 177L104 174L115 191L105 188L117 205L101 219L97 219L82 205L94 188L84 191L94 174L85 177L95 160L87 163L96 147L89 149L96 133L91 136ZM151 156L156 164L153 163L157 172L153 171L158 181L154 179L159 189L154 187L160 197L154 195L161 205L152 213L150 213L141 205L148 195L142 197L148 187L143 189L149 179L144 181L149 171L145 172L149 163L146 164ZM181 113L190 131L184 128L193 149L185 146L195 167L186 164L197 185L187 182L200 203L183 218L179 218L162 203L175 182L165 185L176 164L167 167L177 146L170 149L178 128L172 131ZM283 92L293 110L286 106L295 127L287 124L298 145L288 141L300 163L289 159L302 180L290 177L305 198L285 215L280 215L261 198L276 177L263 180L276 159L265 163L277 141L268 145L278 124L270 127L279 106L273 110ZM361 97L370 113L364 110L372 130L365 127L375 147L366 143L377 164L366 160L379 181L367 177L382 197L363 214L358 214L339 197L354 177L342 181L355 160L344 164L355 143L346 147L356 127L349 130L357 110L351 113ZM378 89L388 107L381 103L391 125L382 121L393 143L383 140L396 162L384 158L398 180L385 176L401 198L380 216L375 216L355 198L370 176L357 180L371 158L360 162L372 140L362 143L373 121L365 125L374 103L367 107ZM434 109L442 126L437 123L445 144L438 141L447 162L438 159L450 180L439 176L452 197L436 212L431 212L415 197L428 176L417 180L429 159L420 162L429 141L422 144L430 123L425 126ZM454 127L462 142L457 139L464 157L458 154L466 172L458 169L468 187L459 184L470 202L456 214L452 214L439 202L449 184L441 187L450 169L443 172L451 154L445 157L452 139L447 142ZM513 91L524 112L517 108L527 133L518 129L529 154L519 150L532 175L520 172L535 196L516 214L510 214L491 196L506 172L494 175L507 150L497 154L508 129L500 133L509 108L502 112ZM532 39L548 69L538 64L552 99L539 94L556 129L541 124L560 159L542 154L564 189L536 214L529 214L501 189L523 154L505 159L524 124L509 129L526 94L513 99L527 64L517 69ZM548 121L557 138L552 135L559 155L552 152L562 172L553 169L564 189L554 186L566 206L551 220L546 220L531 206L543 186L533 189L544 169L535 172L545 152L538 155L545 135L540 138ZM576 114L584 132L579 129L587 149L580 146L589 167L580 164L592 184L581 181L594 202L578 216L573 216L557 202L570 181L560 184L571 164L562 167L571 146L564 149L572 129L567 132ZM594 69L606 95L598 90L610 120L599 116L613 145L601 141L617 171L602 166L620 196L597 217L590 217L567 196L585 166L571 171L587 141L574 145L588 116L577 120L589 90L581 95ZM760 114L768 126L763 123L770 138L764 135L772 150L764 147L773 162L765 159L775 174L766 171L776 186L766 183L778 198L763 212L758 212L743 198L755 183L744 186L755 171L746 174L756 159L748 162L756 147L749 150L757 135L751 138L758 123L753 126ZM794 79L806 103L799 99L809 127L800 123L813 151L801 146L816 174L802 170L819 198L797 218L791 218L769 198L786 170L773 174L788 146L776 151L789 123L779 127L790 99L782 103ZM839 91L848 107L842 103L851 122L843 118L853 137L844 134L855 153L844 149L857 168L845 164L859 183L846 180L861 199L841 216L836 216L816 199L831 180L818 183L832 164L820 168L833 149L822 153L833 134L824 137L834 118L827 122L835 103L829 107Z'/%3E%3Cpath fill='url%28%23f%29' d='M20 160L25 167L22 165L26 174L22 173L27 182L22 180L28 189L23 187L29 196L23 195L30 204L24 202L31 211L21 219L19 219L9 211L16 202L10 204L17 195L11 196L17 187L12 189L18 180L13 182L18 173L14 174L18 165L15 167ZM55 159L60 169L57 167L62 179L57 178L63 190L58 188L64 200L58 198L66 210L56 219L54 219L44 210L52 198L46 200L52 188L47 190L53 178L48 179L53 167L50 169ZM82 144L89 157L85 154L91 170L85 167L92 183L86 181L94 196L87 194L96 209L84 220L81 220L69 209L78 194L70 196L79 181L72 183L79 167L74 170L80 154L76 157ZM125 131L133 146L128 143L135 161L129 158L137 176L129 173L139 191L130 188L141 206L127 218L123 218L110 206L120 188L112 191L121 173L114 176L122 158L116 161L123 143L118 146ZM210 125L217 136L212 133L218 146L213 144L219 157L213 154L221 168L214 165L222 178L214 176L224 189L215 186L225 199L212 211L208 211L194 199L205 186L196 189L205 176L197 178L206 165L199 168L206 154L200 157L207 144L201 146L207 133L203 136ZM234 122L242 136L237 133L244 149L237 147L245 163L238 160L247 177L239 174L249 191L239 188L251 205L236 218L232 218L216 205L228 188L218 191L229 174L220 177L230 160L222 163L230 147L224 149L231 133L226 136ZM252 122L260 133L255 130L261 144L256 141L263 155L256 152L264 166L257 163L266 177L257 175L267 188L258 186L269 200L254 212L251 212L236 200L247 186L238 188L248 175L239 177L248 163L241 166L249 152L242 155L249 141L244 144L250 130L245 133ZM300 142L306 152L302 149L307 161L303 159L309 171L303 168L310 180L304 178L311 190L304 187L313 199L304 197L314 209L302 219L298 219L286 209L295 197L287 199L296 187L289 190L296 178L290 180L297 168L291 171L297 159L292 161L298 149L294 152ZM329 82L340 101L333 97L342 121L334 117L345 140L334 136L348 159L335 155L350 179L336 175L353 198L331 217L326 217L304 198L321 175L307 179L322 155L309 159L323 136L312 140L324 117L315 121L325 97L317 101ZM395 94L404 108L398 105L406 123L399 119L408 137L400 134L410 152L401 148L412 166L401 163L414 181L402 177L416 195L398 212L392 212L374 195L388 177L376 181L389 163L378 166L389 148L380 152L390 134L382 137L391 119L384 123L392 105L386 108ZM416 97L426 117L420 113L428 136L420 133L431 156L421 152L434 175L422 172L436 195L418 210L414 210L396 195L410 172L398 175L411 152L401 156L412 133L404 136L413 113L406 117ZM483 84L493 101L487 97L496 118L487 114L498 134L488 130L500 151L489 147L502 167L490 163L505 184L491 180L507 201L486 219L480 219L458 201L475 180L461 184L476 163L463 167L476 147L465 151L477 130L467 134L478 114L470 118L479 97L472 101ZM611 103L621 123L615 120L624 143L616 139L627 163L617 159L629 183L618 179L632 202L614 218L609 218L591 202L605 179L593 183L606 159L596 163L607 139L599 143L608 120L602 123ZM631 47L644 67L636 62L647 87L637 83L650 108L638 103L652 128L639 123L655 148L640 143L658 168L641 163L661 188L635 211L628 211L602 188L622 163L604 168L623 143L607 148L623 123L610 128L624 103L613 108L625 83L615 87L626 62L618 67ZM653 86L664 108L657 104L667 130L658 126L670 152L659 148L673 174L660 171L676 197L655 215L650 215L629 197L645 171L632 174L646 148L635 152L647 126L638 130L648 104L641 108ZM675 107L683 120L678 117L685 133L679 130L687 146L679 143L689 159L680 156L691 173L681 169L692 186L681 182L694 199L677 214L673 214L656 199L669 182L658 186L669 169L659 173L670 156L661 159L671 143L663 146L671 130L665 133L672 117L666 120ZM706 44L719 65L710 60L722 86L711 81L724 106L712 101L727 127L713 122L730 147L714 142L733 168L715 163L736 188L709 212L702 212L675 188L696 163L678 168L697 142L681 147L698 122L684 127L699 101L687 106L700 81L689 86L701 60L692 65ZM736 112L744 126L739 123L746 140L740 137L748 154L740 151L750 168L741 165L752 182L742 179L754 196L738 210L734 210L718 196L730 179L720 182L731 165L722 168L732 151L724 154L732 137L726 140L733 123L728 126ZM816 99L826 114L820 110L828 129L821 125L830 143L821 140L832 158L822 155L834 173L823 170L836 188L823 184L838 203L819 220L814 220L795 203L809 184L797 188L810 170L799 173L811 155L801 158L811 140L803 143L812 125L805 129L813 110L807 114ZM868 123L876 134L871 132L877 146L871 143L879 157L872 155L880 169L872 166L882 181L873 178L883 192L874 189L885 204L870 217L866 217L851 204L863 189L853 192L863 178L854 181L864 166L856 169L864 155L857 157L865 143L859 146L865 132L861 134ZM891 112L900 130L894 127L903 148L895 145L905 167L896 163L908 185L897 182L910 203L893 218L889 218L872 203L885 182L874 185L886 163L877 167L887 145L879 148L888 127L882 130ZM908 111L916 123L911 120L918 136L911 133L919 149L912 146L921 161L912 158L923 174L913 171L924 187L914 184L926 199L910 214L905 214L889 199L902 184L891 187L902 171L893 174L903 158L894 161L903 146L896 149L904 133L898 136L905 120L899 123ZM941 119L950 136L944 133L952 153L945 150L955 171L946 168L957 188L947 185L959 205L943 219L939 219L923 205L936 185L926 188L937 168L928 171L937 150L930 153L938 133L933 136ZM972 126L980 142L975 139L982 158L975 155L984 174L976 171L986 190L977 187L988 206L974 219L970 219L955 206L966 187L957 190L967 171L959 174L968 155L962 158L969 139L964 142Z'/%3E%3C/svg%3E"),
    /* Soft fog glow behind the trees */
    radial-gradient(60% 45% at 62% 88%, rgba(44, 72, 112, 0.42) 0%, rgba(12, 22, 40, 0) 70%),
    linear-gradient(180deg, #0f1c33 0%, #0b1425 100%);
  background-repeat: no-repeat;
  background-position: left top, right 26% bottom 70px, center, center;
  background-size: 420px 300px, min(1100px, 92%) auto, 100% 100%, 100% 100%;
  color: var(--ft-text);
  border-top: 4px solid var(--clc-gold);
  padding: 64px 0 26px;
  font-size: 0.95rem;
  overflow: hidden;
}

.site-footer a {
  -webkit-tap-highlight-color: transparent;
}

.site-footer a:focus-visible,
.site-footer summary:focus-visible {
  outline: 2px solid var(--clc-gold);
  outline-offset: 3px;
  border-radius: 4px;
}

.site-footer__container-inner {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 var(--ft-gutter);
}

.site-footer__grid {
  display: grid;
  /* Link columns size to their content so no link ever wraps;
     brand + card share the remaining space. */
  grid-template-columns: minmax(250px, 1fr) auto auto auto minmax(310px, 1fr);
  column-gap: clamp(24px, 2.4vw, 52px);
  align-items: start;
  margin-bottom: 40px;
}

/* --- Column 1: Brand --- */
.site-footer__brand-col {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-top: 26px;
}

.site-footer__brand-link {
  display: block;
  width: 100%;
  max-width: 320px;
}

.site-footer__brand-logo {
  height: auto;
  width: 100%;
  max-width: 320px;
  margin-bottom: 22px;
}

.site-footer__brand-desc {
  color: var(--ft-text);
  font-size: 1rem;
  line-height: 1.55;
  margin: 0 0 26px;
  max-width: 34em;
}

.site-footer__badges {
  width: 100%;
  max-width: 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.site-footer__service-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  width: 100%;
}

.site-footer__service-mini {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
  padding: 2px 8px;
  border-right: 1px solid rgba(255, 255, 255, 0.22);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 500;
  line-height: 1.2;
}

.site-footer__service-mini:last-child {
  border-right: 0;
}

.site-footer__service-mini svg {
  color: var(--clc-gold);
  width: 34px;
  height: 34px;
}

.site-footer__insured-pill {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 11px 26px;
  border-radius: 12px;
  border: 1.5px solid var(--clc-gold);
  background: rgba(10, 18, 33, 0.6);
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
}

.site-footer__insured-pill svg {
  color: var(--clc-gold);
  width: 26px;
  height: 26px;
  flex-shrink: 0;
}

/* --- Columns 2–4: link groups (native <details>) --- */
.site-footer__accordion {
  margin: 0;
  padding: 0;
}

.site-footer__accordion-summary {
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #fff;
  font-family: var(--font-display);
  font-size: 1.12rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  line-height: 1.2;
  white-space: nowrap;
  padding: 26px 0 14px;
  margin-bottom: 26px;
  border-bottom: 3px solid var(--clc-gold);
}

.site-footer__accordion-summary::-webkit-details-marker {
  display: none;
}

.site-footer__accordion-chev {
  display: none;
  flex-shrink: 0;
  color: var(--clc-gold);
  transition: transform 0.2s ease;
}

.site-footer__links-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.site-footer__links-list li + li {
  margin-top: 14px;
}

.site-footer__link-item {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: var(--ft-text);
  text-decoration: none;
  font-size: 1rem;
  line-height: 1.35;
  white-space: nowrap;
  transition: color 0.18s ease;
}

/* Gold chevron drawn in CSS: no extra DOM, no glyph-dependent sizing */
.site-footer__link-item::after {
  content: "";
  width: 7px;
  height: 7px;
  flex-shrink: 0;
  border-top: 2.2px solid var(--clc-gold);
  border-right: 2.2px solid var(--clc-gold);
  transform: rotate(45deg);
  transition: transform 0.18s ease;
}

.site-footer__link-item:hover,
.site-footer__link-item:focus-visible {
  color: var(--clc-gold);
}

.site-footer__link-item:hover::after {
  transform: translateX(3px) rotate(45deg);
}

/* Town listed before its page exists (emitted by tools/gen/build_cities.py) */
.site-footer__link-item--muted,
.site-footer__link-item--muted:hover {
  color: var(--ft-text-dim);
  cursor: default;
}

.site-footer__link-item--muted::after {
  display: none;
}

/* --- Column 5: "Get in Touch" card --- */
.site-footer__contact-card {
  background:
    radial-gradient(120% 60% at 100% 0%, rgba(242, 200, 75, 0.09), rgba(242, 200, 75, 0) 60%),
    linear-gradient(180deg, rgba(20, 34, 58, 0.92), rgba(12, 22, 40, 0.94));
  border: 2px solid var(--clc-gold);
  border-radius: 20px;
  padding: 22px 22px 22px;
  box-shadow:
    0 0 0 1px rgba(242, 200, 75, 0.12),
    0 0 26px rgba(242, 200, 75, 0.16),
    0 18px 40px rgba(0, 0, 0, 0.4);
}

.site-footer__contact-head {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 0 4px 16px;
  border-bottom: 1px solid var(--ft-rule);
}

.site-footer__contact-head-icon {
  color: var(--clc-gold);
  width: 42px;
  height: 42px;
  flex-shrink: 0;
}

.site-footer__contact-title {
  font-family: var(--font-display);
  color: #fff;
  font-size: 1.85rem;
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 6px;
}

.site-footer__contact-sub {
  color: var(--ft-text);
  font-size: 0.92rem;
  line-height: 1.35;
  margin: 0;
}

.site-footer__contact-list {
  list-style: none;
  margin: 0 0 18px;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.site-footer__contact-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 9px 0;
  border-bottom: 1px solid var(--ft-rule);
}

.site-footer__contact-row:last-child {
  border-bottom: 0;
}

.site-footer__contact-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--clc-gold);
  flex-shrink: 0;
}

.site-footer__contact-badge svg {
  width: 22px;
  height: 22px;
}

.site-footer__contact-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.site-footer__contact-label {
  color: #fff;
  font-size: 0.92rem;
  font-weight: 700;
  line-height: 1.25;
}

.site-footer__contact-val,
.site-footer__contact-val a {
  color: var(--ft-text);
  font-size: 0.88rem;
  line-height: 1.3;
  text-decoration: none;
  overflow-wrap: break-word;
}

.site-footer__contact-val a:hover {
  color: var(--clc-gold);
  text-decoration: underline;
}

.site-footer__cta-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 14px 18px;
  border-radius: 10px;
  background: linear-gradient(180deg, #F7D466 0%, var(--clc-gold-deep) 100%);
  color: var(--clc-navy-ink);
  font-family: var(--font-display);
  font-size: 1.12rem;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 6px 18px rgba(242, 200, 75, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.45);
  transition: transform 0.18s ease, filter 0.18s ease;
}

.site-footer__cta-btn svg {
  flex-shrink: 0;
}

.site-footer__cta-btn:hover,
.site-footer__cta-btn:focus-visible {
  transform: translateY(-1px);
  filter: brightness(1.05);
}

/* --- Bottom bar: copyright | socials | privacy --- */
.site-footer__bottom-row {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px 24px;
  font-size: 0.86rem;
  color: var(--ft-text);
}

.site-footer__social-wrap {
  display: flex;
  align-items: center;
  gap: 22px;
}

.site-footer__social-wrap::before,
.site-footer__social-wrap::after {
  content: "";
  width: 2px;
  height: 30px;
  background: var(--clc-gold);
  opacity: 0.85;
}

.site-footer__social-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.site-footer__social-list li {
  display: inline-flex;
}

/* :link/:visited included to outrank the legacy rules in the live style.css */
.site-footer__social-link,
.site-footer__social-link:link,
.site-footer__social-link:visited {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
  border: 1.5px solid rgba(255, 255, 255, 0.6);
  color: #fff;
  text-decoration: none;
  transition: color 0.2s ease, background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.site-footer__social-link svg {
  width: 17px;
  height: 17px;
  fill: currentColor;
}

.site-footer__social-link:hover,
.site-footer__social-link:focus-visible {
  color: var(--clc-navy);
  background: var(--clc-gold);
  border-color: var(--clc-gold);
  transform: translateY(-2px);
}

.site-footer__copyright,
.site-footer__privacy-note {
  white-space: nowrap;
}

/* ==========================================================================
   DESKTOP ONLY: keep the <details> groups permanently expanded — no JS.
   ========================================================================== */
@media (min-width: 901px) {
  .site-footer__accordion::details-content {
    content-visibility: visible;
    display: block;
    block-size: auto;
  }

  .site-footer__accordion-summary {
    pointer-events: none;
    cursor: default;
  }
}

/* --- Bottom bar stacks once its three parts can't share one line --- */
@media (max-width: 1399px) {
  .site-footer__bottom-row {
    flex-direction: column;
    text-align: center;
  }
  .site-footer__social-wrap::before,
  .site-footer__social-wrap::after {
    display: none;
  }
}

/* --- Compact desktop (1280–1439px): same 5 columns, tighter type --- */
@media (max-width: 1439px) and (min-width: 1280px) {
  .site-footer__grid {
    grid-template-columns: minmax(250px, 1fr) auto auto auto minmax(316px, 1fr);
    column-gap: 22px;
  }
  .site-footer__accordion-summary { font-size: 1rem; }
  .site-footer__link-item { font-size: 0.93rem; gap: 10px; }
  .site-footer__brand-desc { font-size: 0.95rem; }
  .site-footer__contact-card { padding: 20px 18px; }
  .site-footer__contact-title { font-size: 1.6rem; }
  .site-footer__contact-head-icon { width: 36px; height: 36px; }
  .site-footer__contact-badge { width: 34px; height: 34px; }
  .site-footer__contact-badge svg { width: 19px; height: 19px; }
  .site-footer__contact-row { gap: 12px; }
  .site-footer__contact-val,
  .site-footer__contact-val a { font-size: 0.8rem; }
}

/* --- Tablet (901–1279px): brand row, 3 link columns, full-width card --- */
@media (max-width: 1279px) and (min-width: 901px) {
  .site-footer__grid {
    grid-template-columns: repeat(3, auto);
    justify-content: space-between;
    row-gap: 36px;
  }
  .site-footer__brand-col {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 340px;
    column-gap: 48px;
    align-items: center;
    padding-top: 0;
  }
  .site-footer__brand-desc {
    margin-bottom: 0;
  }
  .site-footer__badges {
    grid-column: 2;
    grid-row: 1 / span 2;
  }
  .site-footer__accordion-summary {
    padding-top: 0;
  }
  .site-footer__contact-card {
    grid-column: 1 / -1;
  }
  .site-footer__contact-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 28px;
  }
  .site-footer__contact-row:nth-last-child(2) {
    border-bottom: 0;
  }
}

/* ==========================================================================
   MOBILE (≤900px) — matches "MOBILE FOOTER (EXAMPLE)"
   ========================================================================== */
@media (max-width: 900px) {
  .site-footer {
    padding: 38px 0 26px;
    border-top-width: 3px;
    /* Mobile mockup is clean: keep the contours, drop the treeline layer */
    background-position: left top, center, center, center;
    background-size: 320px 230px, 0 0, 100% 100%, 100% 100%;
  }

  .site-footer__grid {
    grid-template-columns: minmax(0, 1fr);
    margin-bottom: 26px;
  }

  .site-footer__brand-col {
    padding-top: 0;
    margin-bottom: 22px;
  }

  .site-footer__brand-logo {
    max-width: 252px;
    margin: 0 0 18px;
  }

  .site-footer__brand-link {
    align-self: center;
  }

  .site-footer__brand-desc {
    font-size: 0.98rem;
    line-height: 1.5;
    margin: 0;
  }

  .site-footer__badges {
    display: none;
  }

  /* Accordions */
  .site-footer__accordion {
    border-top: 1px solid rgba(255, 255, 255, 0.2);
  }

  .site-footer__accordion:last-of-type {
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .site-footer__accordion-summary {
    cursor: pointer;
    border-bottom: 0;
    margin: 0;
    padding: 14px 2px;
    font-size: 1.04rem;
    text-transform: none;
    letter-spacing: 0;
  }

  .site-footer__accordion-chev {
    display: block;
  }

  .site-footer__accordion[open] .site-footer__accordion-chev {
    transform: rotate(180deg);
  }

  .site-footer__links-list {
    padding: 0 2px 16px;
  }

  .site-footer__links-list li + li {
    margin-top: 12px;
  }

  .site-footer__link-item {
    white-space: normal;
  }

  /* Card flattens into a plain icon list + gold button */
  .site-footer__contact-card {
    background: none;
    border: 0;
    border-radius: 0;
    padding: 20px 0 0;
    box-shadow: none;
  }

  .site-footer__contact-head,
  .site-footer__contact-label,
  .site-footer__contact-row--after-hours,
  .site-footer__contact-row--quotes {
    display: none;
  }

  .site-footer__contact-list {
    margin-bottom: 16px;
  }

  /* Mockup order: phone, email, location, hours */
  .site-footer__contact-row--phone   { order: 1; }
  .site-footer__contact-row--email   { order: 2; }
  .site-footer__contact-row--address { order: 3; }
  .site-footer__contact-row--hours   { order: 4; }

  .site-footer__contact-row {
    border-bottom: 0;
    padding: 6px 0 6px 8px;
    gap: 14px;
  }

  .site-footer__contact-badge {
    width: 24px;
    height: 24px;
    background: none;
    border: 0;
  }

  .site-footer__contact-badge svg {
    width: 24px;
    height: 24px;
  }

  .site-footer__contact-val,
  .site-footer__contact-val a {
    color: #fff;
    font-size: 0.98rem;
  }

  .site-footer__cta-btn {
    font-size: 1.1rem;
  }

  .site-footer__cta-icon {
    display: none;
  }

  /* Bottom: socials first, then legal lines */
  .site-footer__bottom-row {
    border-top-color: rgba(255, 255, 255, 0.14);
    gap: 18px;
    font-size: 0.8rem;
    color: var(--ft-text-dim);
  }

  .site-footer__social-wrap {
    order: -1;
  }

  /* 9 icons balance as 5 + 4 with 44px tap targets */
  .site-footer__social-list {
    max-width: 268px;
    gap: 12px;
  }

  .site-footer__social-link,
  .site-footer__social-link:link,
  .site-footer__social-link:visited {
    width: 44px;
    height: 44px;
  }

  .site-footer__social-link svg {
    width: 19px;
    height: 19px;
  }

  .site-footer__copyright,
  .site-footer__privacy-note {
    white-space: normal;
  }
}

/* Clearance above the existing mobile sticky CTA bar (bar styles already live) */
@media (max-width: 768px) {
  .site-footer {
    padding-bottom: calc(26px + 74px + env(safe-area-inset-bottom, 0px));
  }
}
```

---

### Step 2: No JavaScript Changes (Do **Not** Touch `site.js` / `script.js`)

An earlier draft of this plan appended a resize-listener helper to `site.js` and `script.js`. **That is no longer needed. Do not add it.**

How the accordions work without JS:
- The three `<details class="site-footer__accordion">` elements are rendered **without** the `open` attribute, so on mobile they start collapsed natively.
- On desktop (`min-width: 901px`) the Step 1 CSS forces their content visible with `.site-footer__accordion::details-content { content-visibility: visible; display: block; }` and disables pointer events on `<summary>`.
- `::details-content` is supported in Chrome/Edge 131+, Safari 18.4+ and Firefox 143+. For older browsers, the footer template in Step 3 ends with a **one-line inline script inside `<footer>`** that runs only when the feature is missing *and* the viewport is desktop-width, opening the groups once. No listeners, no external file, and nothing runs in modern browsers.
- Because the fallback lives inside `<footer>`, the propagation script replaces it along with the footer, so re-running Step 3 stays idempotent.

If a previous attempt already added `syncFooterAccordions` to `site.js` or `script.js`, delete that block.

---

### Step 3: Run the Automated Python Footer Propagation Script across All 54 Pages

Create `tools/apply_footer.py` with the exact code below and run `python tools/apply_footer.py`.

How this script works safely:
- It finds all 54 HTML files in `charlotte-land-clearing/` (including `404.html`, `index.html`, depth-1 folders, and depth-2 `lot-clearing-tips/*` articles), plus the staged city pages in `tools/seo_engine/staging/` (which `deploy_city_batch.py` copies over live pages).
- For each file, it automatically determines the exact relative path prefix (`""`, `"/"`, `"../"`, or `"../../"`) and preserves the page's existing walkthrough CTA target (`#estimate`, `#estimate-form`, `../free-estimate/`, etc.).
- Because `tools/gen/lib.py` dynamically slices `CLOSING` from `charlotte-land-clearing/land-clearing-charlotte-nc/index.html`, updating `land-clearing-charlotte-nc/index.html` automatically updates the generator template too.

```python
"""Propagate the redesigned site-footer across all 54 HTML files in charlotte-land-clearing/."""
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "charlotte-land-clearing")
# Staged city pages are copied over live pages by tools/seo_engine/deploy_city_batch.py,
# so they must carry the new footer too (same folder depth as the live pages).
STAGING = os.path.join(REPO, "tools", "seo_engine", "staging")

FOOTER_TEMPLATE = """  <footer class="site-footer">
    <div class="site-footer__container-inner">

      <div class="site-footer__grid">

        <!-- Column 1: Brand + Service Icons + Insured Pill -->
        <div class="site-footer__brand-col">
          <a class="site-footer__brand-link" href="{home_href}" aria-label="Land Clearing Charlotte Home">
            <img class="site-footer__brand-logo" src="{prefix}images/logo/lockup-on-navy.svg" alt="Land Clearing Charlotte" width="356" height="82">
          </a>
          <p class="site-footer__brand-desc">
            Premier forestry mulching, underbrush mulching, and acreage land clearing across Greater Charlotte and surrounding North Carolina counties.
          </p>
          <div class="site-footer__badges">
          <div class="site-footer__service-strip" aria-label="Core Services Overview">
            <div class="site-footer__service-mini">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2L5 11h4l-3 7h5v4h2v-4h5l-3-7h4L12 2z"/></svg>
              <span>Land<br>Clearing</span>
            </div>
            <div class="site-footer__service-mini">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="10" width="11" height="6" rx="1"/><path d="M6 10V6h5l2 4"/><path d="M14 12h4l3 3v3h-3"/><circle cx="6.5" cy="18" r="2"/><circle cx="11.5" cy="18" r="2"/><path d="M18 11v7"/></svg>
              <span>Forestry<br>Mulching</span>
            </div>
            <div class="site-footer__service-mini">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17 4C8 4 4 11 4 19c0 .6.4 1 1 1s1-.4 1-1c0-3.2 1.8-6.1 4.8-7.7-1.6 2.1-2.5 4.7-2.6 7.7 8 0 12.8-6 12.8-14 0-.6-.4-1-1-1h-3z"/></svg>
              <span>Brush<br>Clearing</span>
            </div>
          </div>
          <div class="site-footer__insured-pill">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z"/><path d="M9 12l2 2 4-4"/></svg>
            <span>Fully Insured in NC</span>
          </div>
          </div>
        </div>

        <!-- Column 2: Core Services -->
        <details class="site-footer__accordion">
          <summary class="site-footer__accordion-summary">
            <span>Core Services</span>
            <svg class="site-footer__accordion-chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
          </summary>
          <ul class="site-footer__links-list">
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-charlotte-nc/">Land Clearing in Charlotte</a></li>
            <li><a class="site-footer__link-item" href="{prefix}forestry-mulching-charlotte-nc/">Forestry Mulching in Charlotte</a></li>
            <li><a class="site-footer__link-item" href="{prefix}brush-clearing-charlotte-nc/">Brush Clearing in Charlotte</a></li>
          </ul>
        </details>

        <!-- Column 3: Service Areas -->
        <details class="site-footer__accordion">
          <summary class="site-footer__accordion-summary">
            <span>Service Areas</span>
            <svg class="site-footer__accordion-chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
          </summary>
          <ul class="site-footer__links-list">
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-huntersville-nc/">Huntersville, NC</a></li>
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-mint-hill-nc/">Mint Hill, NC</a></li>
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-waxhaw-nc/">Waxhaw, NC</a></li>
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-concord-nc/">Concord, NC</a></li>
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-mooresville-nc/">Mooresville, NC</a></li>
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-indian-trail-nc/">Indian Trail, NC</a></li>
          </ul>
        </details>

        <!-- Column 4: Resources & Legal -->
        <details class="site-footer__accordion">
          <summary class="site-footer__accordion-summary">
            <span>Resources &amp; Legal</span>
            <svg class="site-footer__accordion-chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
          </summary>
          <ul class="site-footer__links-list">
            <li><a class="site-footer__link-item" href="{prefix}land-clearing-cost-calculator/">Cost Calculator</a></li>
            <li><a class="site-footer__link-item" href="{prefix}lot-clearing-tips/">Lot Clearing Tips</a></li>
            <li><a class="site-footer__link-item" href="https://www.trustpilot.com/review/landclearingcharlotte.com" target="_blank" rel="noopener noreferrer">Trustpilot Reviews</a></li>
            <li><a class="site-footer__link-item" href="{prefix}privacy-policy/">Privacy Policy</a></li>
            <li><a class="site-footer__link-item" href="{prefix}cookies-policy/">Cookies Policy</a></li>
            <li><a class="site-footer__link-item" href="{prefix}terms-and-conditions/">Terms &amp; Conditions</a></li>
            <li><a class="site-footer__link-item" href="{estimate_href}">Get Free Walkthrough</a></li>
          </ul>
        </details>

        <!-- Column 5: Get in Touch Card -->
        <div class="site-footer__contact-card">
          <div class="site-footer__contact-head">
            <svg class="site-footer__contact-head-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.58a1 1 0 0 1-.25 1.01l-2.2 2.2z"/></svg>
            <div>
              <p class="site-footer__contact-title">Get in Touch</p>
              <p class="site-footer__contact-sub">Questions, quotes, or project planning? We&rsquo;re here to help.</p>
            </div>
          </div>

          <ul class="site-footer__contact-list">
            <li class="site-footer__contact-row site-footer__contact-row--address">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">Address</span>
                <span class="site-footer__contact-val">1930 Camden Rd Ste 238, Charlotte, NC 28203</span>
              </div>
            </li>
            <li class="site-footer__contact-row site-footer__contact-row--phone">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.58a1 1 0 0 1-.25 1.01l-2.2 2.2z"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">Phone</span>
                <span class="site-footer__contact-val"><a href="tel:7047416895">(704) 741-6895</a></span>
              </div>
            </li>
            <li class="site-footer__contact-row site-footer__contact-row--after-hours">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="2" width="12" height="20" rx="2"/><circle cx="12" cy="18" r="1" fill="currentColor"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">After Hours Phone</span>
                <span class="site-footer__contact-val"><a href="tel:8285763931">(828) 576-3931</a></span>
              </div>
            </li>
            <li class="site-footer__contact-row site-footer__contact-row--email">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">Email</span>
                <span class="site-footer__contact-val"><a href="mailto:patrick@landclearingcharlotte.com">patrick@landclearingcharlotte.com</a></span>
              </div>
            </li>
            <li class="site-footer__contact-row site-footer__contact-row--quotes">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 7V3.5L18.5 9H13zM8 13h8v1.6H8V13zm0 3.4h8V18H8v-1.6zM8 9.6h3v1.6H8V9.6z"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">Quotes</span>
                <span class="site-footer__contact-val"><a href="mailto:quotes@landclearingcharlotte.com">quotes@landclearingcharlotte.com</a></span>
              </div>
            </li>
            <li class="site-footer__contact-row site-footer__contact-row--hours">
              <span class="site-footer__contact-badge" aria-hidden="true">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M12 6.5V12l3.5 2.5"/></svg>
              </span>
              <div class="site-footer__contact-info">
                <span class="site-footer__contact-label">Hours</span>
                <span class="site-footer__contact-val">Mon &ndash; Sat: 6:00 AM &ndash; 6:00 PM</span>
              </div>
            </li>
          </ul>

          <a class="site-footer__cta-btn" href="{estimate_href}">
            <svg class="site-footer__cta-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 16l2 2 4-4"/></svg>
            <span>Get a Free Quote</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
        </div>

      </div>

      <div class="site-footer__bottom-row">
        <span class="site-footer__copyright">&copy; 2026 Land Clearing Charlotte. All Rights Reserved. Fully Insured in NC.</span>
        <div class="site-footer__social-wrap">
          <ul class="site-footer__social-list" aria-label="Social Media">
            <li><a class="site-footer__social-link" href="https://www.trustpilot.com/review/landclearingcharlotte.com" target="_blank" rel="noopener noreferrer" aria-label="Trustpilot"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 1.5l3.24 6.57 7.26 1.05-5.25 5.12 1.24 7.23L12 18.06l-6.49 3.41 1.24-7.23L1.5 9.12l7.26-1.05L12 1.5z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.facebook.com/landclearingcharlotte/" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.instagram.com/landclearingcharlotte/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://x.com/landclearingcha" target="_blank" rel="noopener noreferrer" aria-label="X (Twitter)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.pinterest.com/landclearingcharlotte/" target="_blank" rel="noopener noreferrer" aria-label="Pinterest"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.026L12.017 0z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.reddit.com/user/landclearingcha/" target="_blank" rel="noopener noreferrer" aria-label="Reddit"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.373 0 0 5.373 0 12c0 3.314 1.343 6.314 3.515 8.485l-2.286 2.286C.775 23.225 1.097 24 1.738 24H12c6.627 0 12-5.373 12-12S18.627 0 12 0Zm4.388 3.199c1.104 0 1.999.895 1.999 1.999 0 1.105-.895 2-1.999 2-.946 0-1.739-.657-1.947-1.539v.002c-1.147.162-2.032 1.15-2.032 2.341v.007c1.776.067 3.4.567 4.686 1.363.473-.363 1.064-.58 1.707-.58 1.547 0 2.802 1.254 2.802 2.802 0 1.117-.655 2.081-1.601 2.531-.088 3.256-3.637 5.876-7.997 5.876-4.361 0-7.905-2.617-7.998-5.87-.954-.447-1.614-1.415-1.614-2.538 0-1.548 1.255-2.802 2.803-2.802.645 0 1.239.218 1.712.585 1.275-.79 2.881-1.291 4.64-1.365v-.01c0-1.663 1.263-3.034 2.88-3.207.188-.911.993-1.595 1.959-1.595Zm-8.085 8.376c-.784 0-1.459.78-1.506 1.797-.047 1.016.64 1.429 1.426 1.429.786 0 1.371-.369 1.418-1.385.047-1.017-.553-1.841-1.338-1.841Zm7.406 0c-.786 0-1.385.824-1.338 1.841.047 1.017.634 1.385 1.418 1.385.785 0 1.473-.413 1.426-1.429-.046-1.017-.721-1.797-1.506-1.797Zm-3.703 4.013c-.974 0-1.907.048-2.77.135-.147.015-.241.168-.183.305.483 1.154 1.622 1.964 2.953 1.964 1.33 0 2.47-.81 2.953-1.964.057-.137-.037-.29-.184-.305-.863-.087-1.795-.135-2.769-.135Z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.twitch.tv/landclearingcharlotte" target="_blank" rel="noopener noreferrer" aria-label="Twitch"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.snapchat.com/@landclearingcha" target="_blank" rel="noopener noreferrer" aria-label="Snapchat"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.206.793c.99 0 4.347.276 5.93 3.821.529 1.193.403 3.219.299 4.847l-.003.06c-.012.18-.022.345-.03.51.075.045.203.09.401.09.3-.016.659-.12 1.033-.301.165-.088.344-.104.464-.104.182 0 .359.029.509.09.45.149.734.479.734.838.015.449-.39.839-1.213 1.168-.089.029-.209.075-.344.119-.45.135-1.139.36-1.333.81-.09.224-.061.524.12.868l.015.015c.06.136 1.526 3.475 4.791 4.014.255.044.435.27.42.509 0 .075-.015.149-.045.225-.24.569-1.273.988-3.146 1.271-.059.091-.12.375-.164.57-.029.179-.074.36-.134.553-.076.271-.27.405-.555.405h-.03c-.135 0-.313-.031-.538-.074-.36-.075-.765-.135-1.273-.135-.3 0-.599.015-.913.074-.6.104-1.123.464-1.723.884-.853.599-1.826 1.288-3.294 1.288-.06 0-.119-.015-.18-.015h-.149c-1.468 0-2.427-.675-3.279-1.288-.599-.42-1.107-.779-1.707-.884-.314-.045-.629-.074-.928-.074-.54 0-.958.089-1.272.149-.211.043-.391.074-.54.074-.374 0-.523-.224-.583-.42-.061-.192-.09-.389-.135-.567-.046-.181-.105-.494-.166-.57-1.918-.222-2.95-.642-3.189-1.226-.031-.063-.052-.15-.055-.225-.015-.243.165-.465.42-.509 3.264-.54 4.73-3.879 4.791-4.02l.016-.029c.18-.345.224-.645.119-.869-.195-.434-.884-.658-1.332-.809-.121-.029-.24-.074-.346-.119-1.107-.435-1.257-.93-1.197-1.273.09-.479.674-.793 1.168-.793.146 0 .27.029.383.074.42.194.789.3 1.104.3.234 0 .384-.06.465-.105l-.046-.569c-.098-1.626-.225-3.651.307-4.837C7.392 1.077 10.739.807 11.727.807l.419-.015h.06z"/></svg></a></li>
            <li><a class="site-footer__social-link" href="https://www.linkedin.com/company/landclearingcharlotte" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a></li>
          </ul>
        </div>
        <span class="site-footer__privacy-note">We respect user privacy and do not sell data to third parties.</span>
      </div>

    </div>
    <!-- Only for browsers without ::details-content (pre-2025): expand the
         footer link groups once on desktop. Modern browsers skip it entirely. -->
    <script>if(!CSS.supports('selector(::details-content)')&&matchMedia('(min-width:901px)').matches)document.querySelectorAll('.site-footer__accordion').forEach(function(d){{d.open=true}})</script>
  </footer>"""

FOOTER_RE = re.compile(r'  <footer class="site-footer">.*?  </footer>', re.S)

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    files += sorted(glob.glob(os.path.join(STAGING, "**", "*.html"), recursive=True))
    files = [f for f in files if "_shot" not in f]
    updated = 0
    for path in files:
        content = open(path, encoding="utf-8").read()
        m = FOOTER_RE.search(content)
        if not m:
            print(f"SKIP (no footer): {os.path.relpath(path, ROOT)}")
            continue
        old_footer = m.group(0)

        # Detect prefix from existing brand logo src
        logo_m = re.search(r'src="([^"]*?)images/logo/lockup-on-navy\.svg"', old_footer)
        if logo_m:
            prefix = logo_m.group(1)
        else:
            base = STAGING if path.startswith(STAGING) else ROOT
            rel_dir = os.path.relpath(os.path.dirname(path), base)
            if os.path.basename(path) == "404.html":
                prefix = "/"
            elif rel_dir == ".":
                prefix = ""
            else:
                depth = len(rel_dir.split(os.sep))
                prefix = "../" * depth

        # 404.html is served from any path, so it needs root-relative "/"; everything else stays relative
        home_href = "/" if prefix == "/" else (prefix or "./")

        # Detect existing walkthrough / estimate href
        walk_m = re.search(r'href="([^"]+)"[^>]*>(?:<span>)?Get Free Walkthrough', old_footer)
        if walk_m:
            estimate_href = walk_m.group(1)
        elif 'id="estimate"' in content:
            estimate_href = "#estimate"
        elif 'id="estimate-form"' in content:
            estimate_href = "#estimate-form"
        else:
            estimate_href = f"{prefix}free-estimate/"

        new_footer = FOOTER_TEMPLATE.format(
            prefix=prefix,
            home_href=home_href,
            estimate_href=estimate_href,
        )
        new_content = content[:m.start()] + new_footer + content[m.end():]
        if new_content != content:
            open(path, "w", encoding="utf-8", newline="\n").write(new_content)
            updated += 1

    print(f"Updated footer in {updated}/{len(files)} HTML files (live + staging).")

if __name__ == "__main__":
    main()
```

---

### Step 4: Update `tools/qa.py` Phone Validation & Run Verification

1. **Important check in `tools/qa.py`:** Lines 53–61 of `tools/qa.py` were written when only `(828) 576-3931` was on the site. Update lines 53–61 in `tools/qa.py` so both approved numbers (`(704) 741-6895` primary and `(828) 576-3931` after-hours) pass QA without false-positive warnings:
   ```python
   ALLOWED_PHONES = {"(828) 576-3931", "(704) 741-6895", "828-576-3931", "704-741-6895"}
   ALLOWED_TELS = {"8285763931", "7047416895"}
   ```
2. **Run QA:**
   ```powershell
   python tools/qa.py
   ```
   Verify that `BROKEN: 0`, `STALE PROPOSED: 0`, and `SITEMAP missing: [] extra: []` are reported.
3. **Visual check across 3 depths + mobile viewport:**
   - Start the local preview server (`python tools/serve.py`) and inspect:
     - Root page (`http://localhost:8000/`)
     - Depth-1 service page (`http://localhost:8000/land-clearing-concord-nc/`)
     - Depth-2 article page (`http://localhost:8000/lot-clearing-tips/land-clearing-in-western-north-carolina/`)
   - Verify desktop width (`1440px`) matches `RECOMMENDED FOOTER (PRIMARY)` and mobile width (`390px`) matches `MOBILE FOOTER (EXAMPLE)` with collapsible accordions and clearance above the sticky bottom CTA bar.
   - Also check `1280px` (compact 5-column tier: no wrapped headings or links, card email on one line) and `1024px` (tablet layout).
   - Confirm the legacy `.site-footer` rules in `style.css` aren't leaking spacing or colors into the new markup (compare side by side with `land-clearing-charlotte/footer-preview/`).
