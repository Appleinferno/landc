/* ==========================================================================
   LAND CLEARING CHARLOTTE — shared site script
   - Mobile drawer toggle
   - Estimate form handler (POSTs to FORM_ENDPOINT; email fallback until it's set; honeypot; success/error states)
   - FAQPage JSON-LD built from the visible FAQ list (keeps schema = on-page copy)
   ========================================================================== */
(function () {
  // ---- Mobile drawer (Harbor Freight–style Main Menu + Slide-Over Sub-Panels) ----
  var toggleBtn = document.getElementById('clc-mobile-toggle');
  var drawer = document.getElementById('clc-mobile-drawer');
  var hfMain = document.getElementById('clc-hf-main');
  var hfBack = document.getElementById('clc-hf-back');
  var hfTitle = document.getElementById('clc-hf-title');
  var hfClose = document.getElementById('clc-hf-close');

  function showHfPanel(panelId) {
    if (!drawer || !hfMain) return;
    var panels = drawer.querySelectorAll('.hf-sub-panel');
    var triggers = drawer.querySelectorAll('[data-hf-panel]');
    if (!panelId) {
      hfMain.hidden = false;
      panels.forEach(function (p) { p.hidden = true; });
      triggers.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      if (hfBack) hfBack.hidden = true;
      if (hfTitle) hfTitle.hidden = false;
      drawer.scrollTop = 0;
      return;
    }
    var target = document.getElementById(panelId);
    if (!target) return;
    hfMain.hidden = true;
    panels.forEach(function (p) { p.hidden = (p !== target); });
    triggers.forEach(function (b) {
      b.setAttribute('aria-expanded', b.getAttribute('data-hf-panel') === panelId ? 'true' : 'false');
    });
    if (hfBack) hfBack.hidden = false;
    if (hfTitle) hfTitle.hidden = true;
    drawer.scrollTop = 0;
  }

  function setDrawer(open) {
    if (!toggleBtn || !drawer) return;
    drawer.classList.toggle('is-open', open);
    toggleBtn.classList.toggle('is-active', open);
    toggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (!open) showHfPanel(null);
  }

  if (toggleBtn && drawer) {
    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setDrawer(!drawer.classList.contains('is-open'));
    });
    if (hfClose) {
      hfClose.addEventListener('click', function (e) {
        e.stopPropagation();
        setDrawer(false);
      });
    }
    if (hfBack) {
      hfBack.addEventListener('click', function (e) {
        e.stopPropagation();
        showHfPanel(null);
      });
    }
    drawer.querySelectorAll('[data-hf-panel]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        showHfPanel(btn.getAttribute('data-hf-panel'));
      });
    });
    drawer.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setDrawer(false); });
    });
    document.addEventListener('click', function (e) {
      if (!drawer.contains(e.target) && !toggleBtn.contains(e.target)) setDrawer(false);
    });
  }

  // ---- Desktop Services Mega Menu (150ms hover intent, click, Esc, focus management) ----
  var megaItem = document.querySelector('.site-navigation__has-mega');
  var megaTrigger = document.getElementById('clc-mega-trigger');
  var megaMenu = document.getElementById('clc-mega-menu');
  var hoverTimer = null;

  function setMega(open) {
    if (!megaTrigger || !megaMenu) return;
    clearTimeout(hoverTimer);
    megaTrigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    megaMenu.hidden = !open;
  }

  if (megaItem && megaTrigger && megaMenu) {
    megaItem.addEventListener('mouseenter', function () {
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () { setMega(true); }, 150);
    });
    megaItem.addEventListener('mouseleave', function () {
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () { setMega(false); }, 150);
    });
    megaTrigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = megaTrigger.getAttribute('aria-expanded') === 'true';
      setMega(!isOpen);
    });
    megaItem.addEventListener('focusout', function (e) {
      if (!megaItem.contains(e.relatedTarget)) {
        setMega(false);
      }
    });
    megaMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setMega(false); });
    });
    document.addEventListener('click', function (e) {
      if (!megaItem.contains(e.target)) setMega(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') {
      if (megaTrigger && megaTrigger.getAttribute('aria-expanded') === 'true') {
        setMega(false);
        megaTrigger.focus();
      }
      if (drawer && drawer.classList.contains('is-open')) {
        setDrawer(false);
        if (toggleBtn) toggleBtn.focus();
      }
    }
  });

  if (location.search.indexOf('mega=1') !== -1) {
    setMega(true);
  }
  if (location.search.indexOf('drawer=1') !== -1) {
    setDrawer(true);
  }
  if (location.search.indexOf('drawer=land') !== -1) {
    setDrawer(true);
    showHfPanel('clc-hf-panel-land');
  }

  // ---- Estimate forms ----
  // Backend: Formcarry (https://formcarry.com). Submissions are POSTed as JSON with
  // Accept: application/json; Formcarry replies { code: 200, status: "success" }.
  // Each <form> also has action="<endpoint>" method="POST" so it still works without JS.
  // `_gotcha` is Formcarry's honeypot field name (filtered server-side too).
  // If FORM_ENDPOINT is ever emptied, submissions fall back to a prefilled email to FORM_EMAIL.
  var FORM_ENDPOINT = 'https://formcarry.com/s/za8glfgKic_';
  var FORM_EXTRA = {};
  var FORM_EMAIL = 'patrick@landclearingcharlotte.com';
  var HONEYPOT = '_gotcha';

  function formToObject(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) { if (k !== HONEYPOT) data[k] = v; });
    var sel = form.querySelector('select[name="service"], select[name="service-type"]');
    data.page = document.title;
    data.page_url = location.href.split('#')[0];
    if (sel) data.subject = 'Estimate request: ' + sel.options[sel.selectedIndex].text;
    Object.keys(FORM_EXTRA).forEach(function (k) { data[k] = FORM_EXTRA[k]; });
    return data;
  }

  document.querySelectorAll('form[data-estimate-form]').forEach(function (form) {
    var card = form.closest('.svc-form-card') || form.parentElement;
    var errorBox = card.querySelector('.svc-form__error');
    var success = card.querySelector('.svc-form__success');
    var btn = form.querySelector('button[type="submit"]');

    function showSuccess(title, text) {
      if (success && title) success.querySelector('h3').textContent = title;
      if (success && text) success.querySelector('p').textContent = text;
      card.classList.add('is-sent');
      if (success) { success.setAttribute('tabindex', '-1'); success.focus(); }
    }
    function showError() {
      if (errorBox) errorBox.hidden = false;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (errorBox) errorBox.hidden = true;
      var hp = form.querySelector('[name="' + HONEYPOT + '"]');
      if (hp && hp.value) { showSuccess(); return; } // bot: pretend success, send nothing

      var data = formToObject(form);

      if (!FORM_ENDPOINT) {
        var body = Object.keys(data).filter(function (k) { return k !== 'subject'; })
          .map(function (k) { return k + ': ' + data[k]; }).join('\n');
        window.location.href = 'mailto:' + FORM_EMAIL +
          '?subject=' + encodeURIComponent(data.subject || 'Estimate request') +
          '&body=' + encodeURIComponent(body);
        showSuccess('Almost done.', 'Your email app should have opened with your details filled in. Press send and we\'ll call within one business day, or call (828) 576-3931 now.');
        return;
      }

      if (btn) { btn.disabled = true; btn.setAttribute('aria-busy', 'true'); }
      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json().catch(function () { return {}; });
      }).then(function (json) {
        if (json && json.status && json.status !== 'success') throw new Error(json.message || 'Rejected');
        showSuccess();
      }).catch(function () {
        showError();
      }).then(function () {
        if (btn) { btn.disabled = false; btn.removeAttribute('aria-busy'); }
      });
    });
  });

  // ---- FAQPage schema from visible FAQs ----
  var items = document.querySelectorAll('.svc-faq__item');
  if (items.length) {
    var schema = {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: Array.prototype.map.call(items, function (item) {
        return {
          '@type': 'Question',
          name: item.querySelector('.svc-faq__q').textContent.trim(),
          acceptedAnswer: { '@type': 'Answer', text: item.querySelector('.svc-faq__a').textContent.trim() }
        };
      })
    };
    var tag = document.createElement('script');
    tag.type = 'application/ld+json';
    tag.textContent = JSON.stringify(schema);
    document.head.appendChild(tag);
  }

  // ---- Land Clearing Cost Calculator (.buf-estimator) ----
  document.querySelectorAll('.buf-estimator').forEach(function (root) {
    if (root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    var form = root.querySelector('form');
    if (!form) return;
    var fields = form.elements;
    var currency = function (value) {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);
    };
    var areaFormat = function (value) {
      return new Intl.NumberFormat('en-US', { maximumFractionDigits: 4 }).format(value);
    };
    var set = function (name, value) {
      var el = root.querySelector('[data-' + name + ']');
      if (el) el.textContent = value;
    };
    // Owner-confirmed bounds; condition weights and uncertainty are provisional.
    var pricing = { min: 2000, max: 8000, uncertainty: 1000 };
    var goals = [
      'Discuss whether mulch can stay on site and which trees you want to keep.',
      'For construction, confirm stump and root removal, debris handling, and any separate grading or compaction.',
      'For pasture, discuss the finish needed before restoring or maintaining the field.',
      'For access, confirm the route, width, and finish needed for a driveway or trail.'
    ];
    var previousUnit = fields.unit.value;
    var estimate = null;

    function update() {
      var acres = Number(fields.area.value) / (fields.unit.value === 'sqft' ? 43560 : 1);
      var error = root.querySelector('#buf-area-error');
      var valid = fields.area.value.trim() !== '' && Number.isFinite(acres) && acres > 0 && acres <= 1000;
      if (error) error.hidden = valid;
      fields.area.setAttribute('aria-invalid', String(!valid));
      if (!valid) {
        if (error) error.textContent = 'Enter a clearing area greater than 0 and no more than 1,000 acres (43,560,000 square feet).';
        estimate = null;
        set('total', 'Enter a valid area');
        set('rate', 'Your estimate will appear here.');
        return;
      }
      var adjustments = ['density', 'slope', 'ground', 'trees'].map(function (key) {
        var value = Number(fields[key].value);
        set(key, value ? '+' + currency(value) + ' / acre' : '$0');
        return value;
      });
      var base = Math.min(pricing.max, pricing.min + adjustments.reduce(function (a, b) { return a + b; }, 0));
      var low = Math.max(pricing.min, base - pricing.uncertainty);
      var high = Math.min(pricing.max, base + pricing.uncertainty);
      var areaLabel = areaFormat(acres) + (acres === 1 ? ' acre' : ' acres');
      set('total', currency(low * acres) + '–' + currency(high * acres));
      set('rate', currency(low) + '–' + currency(high) + ' per acre · ' + areaLabel);
      set('base', currency(base));
      set('context', base === pricing.min
        ? 'Light growth on mostly flat, clear ground puts this property toward the lower end of the range.'
        : base >= 6500
          ? 'Several demanding conditions put this property toward the higher end. A site visit will confirm equipment access and the work required.'
          : 'Your selected conditions increase the work expected per acre. The breakdown shows how each factor shapes this planning range.');
      set('goal', goals[fields.goal.selectedIndex]);
      var smallNote = root.querySelector('[data-small]');
      if (smallNote) smallNote.hidden = acres >= 1;
      var meter = root.querySelector('[data-meter]');
      if (meter) meter.style.width = Math.max(4, (base - pricing.min) / (pricing.max - pricing.min) * 100) + '%';
      fields.areaSlider.value = Math.min(20, Math.max(0.25, acres));
      var selected = function (key) {
        var checkedInput = Array.from(form.querySelectorAll('input[name="' + key + '"]')).find(function (input) { return input.checked; });
        return checkedInput ? checkedInput.nextElementSibling.querySelector('.buf-choice-label').textContent : '';
      };
      estimate = [
        'Land Clearing Charlotte — planning estimate',
        'Clearing area: ' + areaLabel,
        'Purpose: ' + fields.goal.value,
        'Conditions: ' + ['density', 'slope', 'ground', 'trees'].map(selected).join('; '),
        'Estimated total: ' + currency(low * acres) + '–' + currency(high * acres),
        'Estimated per acre: ' + currency(low) + '–' + currency(high),
        'Provisional condition adjustments; not a quote. Stump removal, hauling, grading, permits, and minimum charges need confirmation.',
        'Free on-site estimate: (828) 576-3931 | https://landclearingcharlotte.com/#estimate-form'
      ].join('\n');
    }

    fields.unit.addEventListener('change', function () {
      var value = Number(fields.area.value);
      if (Number.isFinite(value) && value > 0) {
        fields.area.value = String(previousUnit === 'acres' ? value * 43560 : Number((value / 43560).toFixed(8)));
      }
      previousUnit = fields.unit.value;
      fields.area.max = previousUnit === 'acres' ? '1000' : '43560000';
      fields.area.min = previousUnit === 'acres' ? '0.00000001' : '0.0004356';
      update();
    });

    fields.areaSlider.addEventListener('input', function () {
      fields.area.value = Number(fields.areaSlider.value) * (fields.unit.value === 'sqft' ? 43560 : 1);
      update();
    });

    form.addEventListener('input', update);
    form.addEventListener('change', update);
    form.addEventListener('submit', function (event) { event.preventDefault(); });
    form.addEventListener('reset', function () {
      setTimeout(function () {
        previousUnit = 'acres';
        fields.area.max = '1000';
        fields.area.min = '0.01';
        set('status', '');
        update();
      }, 0);
    });

    var copyBtn = root.querySelector('[data-copy]');
    if (copyBtn) {
      copyBtn.addEventListener('click', async function () {
        if (!estimate) {
          set('status', 'Enter a valid area before copying your estimate.');
          fields.area.focus();
          return;
        }
        try {
          await navigator.clipboard.writeText(estimate);
          set('status', 'Estimate copied. Paste it into your notes or inquiry.');
        } catch (err) {
          set('status', 'Copy is unavailable in this browser. Use Print estimate to save a copy.');
        }
      });
    }

    var printBtn = root.querySelector('[data-print]');
    if (printBtn) {
      printBtn.addEventListener('click', function () {
        if (!estimate) {
          set('status', 'Enter a valid area before printing your estimate.');
          fields.area.focus();
          return;
        }
        window.print();
      });
    }

    var ctaBtn = root.querySelector('.buf-result .buf-button');
    if (ctaBtn) {
      ctaBtn.addEventListener('click', function () {
        if (!estimate) return;
        var notesField = document.querySelector('form[data-estimate-form] textarea');
        if (notesField && !notesField.value.trim()) {
          notesField.value = estimate;
        }
      });
    }

    update();
  });
})();

