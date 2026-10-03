/* Jabella Painting and Carpentry: page behaviour.
   1. Hero film scrubbed by scroll (sticky stage inside a 330vh track).
   2. Before/after slider.
   3. Mobile nav, reveal-on-entry, form success state. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = window.matchMedia('(max-width: 760px)').matches;

  /* ---------------- 1. hero film ---------------- */
  var track = document.querySelector('.hero-scroll');
  var video = track && track.querySelector('.hero-video');
  var poster = track && track.querySelector('.hero-poster');
  var copy = track && track.querySelector('.hero-copy');
  var bar = track && track.querySelector('.hero-progress span');

  function staticHero() {
    track.classList.add('static-hero');
    if (poster) poster.src = 'assets/hero-end.webp';
  }

  if (track && video) {
    if (reduce) {
      staticHero();
    } else {
      var src = mobile && video.dataset.srcMobile ? video.dataset.srcMobile : video.dataset.src;
      var ready = false, target = 0, raf = 0, last = -1;

      // Blob-load so seeking never depends on HTTP range support.
      fetch(src).then(function (r) { return r.blob(); }).then(function (b) {
        video.src = URL.createObjectURL(b);
        video.load();
      }).catch(function () { video.src = src; video.load(); });

      function progress() {
        var rect = track.getBoundingClientRect();
        var total = track.offsetHeight - window.innerHeight;
        var p = total > 0 ? -rect.top / total : 0;
        return Math.min(1, Math.max(0, p));
      }

      function paint() {
        raf = 0;
        var p = progress();
        if (bar) bar.style.transform = 'scaleX(' + p + ')';
        if (copy) copy.style.opacity = String(p < 0.1 ? 1 : p < 0.65 ? 0.18 : Math.min(1, 0.18 + (p - 0.65) * 4));
        if (!ready || !isFinite(video.duration) || video.readyState < 1) return;
        target = p * Math.max(0, video.duration - 0.05);
        if (!video.seeking && Math.abs(video.currentTime - target) > 0.035) {
          video.currentTime = target;
        }
      }
      function schedule() { if (!raf) raf = requestAnimationFrame(paint); }

      function onReady() {
        if (ready) return;
        ready = true;
        video.pause();
        video.classList.add('is-ready');
        schedule();
      }
      ['loadedmetadata', 'loadeddata', 'canplay'].forEach(function (e) { video.addEventListener(e, onReady); });
      video.addEventListener('seeked', schedule);
      // iOS will not decode a frame until play() has been called once.
      video.addEventListener('loadedmetadata', function () {
        var p = video.play();
        if (p && p.then) p.then(function () { video.pause(); }).catch(function () {});
      });

      window.addEventListener('scroll', schedule, { passive: true });
      window.addEventListener('resize', schedule);
      schedule();
    }
  }

  /* ---------------- 2. before / after ---------------- */
  var cmp = document.getElementById('compare');
  if (cmp) {
    var range = cmp.querySelector('.compare__range');
    function setPos(v) { cmp.style.setProperty('--pos', v + '%'); }
    range.addEventListener('input', function () { setPos(range.value); });
    // Pointer drag anywhere in the frame (the range input covers it, but
    // some browsers only move the thumb on direct hits).
    var dragging = false;
    function fromEvent(e) {
      var r = cmp.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      var v = Math.round(Math.min(100, Math.max(0, (x / r.width) * 100)));
      range.value = v; setPos(v);
    }
    cmp.addEventListener('pointerdown', function (e) { dragging = true; fromEvent(e); });
    window.addEventListener('pointermove', function (e) { if (dragging) fromEvent(e); });
    window.addEventListener('pointerup', function () { dragging = false; });
  }

  /* ---------------- 3. chrome ---------------- */
  var toggle = document.querySelector('.menu-toggle');
  var mnav = document.getElementById('mobile-nav');
  if (toggle && mnav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      mnav.hidden = open;
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { toggle.setAttribute('aria-expanded', 'false'); mnav.hidden = true; }
    });
  }

  /* Residential dropdown: click toggles, outside click and Escape close. */
  var subs = document.querySelectorAll('.has-sub');
  Array.prototype.forEach.call(subs, function (wrap) {
    var btn = wrap.querySelector('.nav-sub-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = wrap.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(subs, function (wrap) {
      if (!wrap.contains(e.target)) { wrap.classList.remove('is-open'); wrap.querySelector('.nav-sub-toggle').setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    Array.prototype.forEach.call(subs, function (wrap) { wrap.classList.remove('is-open'); wrap.querySelector('.nav-sub-toggle').setAttribute('aria-expanded', 'false'); });
  });
  // Mark the current page in both menus.
  var here = location.pathname.replace(/index\.html$/, '');
  Array.prototype.forEach.call(document.querySelectorAll('.desktop-nav a, .mobile-nav a'), function (a) {
    var href = a.getAttribute('href') || '';
    if (href.indexOf('#') === -1 && href.replace(/index\.html$/, '') === here) a.setAttribute('aria-current', 'page');
  });

  var reveals = document.querySelectorAll('[data-reveal]');
  if (reveals.length && 'IntersectionObserver' in window && !reduce) {
    reveals.forEach(function (el) {
      if (el.hasAttribute('data-stagger')) {
        Array.prototype.forEach.call(el.children, function (c, i) { c.style.setProperty('--i', i); });
      }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* FAQ accordion: animate height on open and close. */
  var accs = document.querySelectorAll('.accordion details');
  Array.prototype.forEach.call(accs, function (d) {
    var sum = d.querySelector('summary');
    var body = d.querySelector('.acc__body');
    var anim = null;
    if (!sum || !body) return;
    sum.addEventListener('click', function (e) {
      e.preventDefault();
      if (reduce || !body.animate) { d.open = !d.open; return; }
      if (anim) anim.cancel();
      if (d.open) {
        // close: shrink from current height to 0, then drop the open attribute
        var from = body.offsetHeight;
        d.classList.add('is-closing');
        anim = body.animate([{ height: from + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 260, easing: 'cubic-bezier(.4,0,.2,1)' });
        anim.onfinish = function () { d.open = false; d.classList.remove('is-closing'); body.style.height = ''; anim = null; };
        anim.oncancel = function () { d.classList.remove('is-closing'); };
      } else {
        // open: set open first (so the body has a height), then grow into it
        d.open = true;
        var to = body.scrollHeight;
        anim = body.animate([{ height: '0px', opacity: 0 }, { height: to + 'px', opacity: 1 }], { duration: 320, easing: 'cubic-bezier(.23,1,.32,1)' });
        anim.onfinish = function () { body.style.height = ''; anim = null; };
      }
    });
  });

  var form = document.getElementById('estimate-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (f) {
        var bad = !f.value || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.classList.toggle('is-invalid', bad);
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      if (form.website.value) return; // honeypot
      // TODO: wire to the real endpoint (Formspree, GoHighLevel, etc).
      form.querySelector('.form__done').hidden = false;
      form.querySelector('button[type=submit]').disabled = true;
    });
  }
})();
