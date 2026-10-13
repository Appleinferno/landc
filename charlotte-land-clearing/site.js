/* ==========================================================================
   LAND CLEARING CHARLOTTE — shared site script
   - Mobile drawer toggle
   - Estimate form handler (front-end only until a backend/CRM is connected)
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
  // TODO: replace with a real endpoint (email service / CRM webhook) before launch.
  document.querySelectorAll('form[data-estimate-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var card = form.closest('.svc-form-card');
      if (card) card.classList.add('is-sent');
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
