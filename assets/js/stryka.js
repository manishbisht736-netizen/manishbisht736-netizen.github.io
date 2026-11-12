/* Stryka immersive page motion. Transform/opacity only; every loop runs on requestAnimationFrame and stops when
   off-screen or when the tab is hidden; prefers-reduced-motion gets a static page. */
(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const onScreen = (el, cb) => new IntersectionObserver(es => es.forEach(x => cb(x.isIntersecting)), { threshold: 0.05 }).observe(el);

  /* 1. Constellation stars behind the hero (house chart style: drifting points, soft links, no glitter) */
  const cv = document.querySelector('.sx-stars');
  if (cv) {
    const ctx = cv.getContext('2d');
    let W = 0, H = 0, pts = [], vis = false, raf = 0;
    const size = () => {
      const r = Math.min(devicePixelRatio || 1, 1.5);
      W = cv.clientWidth; H = cv.clientHeight; cv.width = W * r; cv.height = H * r; ctx.setTransform(r, 0, 0, r, 0, 0);
      const n = Math.round(Math.min(70, W * H / 16000));
      pts = Array.from({ length: n }, () => ({ x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .18, vy: (Math.random() - .5) * .18, r: Math.random() * 1.4 + .6 }));
    };
    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
      }
      ctx.lineWidth = 1;
      for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
        const a = pts[i], b = pts[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 120) { ctx.strokeStyle = `rgba(45,212,191,${(1 - d / 120) * .22})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      }
      for (const p of pts) { ctx.fillStyle = 'rgba(190,240,232,.75)'; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill(); }
    };
    const loop = () => { draw(); raf = vis && !document.hidden ? requestAnimationFrame(loop) : 0; };
    size(); draw();
    addEventListener('resize', () => { size(); draw(); });
    if (!RM) {
      onScreen(cv, v => { vis = v; if (v && !raf) loop(); });
      document.addEventListener('visibilitychange', () => { if (!document.hidden && vis && !raf) loop(); });
    }
  }

  /* 2. Hero phone fan: tilts toward the pointer and lifts slightly on scroll */
  const stage = document.querySelector('.sx-stage'), fan = document.querySelector('.sx-fan');
  if (stage && fan && !RM) {
    let tx = 0, ty = 0, queued = false, rect = null;
    const apply = () => {
      queued = false;
      fan.style.setProperty('--ry', (-10 + tx * 14).toFixed(2) + 'deg');
      fan.style.setProperty('--rx', (6 - ty * 10).toFixed(2) + 'deg');
      fan.style.setProperty('--py', (-Math.min(scrollY, 600) * .08).toFixed(1) + 'px');
    };
    const q = () => { if (!queued) { queued = true; requestAnimationFrame(apply); } };
    stage.parentElement.addEventListener('pointerenter', () => { rect = stage.getBoundingClientRect(); });
    stage.parentElement.addEventListener('pointermove', ev => {
      if (ev.pointerType !== 'mouse') return;
      if (!rect) rect = stage.getBoundingClientRect();
      tx = (ev.clientX - rect.left) / rect.width - .5; ty = (ev.clientY - rect.top) / rect.height - .5; q();
    });
    stage.parentElement.addEventListener('pointerleave', () => { tx = 0; ty = 0; rect = null; q(); });
    addEventListener('scroll', q, { passive: true });
  }

  /* 3. Scroll story: the step in the middle of the screen drives the sticky 3D phone */
  const device = document.querySelector('.sx-device');
  const steps = [...document.querySelectorAll('.sx-step')];
  if (device && steps.length) {
    const front = [...device.querySelectorAll('.sx-front .sx-screen')];
    const back = [...device.querySelectorAll('.sx-back .sx-screen')];
    const dots = [...document.querySelectorAll('.sx-dots i')];
    let cur = -1;
    const show = k => {
      if (k === cur) return; cur = k;
      steps.forEach(s => s.classList.toggle('is-active', +s.dataset.i === k));
      front.forEach(s => s.classList.toggle('is-on', +s.dataset.i === k));
      let hasBack = false;
      back.forEach(s => { const on = +s.dataset.i === k; s.classList.toggle('is-on', on); hasBack = hasBack || on; });
      dots.forEach(d => d.classList.toggle('is-on', +d.dataset.i === k));
      device.classList.toggle('has-back', hasBack);
      if (!RM) {
        device.style.setProperty('--dy', (k % 2 ? 14 : -14) + 'deg');
        device.style.setProperty('--dx', (k % 3 === 1 ? -3 : 4) + 'deg');
        device.classList.remove('flash'); requestAnimationFrame(() => device.classList.add('flash'));
      }
    };
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) show(+x.target.dataset.i); }),
      { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(s => io.observe(s));
    show(0);
  }

  /* 4. Run replay demo: the route draws itself, km markers pop in, distance and time tick along */
  const map = document.querySelector('.sx-map');
  if (map) {
    const route = map.querySelector('.sx-route'), glow = map.querySelector('.sx-route-glow');
    const dot = map.querySelector('.sx-dot'), halo = map.querySelector('.sx-dot-halo'), kms = map.querySelector('.sx-kms');
    const kmEl = map.querySelector('.sx-km'), tEl = map.querySelector('.sx-time');
    const len = route.getTotalLength(), KM = 4.64, PACE = 337; // sample run: 4.64 km at 5:37 /km
    map.style.setProperty('--len', len);
    const marks = [1, 2, 3, 4].map(n => {
      const p = route.getPointAtLength(len * n / KM);
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.innerHTML = `<circle cx="${p.x}" cy="${p.y}" r="10"/><text x="${p.x}" y="${p.y}">${n}</text>`;
      kms.appendChild(g); return g;
    });
    const set = f => {
      const off = len * (1 - f), p = route.getPointAtLength(len * f);
      route.style.strokeDashoffset = off; glow.style.strokeDashoffset = off;
      dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y); halo.setAttribute('cx', p.x); halo.setAttribute('cy', p.y);
      const km = KM * f, s = Math.round(km * PACE);
      kmEl.textContent = km.toFixed(2); tEl.textContent = Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
      marks.forEach((m, i) => m.classList.toggle('on', f >= (i + 1) / KM));
    };
    if (RM) set(1);
    else {
      let vis = false, raf = 0, t0 = 0;
      const DUR = 9000, HOLD = 2200;
      const loop = now => {
        if (!t0) t0 = now;
        const e = (now - t0) % (DUR + HOLD), f = Math.min(1, e / DUR);
        set(f * (2 - f) * .35 + f * .65); // gentle ease-out
        raf = vis && !document.hidden ? requestAnimationFrame(loop) : 0;
      };
      set(0);
      onScreen(map, v => { vis = v; if (v && !raf) raf = requestAnimationFrame(loop); });
      document.addEventListener('visibilitychange', () => { if (!document.hidden && vis && !raf) raf = requestAnimationFrame(loop); });
    }
  }

  /* 5. Feature cards tilt in 3D under the mouse */
  if (!RM) document.querySelectorAll('.sx-tilt').forEach(c => {
    let r = null, queued = false, x = .5, y = .5;
    const apply = () => {
      queued = false;
      c.style.setProperty('--ty', ((x - .5) * 12).toFixed(2) + 'deg'); c.style.setProperty('--tx', ((.5 - y) * 12).toFixed(2) + 'deg');
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    };
    c.addEventListener('pointerenter', () => { r = c.getBoundingClientRect(); });
    c.addEventListener('pointermove', ev => {
      if (ev.pointerType !== 'mouse' || !r) return;
      x = (ev.clientX - r.left) / r.width; y = (ev.clientY - r.top) / r.height;
      if (!queued) { queued = true; requestAnimationFrame(apply); }
    });
    c.addEventListener('pointerleave', () => { x = .5; y = .5; r = null; requestAnimationFrame(apply); });
  });
})();
