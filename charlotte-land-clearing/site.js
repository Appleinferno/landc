/* ==========================================================================
   LAND CLEARING CHARLOTTE — shared site script
   - Mobile drawer toggle
   - Estimate form handler (POSTs to FORM_ENDPOINT; email fallback until it's set; honeypot; success/error states)
   - FAQPage JSON-LD built from the visible FAQ list (keeps schema = on-page copy)
   ========================================================================== */
(function () {
  // ---- Mobile drawer ----
  var toggleBtn = document.getElementById('clc-mobile-toggle');
  var drawer = document.getElementById('clc-mobile-drawer');

  function setDrawer(open) {
    if (!toggleBtn || !drawer) return;
    drawer.classList.toggle('is-open', open);
    toggleBtn.classList.toggle('is-active', open);
    toggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
  }

  if (toggleBtn && drawer) {
    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      setDrawer(!drawer.classList.contains('is-open'));
    });
    drawer.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setDrawer(false); });
    });
    document.addEventListener('click', function (e) {
      if (!drawer.contains(e.target) && !toggleBtn.contains(e.target)) setDrawer(false);
    });
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
})();
