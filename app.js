/* PINNeAPPle Labs — landing page behaviour */
(function () {
  'use strict';

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- copy install command ---------- */
  document.querySelectorAll('.install').forEach(function (el) {
    var cmd = el.getAttribute('data-copy') || el.textContent.trim();
    el.addEventListener('click', function () {
      copy(cmd).then(function () {
        el.classList.add('copied');
        var label = el.querySelector('.copy-ico');
        if (label) {
          var prev = label.innerHTML;
          label.innerHTML = '✓';
          setTimeout(function () { label.innerHTML = prev; }, 1400);
        }
        setTimeout(function () { el.classList.remove('copied'); }, 1400);
      });
    });
  });

  /* ---------- copy buttons ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (el) {
    if (el.classList.contains('install')) return;
    el.addEventListener('click', function () {
      copy(el.getAttribute('data-copy')).then(function () {
        var prev = el.textContent;
        el.textContent = el.getAttribute('data-copied-label') || 'copiado';
        setTimeout(function () { el.textContent = prev; }, 1400);
      });
    });
  });

  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { legacy(text); });
    }
    legacy(text);
    return Promise.resolve();
  }
  function legacy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
  }

  /* ---------- code tabs ---------- */
  document.querySelectorAll('[data-tabs]').forEach(function (group) {
    var buttons = group.querySelectorAll('.tabs button');
    var panes = group.querySelectorAll('pre.code');
    buttons.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) {
          b.setAttribute('aria-selected', 'false');
          b.setAttribute('tabindex', '-1');
        });
        btn.setAttribute('aria-selected', 'true');
        btn.setAttribute('tabindex', '0');
        panes.forEach(function (p, j) { p.hidden = i !== j; });
        var name = group.querySelector('.fname');
        if (name && btn.getAttribute('data-file')) name.textContent = btn.getAttribute('data-file');
      });
    });
  });

  /* ---------- reveal on scroll ---------- */
  var revealables = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- video: only play when visible, pause offscreen ---------- */
  var heroVideo = document.querySelector('.hero-media video');
  if (heroVideo && 'IntersectionObserver' in window) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      heroVideo.removeAttribute('autoplay');
      heroVideo.pause();
    } else {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { heroVideo.play().catch(function () {}); }
          else { heroVideo.pause(); }
        });
      }, { threshold: 0.15 }).observe(heroVideo);
    }
  }

  /* ---------- nav current section ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
  var links = Array.prototype.slice.call(document.querySelectorAll('nav.main a[href^="#"]'));
  if (sections.length && links.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute('href') === '#' + entry.target.id;
          if (on) { a.setAttribute('aria-current', 'true'); }
          else { a.removeAttribute('aria-current'); }
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }
})();
