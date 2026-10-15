/* Yubo Wang homepage — small progressive enhancements, vanilla JS only.
   0. Teasers: lazy for first paint, prefetched during idle time
   1. Theme toggle (follows the OS until the visitor picks; choice saved in localStorage)
   2. Publications: Selected / All toggle (aria-pressed), year groups hide when empty, deep links
   3. News: show the first 6 items, "show all" button for the rest
   4. Section nav: mark the section currently in view                                 */
(function () {
  'use strict';
  var root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };

  /* ---- 0. Teasers ---- */
  var conn = navigator.connection || {};
  if (!conn.saveData && !/2g/.test(conn.effectiveType || '')) {
    var prefetchTeasers = function () {
      each(document.querySelectorAll('img[loading="lazy"]'), function (img) { img.loading = 'eager'; });
    };
    var whenIdle = function (fn) {
      if (window.requestIdleCallback) window.requestIdleCallback(fn, { timeout: 2000 }); else setTimeout(fn, 300);
    };
    if (document.readyState === 'complete') whenIdle(prefetchTeasers);
    else window.addEventListener('load', function () { whenIdle(prefetchTeasers); });
  }

  /* ---- 1. Theme ---- */
  function storedTheme() {
    try { var t = localStorage.getItem('theme'); return (t === 'light' || t === 'dark') ? t : null; } catch (e) { return null; }
  }
  function systemTheme() { return (mq && mq.matches) ? 'dark' : 'light'; }
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.setAttribute('aria-pressed', String(theme === 'dark'));   /* constant name "Dark theme", state = pressed */
  }
  applyTheme(storedTheme() || systemTheme());
  if (mq && mq.addEventListener) {
    mq.addEventListener('change', function () { if (!storedTheme()) applyTheme(systemTheme()); });
  }
  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try {
        /* If the choice matches the OS again, forget it so the page keeps following the OS. */
        if (next === systemTheme()) localStorage.removeItem('theme'); else localStorage.setItem('theme', next);
      } catch (e) { /* storage unavailable: theme still applies for this visit */ }
    });
  }

  /* ---- 2. Publications: Selected / All ---- */
  var pubs = document.getElementById('publications');
  if (pubs) {
    var buttons = pubs.querySelectorAll('.seg button[data-view]');
    var status = pubs.querySelector('.pubs-status');
    var allPubs = pubs.querySelectorAll('.pub');
    var selectedPubs = pubs.querySelectorAll('.pub[data-selected="true"]');
    each(buttons, function (b) {
      var c = b.querySelector('.count');
      if (c) c.textContent = (b.getAttribute('data-view') === 'all' ? allPubs : selectedPubs).length;
    });
    var setView = function (view) {
      pubs.setAttribute('data-view', view);
      each(buttons, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === view)); });
      each(allPubs, function (p) {
        p.hidden = (view === 'selected' && p.getAttribute('data-selected') !== 'true');
      });
      each(pubs.querySelectorAll('.pub-group'), function (g) {
        g.hidden = !g.querySelector('.pub:not([hidden])');
      });
      if (status) {
        status.textContent = view === 'all'
          ? 'Showing all ' + allPubs.length + ' papers.'
          : 'Showing ' + selectedPubs.length + ' selected of ' + allPubs.length + ' papers.';
      }
    };
    each(buttons, function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-view')); }); });
    /* ?view=all opens the full list; a #pub-<key> link to a non-selected paper also opens it. */
    var wantAll = /[?&]view=all(&|$)/.test(location.search);
    var target = location.hash && /^#pub-/.test(location.hash) ? document.getElementById(location.hash.slice(1)) : null;
    if (target && target.getAttribute('data-selected') !== 'true') wantAll = true;
    setView(wantAll ? 'all' : (pubs.getAttribute('data-view') || 'selected'));
    if (target) setTimeout(function () { target.scrollIntoView(); }, 0);
    window.addEventListener('hashchange', function () {
      var t = /^#pub-/.test(location.hash) ? document.getElementById(location.hash.slice(1)) : null;
      if (t && t.getAttribute('data-selected') !== 'true') { setView('all'); t.scrollIntoView(); }
    });
  }

  /* ---- 3. News: show more ---- */
  var newsList = document.querySelector('.news-list');
  var newsBtn = document.querySelector('.news-more');
  var NEWS_LIMIT = 6;
  if (newsList && newsBtn && newsList.children.length > NEWS_LIMIT) {
    var total = newsList.children.length;
    each(newsList.children, function (li, i) { if (i >= NEWS_LIMIT) li.classList.add('is-extra'); });
    var render = function (collapsed) {
      newsList.classList.toggle('is-collapsed', collapsed);
      newsBtn.setAttribute('aria-expanded', String(!collapsed));
      newsBtn.textContent = collapsed ? ('Show all ' + total + ' updates') : 'Show fewer updates';
    };
    newsBtn.hidden = false;
    render(true);
    newsBtn.addEventListener('click', function () { render(!newsList.classList.contains('is-collapsed')); });
  }

  /* ---- 4. Section nav: current section ---- */
  var links = document.querySelectorAll('.nav-links a[href^="#"]');
  if ('IntersectionObserver' in window && links.length) {
    var byId = {}, order = [], visible = {};
    each(links, function (a) { var id = a.getAttribute('href').slice(1); byId[id] = a; order.push(id); });
    var setCurrent = function () {
      var current = null;
      for (var i = 0; i < order.length; i++) { if (visible[order[i]]) { current = order[i]; break; } }
      /* At the very bottom the last section can never reach the observation band: mark it anyway. */
      if (Math.ceil(window.scrollY + window.innerHeight) >= document.documentElement.scrollHeight - 2) current = order[order.length - 1];
      each(links, function (a) {
        if (current && a === byId[current]) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
      setCurrent();
    }, { rootMargin: '-15% 0px -70% 0px' });
    order.forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
    window.addEventListener('scroll', setCurrent, { passive: true });
  }
})();
