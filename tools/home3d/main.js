/* buddhabytes.app home: Stryka in 3D. A real-time phone (three.js r186 from the Design-Library) plays real recordings of
   the app on its screen and flies chapter by chapter as you scroll. Built by tools/build_home3d.py (esbuild, minified)
   into assets/js/home3d.js.
   Speed: one fixed canvas, pixel ratio capped, rendering stops while the tab is hidden; only the current chapter's video
   plays; layout is measured once per resize (never per frame). prefers-reduced-motion: no spin, no idle drift.
   No WebGL: html.no-gl shows the still screenshots that sit in every chapter. */
import * as THREE from 'three';
import { RoundedBoxGeometry } from './vendor/three/RoundedBoxGeometry.js';
import { RoomEnvironment } from './vendor/three/RoomEnvironment.js';

const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const root = document.documentElement;
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];

/* ---------- loader ---------- */
const LD = $('.ld'), ldNum = $('.ld-num');
let ldShown = 0, ldTarget = 0;
const ldStart = performance.now();
const ldTick = () => { ldShown += (ldTarget - ldShown) * .12; if (ldNum) ldNum.textContent = String(Math.round(ldShown)).padStart(3, '0');
  if (ldShown < 99.5) requestAnimationFrame(ldTick) };
requestAnimationFrame(ldTick);
let doneCalled = false;
const ldDone = () => { if (doneCalled) return; doneCalled = true; ldTarget = 100;
  const wait = Math.max(0, (RM ? 300 : 1500) - (performance.now() - ldStart));
  setTimeout(() => { root.classList.add('loaded'); setTimeout(() => LD && LD.remove(), 1400) }, wait) };
setTimeout(ldDone, 7000); // never block the page on a slow network

/* ---------- text reveals ---------- */
$$('.split').forEach(el => {
  const words = el.textContent.trim().split(/\s+/); let i = 0; el.setAttribute('aria-label', el.textContent.trim());
  el.innerHTML = words.map(w => `<span class="w" aria-hidden="true">${[...w].map(c => `<span class="c" style="--i:${i++}">${c}</span>`).join('')}</span>`).join(' ');
});
const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target) } }), { threshold: .25 });
$$('.rv').forEach(el => io.observe(el));

/* ---------- 3D ---------- */
const canvas = $('#gl');
let renderer;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }) }
catch (e) { renderer = null }
if (!renderer) { root.classList.add('no-gl'); ldDone() }
else start();

function start() {
  root.classList.add('gl');
  const small = () => innerWidth < 760;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, small() ? 1.5 : 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, .1, 60); camera.position.set(0, 0, 7.2);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
  ldTarget = 35;

  scene.add(new THREE.AmbientLight(0xffffff, .25));
  const rim = new THREE.DirectionalLight(0x00cba9, 3.2); rim.position.set(-4, 2.5, -3); scene.add(rim);
  const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(3, 4, 5); scene.add(key);
  const warm = new THREE.PointLight(0xf5b451, 6, 12); warm.position.set(3, -2, 2); scene.add(warm);

  /* phone: rounded body, glass screen (rounded rect with 0..1 UVs), camera bump, side keys, STRYKA on the back */
  const SW = .92, SH = SW / .4493, BW = SW + .1, BH = SH + .1, BD = .12;
  const phone = new THREE.Group(), tilt = new THREE.Group(); tilt.add(phone); scene.add(tilt);
  const metal = new THREE.MeshPhysicalMaterial({ color: 0x0b1010, metalness: .9, roughness: .26, clearcoat: 1, clearcoatRoughness: .18 });
  phone.add(new THREE.Mesh(new RoundedBoxGeometry(BW, BH, BD, 8, .14), metal));
  const rr = (w, h, r) => { const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
    s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r);
    s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s };
  const uvRect = (g, w, h) => { const p = g.attributes.position, uv = new Float32Array(p.count * 2);
    for (let i = 0; i < p.count; i++) { uv[i * 2] = p.getX(i) / w + .5; uv[i * 2 + 1] = p.getY(i) / h + .5 } g.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); return g };
  const glassBlack = new THREE.MeshBasicMaterial({ color: 0x020404 });
  const bez = new THREE.Mesh(new THREE.ShapeGeometry(rr(SW + .04, SH + .04, .12), 24), glassBlack); bez.position.z = BD / 2 + .001; phone.add(bez);
  const screenMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const screen = new THREE.Mesh(uvRect(new THREE.ShapeGeometry(rr(SW, SH, .1), 24), SW, SH), screenMat); screen.position.z = BD / 2 + .002; phone.add(screen);
  const gloss = new THREE.Mesh(new THREE.ShapeGeometry(rr(SW, SH, .1), 24), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: .06, roughness: .05, metalness: 0, clearcoat: 1 }));
  gloss.position.z = BD / 2 + .004; phone.add(gloss);
  const bump = new THREE.Mesh(new RoundedBoxGeometry(.36, .36, .04, 4, .08), metal); bump.position.set(-BW / 2 + .3, BH / 2 - .3, -BD / 2 - .015); phone.add(bump);
  const lensMat = new THREE.MeshPhysicalMaterial({ color: 0x050707, metalness: .2, roughness: .05, clearcoat: 1 });
  [[-.07, .07], [.07, -.07]].forEach(([dx, dy]) => { const l = new THREE.Mesh(new THREE.CylinderGeometry(.055, .055, .03, 32), lensMat); l.rotation.x = Math.PI / 2; l.position.set(bump.position.x + dx, bump.position.y + dy, -BD / 2 - .04); phone.add(l) });
  [[.42, .22], [.12, .14]].forEach(([y, h]) => { const k = new THREE.Mesh(new RoundedBoxGeometry(.03, h, .05, 2, .012), metal); k.position.set(BW / 2 + .006, y, 0); phone.add(k) });
  const backTex = (() => { const c = document.createElement('canvas'); c.width = 512; c.height = 1024; const x = c.getContext('2d');
    x.fillStyle = '#00CBA9'; x.font = '700 64px "Space Grotesk", sans-serif'; x.textAlign = 'center'; x.globalAlpha = .9; x.fillText('STRYKA', 256, 560);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t })();
  const back = new THREE.Mesh(new THREE.PlaneGeometry(BW * .9, BH * .9), new THREE.MeshBasicMaterial({ map: backTex, transparent: true, toneMapped: false }));
  back.rotation.y = Math.PI; back.position.z = -BD / 2 - .002; phone.add(back);

  /* constellation dust (house style: drifting teal points, soft, no glitter) */
  const N = small() ? 260 : 520, pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) { const r = 3 + Math.random() * 7, t = Math.random() * 6.283, u = Math.random() * 2 - 1, s = Math.sqrt(1 - u * u);
    pos[i * 3] = r * s * Math.cos(t); pos[i * 3 + 1] = r * u * .7; pos[i * 3 + 2] = r * s * Math.sin(t) - 3 }
  const dustG = new THREE.BufferGeometry(); dustG.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const dust = new THREE.Points(dustG, new THREE.PointsMaterial({ color: 0x5eead4, size: .028, transparent: true, opacity: .55, depthWrite: false }));
  scene.add(dust);
  const halo = new THREE.Mesh(new THREE.CircleGeometry(2.2, 48), new THREE.MeshBasicMaterial({ color: 0x00cba9, transparent: true, opacity: .07, depthWrite: false }));
  halo.position.z = -1.2; tilt.add(halo);

  /* screens: one per section; a still first, then its recording once it can play */
  const loaderTex = new THREE.TextureLoader();
  const secs = $$('[data-scr]');
  const S = secs.map(el => ({ el, img: el.dataset.scr, vid: el.dataset.vid, side: el.dataset.side || 'r', spin: +el.dataset.spin || 0,
    away: el.dataset.away === '1', tex: null, vtex: null, video: null }));
  const imgTex = s => s.tex || (s.tex = loaderTex.load(s.img, t => { t.colorSpace = THREE.SRGBColorSpace; if (cur >= 0 && S[cur] === s && !S[cur].vready) setMap(s.tex) }));
  const vidOf = s => { if (!s.vid || RM) return null; if (s.video) return s.video;
    const v = s.video = document.createElement('video'); Object.assign(v, { muted: true, loop: true, playsInline: true, preload: 'auto' });
    v.setAttribute('muted', ''); v.setAttribute('playsinline', ''); v.src = s.vid;
    v.addEventListener('canplay', () => { if (!s.vtex) { s.vtex = new THREE.VideoTexture(v); s.vtex.colorSpace = THREE.SRGBColorSpace }
      s.vready = true; if (S[cur] === s && !swapping) setMap(s.vtex) }, { once: false });
    return v };
  const setMap = t => { screenMat.map = t; screenMat.needsUpdate = true };
  imgTex(S[0]).image; // hero still first
  ldTarget = 60;

  /* layout per section (desktop / phone) */
  const target = { x: 1.25, y: 0, ry: -.45, rx: .06, rz: .06, s: 1 }, now = { ...target, y: -4 };
  let cur = -1, sp = 0, swapping = false, spinFrom = 0, spinTo = 0, spinT = 1, spinSwap = null, extraSpin = 0;
  const kf = (s, p) => {
    const mob = innerWidth < 760, side = s.side === 'l' ? -1 : 1;
    if (s.away) return { x: 0, y: 4.2, ry: 0, rx: .3, rz: 0, s: .8 };
    if (mob) return { x: 0, y: 1.24, ry: side * -.28 + (p - .5) * .5, rx: .08, rz: 0, s: .55 };
    return { x: side * 1.32, y: (p - .5) * -.25, ry: side * -.42 + (p - .5) * .45, rx: .06 - (p - .5) * .1, rz: side * .04, s: 1 };
  };
  let tops = [];
  const measure = () => { tops = secs.map(el => el.getBoundingClientRect().top + scrollY); const h = innerHeight;
    renderer.setSize(innerWidth, h, false); camera.aspect = innerWidth / h; camera.updateProjectionMatrix() };
  measure(); addEventListener('resize', () => { measure(); onScroll() }); if (document.fonts) document.fonts.ready.then(() => { measure(); backTex.needsUpdate = true; redrawBack() });
  function redrawBack() { const c = backTex.image, x = c.getContext('2d'); x.clearRect(0, 0, 512, 1024); x.fillStyle = '#00CBA9'; x.globalAlpha = .9;
    x.font = '700 64px "Space Grotesk", sans-serif'; x.textAlign = 'center'; x.fillText('STRYKA', 256, 560); backTex.needsUpdate = true }

  const choose = i => {
    if (i === cur) return; const prev = cur; cur = i; const s = S[i];
    imgTex(s); if (S[i + 1]) imgTex(S[i + 1]);
    S.forEach((o, k) => { if (o.video && k !== i) o.video.pause() });
    const v = vidOf(s); if (v) { const pr = v.play(); if (pr) pr.catch(() => {}) }
    const show = () => setMap(s.vready ? s.vtex : s.tex);
    if (prev < 0 || RM || s.away || S[prev].away || S[prev].img === s.img) { show(); return }
    /* turn the phone round: the screen changes while it faces away */
    swapping = true; spinFrom = extraSpin; spinTo = extraSpin + Math.PI * 2 * (i > prev ? 1 : -1); spinT = 0; spinSwap = show;
  };
  const onScroll = () => {
    const y = scrollY + innerHeight * .5; let i = 0;
    for (let k = 0; k < tops.length; k++) if (tops[k] <= y) i = k;
    const next = tops[i + 1] != null ? tops[i + 1] : tops[i] + innerHeight;
    sp = Math.min(1, Math.max(0, (y - tops[i]) / Math.max(1, next - tops[i])));
    choose(i); Object.assign(target, kf(S[i], sp));
  };
  let queued = false; addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; onScroll() }) } }, { passive: true });
  onScroll(); setMap(S[0].tex);

  /* pointer parallax (mouse only) */
  let mx = 0, my = 0; addEventListener('pointermove', e => { if (e.pointerType === 'mouse') { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5 } }, { passive: true });

  let last = performance.now(), raf = 0, first = true;
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const frame = t => {
    raf = 0; const dt = Math.min(.05, (t - last) / 1000); last = t; const k = 1 - Math.exp(-dt * (RM ? 30 : 3.6));
    for (const n of ['x', 'y', 'ry', 'rx', 'rz', 's']) now[n] += (target[n] - now[n]) * k;
    if (spinT < 1) { spinT = Math.min(1, spinT + dt / .95); const e = ease(spinT); extraSpin = spinFrom + (spinTo - spinFrom) * e;
      if (spinSwap && spinT > .28) { spinSwap(); spinSwap = null } if (spinT >= 1) { swapping = false; extraSpin = 0; spinFrom = spinTo = 0;
        const s = S[cur]; if (s && s.vready) setMap(s.vtex) } }
    const idle = RM ? 0 : Math.sin(t / 1800) * .05;
    tilt.position.set(now.x, now.y + (RM ? 0 : Math.sin(t / 1500) * .04), 0);
    tilt.rotation.set(now.rx + my * .12, now.ry + mx * .22 + idle, now.rz);
    tilt.scale.setScalar(now.s); phone.rotation.y = extraSpin;
    if (!RM) { dust.rotation.y += dt * .015; dust.rotation.x = Math.sin(t / 9000) * .05 }
    renderer.render(scene, camera);
    if (first) { first = false; ldTarget = 100; ldDone() }
    if (!document.hidden) raf = requestAnimationFrame(frame);
  };
  document.addEventListener('visibilitychange', () => { if (document.hidden) S.forEach(o => o.video && o.video.pause());
    else { last = performance.now(); if (!raf) raf = requestAnimationFrame(frame); const s = S[cur]; if (s && s.video) s.video.play().catch(() => {}) } });
  raf = requestAnimationFrame(frame);
}
