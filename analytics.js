/* Replace G-XXXXXXXXXX once with this site's GA4 Measurement ID. */
(function () {
  'use strict';
  var measurementId = 'G-XXXXXXXXXX';
  var storageKey = 'hwj_analytics_consent';
  var validId = /^G-[A-Z0-9]+$/.test(measurementId) && measurementId !== 'G-XXXXXXXXXX';

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', { analytics_storage: 'denied', wait_for_update: 500 });

  function loadAnalytics() {
    if (!validId || document.querySelector('script[data-ga4]')) return;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    script.dataset.ga4 = 'true';
    document.head.appendChild(script);
    window.gtag('js', new Date());
    window.gtag('config', measurementId, { anonymize_ip: true });
  }

  function setConsent(allowed) {
    localStorage.setItem(storageKey, allowed ? 'granted' : 'denied');
    window.gtag('consent', 'update', { analytics_storage: allowed ? 'granted' : 'denied' });
    if (allowed) loadAnalytics();
    var banner = document.getElementById('analytics-consent');
    if (banner) banner.remove();
  }

  function banner() {
    var el = document.createElement('aside');
    el.id = 'analytics-consent';
    el.setAttribute('aria-label', 'Analytics preferences');
    el.innerHTML = '<div><strong>Help us improve HWJ Valets</strong><p>We use optional Google Analytics cookies to understand visits and improve the site. You can accept or decline.</p></div><div class="consent-actions"><button type="button" data-consent="deny">Decline</button><button type="button" class="accept" data-consent="allow">Accept analytics</button></div>';
    document.body.appendChild(el);
    el.addEventListener('click', function (event) {
      var choice = event.target.getAttribute('data-consent');
      if (choice) setConsent(choice === 'allow');
    });
  }

  var saved = localStorage.getItem(storageKey);
  if (saved === 'granted') { window.gtag('consent', 'update', { analytics_storage: 'granted' }); loadAnalytics(); }
  else if (saved !== 'denied') { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', banner); else banner(); }

  document.addEventListener('click', function (event) {
    var link = event.target.closest('a');
    if (!link || saved === 'denied') return;
    var href = link.getAttribute('href') || '';
    var type = href.indexOf('tel:') === 0 ? 'phone_click' : href.indexOf('https://wa.me/') === 0 ? 'whatsapp_click' : href.indexOf('mailto:') === 0 ? 'email_click' : '';
    if (type) window.gtag('event', type, { link_url: href });
  });
  document.addEventListener('submit', function (event) {
    if (event.target.matches('form')) window.gtag('event', 'generate_lead', { form_name: 'website_enquiry' });
  });
}());
