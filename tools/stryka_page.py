"""Immersive Stryka landing page (rise/index.html): 3D hero, scroll story, run-replay demo.

Called from build_site.py for apps with immersive=True. Styles: assets/css/stryka.css, motion: assets/js/stryka.js
(transform/opacity only, paused off-screen and when the tab is hidden, static with prefers-reduced-motion).
"""


def render(a, site):
    e, ic, head, nav, footer = site.e, site.ic, site.head, site.nav, site.footer
    img = f"../assets/img/apps/{a['slug']}"

    # real app motion (store/web-motion/record.js in the Stryka repo): screen → silent looping clip
    VID = {"shot-1": "pulse", "tour-ins-vitals": "insights", "shot-3": "run", "tour-run-finish": "replay", "shot-4": "coach"}
    vdir = "../assets/video/stryka"

    def media(name, alt="", cls="sx-screen", attrs=""):
        if name in VID:
            return (f'<video class="{cls} sx-vid" data-src="{vdir}/{VID[name]}.webm" poster="{img}/{name}.webp" muted loop playsinline '
                    f'preload="none" aria-label="{e(alt)}"{attrs}></video>')
        return f'<img class="{cls}" src="{img}/{name}.webp" alt="{e(alt)}" loading="lazy" decoding="async"{attrs}>'

    def shot(name, alt, cls="sx-phone", lazy=True):
        if name in VID:
            return f'<div class="{cls}">{media(name, alt, "")}</div>'
        lz = ' loading="lazy"' if lazy else ""
        return f'<div class="{cls}"><img src="{img}/{name}.webp" alt="{e(alt)}"{lz} decoding="async"></div>'

    play = (f'<a class="btn btn-primary sx-glow" href="{a["play"]}" target="_blank" rel="noopener">'
            f'{ic("google-play-logo")} Get it on Google Play</a>')

    # --- scroll story: one step per tour row; the sticky 3D phone swaps to the step's screens
    steps, screens, backs, dots = "", "", "", ""
    for k, (i, t, h, d, bullets, imgs) in enumerate(a["tour"]):
        lis = "".join(f"<li>{ic('seal-check')}<span>{e(b)}</span></li>" for b in bullets)
        inline = "".join(shot(s, f"{a['name']}: {t}") for s in imgs)
        steps += (f'<article class="sx-step" data-i="{k}"><div class="sx-step-media">{inline}</div>'
                  f'<div class="tour-kicker">{ic(i)} {e(t)}</div><h3>{e(h)}</h3><p>{e(d)}</p>'
                  f'<ul class="checks">{lis}</ul></article>')
        screens += media(imgs[0], attrs=f' data-i="{k}"')
        if len(imgs) > 1:
            backs += media(imgs[1], attrs=f' data-i="{k}"')
        dots += f'<i data-i="{k}"></i>'

    feats = "".join(f'<div class="feature sx-tilt reveal"><div class="fi">{ic(i)}</div><h4>{e(t)}</h4><p>{e(d)}</p></div>'
                    for i, t, d in a["features"])
    st, sp, checks, photo = a["split"]
    checks_html = "".join(f"<li>{ic('seal-check')}<span>{e(c)}</span></li>" for c in checks)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in a["faq"])
    legal = "".join(f'<a href="{h}">{ic("lock-simple")} {e(t)}</a>' for t, h in a["legal"])
    others = "".join(
        f'<a href="../{o["slug"]}/"><img src="../assets/img/apps/{o["slug"]}/icon.png" alt="" loading="lazy"><span>{e(o["name"])}<small>{e(o["kind"])}</small></span></a>'
        for o in site.APPS if o is not a)

    style = (site.accent_style(a) +
             '<style>:root{color-scheme:dark;--bg:#090F0E;--bg-2:#0E1716;--card:#121C1B;--ink:#ECF3F1;'
             '--muted:#A3B4B0;--line:#22302E;--accent-text:#2DD4BF}</style>\n'
             '<link rel="stylesheet" href="../assets/css/stryka.css">\n')
    out = head(f"{a['title']} | Buddha Bytes", a["short"], f"https://buddhabytes.app/{a['slug']}/",
               f"assets/img/photos/{a['slug']}.webp", "../", style)
    out += nav("../", [("Tour", "#tour"), ("Replay", "#replay"), ("Features", "#features"), ("FAQ", "#faq"),
                       ("All apps", "../#apps")])
    out += f"""
<header class="sx-hero">
  <canvas class="sx-stars" aria-hidden="true"></canvas>
  <div class="sx-nebula" aria-hidden="true"></div>
  <div class="wrap sx-hero-grid">
    <div class="sx-hero-copy">
      <img class="hero-icon" src="{img}/icon.png" alt="{e(a['name'])} app icon">
      <div class="eyebrow">{e(a['kind'])}</div>
      <h1>Train smarter.<br><span class="sx-grad">Recover better.</span><br>See every trend.</h1>
      <p class="lead">{e(a['lead'])}</p>
      <div class="hero-actions">{play}<a class="btn btn-ghost" href="#tour">Take the tour</a></div>
      <div class="sx-chips"><span>{ic('gauge')} Readiness</span><span>{ic('bed')} Sleep debt</span>
        <span>{ic('map-trifold')} 3D map runs</span><span>{ic('cube')} 3D coach</span></div>
    </div>
    <div class="sx-stage" aria-hidden="true">
      <div class="sx-fan">
        {shot('shot-2', '', 'sx-phone l', False)}
        <div class="sx-phone c"><video class="sx-vid" data-src="{vdir}/pulse.webm" poster="{img}/shot-1.webp" muted loop playsinline preload="none" data-eager="1"></video></div>
        {shot('shot-3', '', 'sx-phone r', False)}
        <div class="sx-float f1"><b>73</b><span>Readiness · Good<small>est.</small></span></div>
        <div class="sx-float f2"><b>5h 12m</b><span>Sleep debt<small>last 14 nights</small></span></div>
        <div class="sx-float f3"><b>5:37</b><span>avg pace /km<small>live run</small></span></div>
      </div>
    </div>
  </div>
  <p class="sx-note wrap">The phones play real recordings of the app with sample data. Health numbers are estimates, not medical advice.</p>
  <a class="sx-cue" href="#tour" aria-label="Scroll to the tour"><span></span></a>
</header>

<section id="tour" class="sx-story">
  <div class="wrap">
    <div class="section-head center reveal"><h2>Take the tour</h2><p>Scroll through the app. Every screen is real.</p></div>
    <div class="sx-story-grid">
      <div class="sx-steps">{steps}</div>
      <div class="sx-sticky" aria-hidden="true">
        <div class="sx-device">
          <div class="sx-back">{backs}</div>
          <div class="sx-front">{screens}</div>
          <div class="sx-shine"></div>
        </div>
        <div class="sx-dots">{dots}</div>
      </div>
    </div>
  </div>
</section>

<section id="replay" class="sx-replay">
  <div class="wrap sx-replay-grid">
    <div class="sx-map reveal" aria-label="Animated example of a run replay">
      <svg viewBox="0 0 400 400" role="img" aria-hidden="true">
        <defs>
          <linearGradient id="sxRoute" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2DD4BF"/><stop offset=".55" stop-color="#F5B451"/><stop offset="1" stop-color="#F472B6"/></linearGradient>
          <pattern id="sxGrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="rgba(160,200,195,.10)"/></pattern>
          <filter id="sxBlur"><feGaussianBlur stdDeviation="6"/></filter>
        </defs>
        <rect width="400" height="400" fill="url(#sxGrid)"/>
        <path d="M30 130 L370 110 M60 300 L360 280 M140 20 L170 390 M280 20 L250 390" stroke="rgba(160,200,195,.16)" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path class="sx-route-bg" d="M88 318 C70 250 96 196 150 182 S230 120 236 82 S320 52 330 120 S300 214 256 236 S210 300 248 330 S160 360 88 318Z" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="5"/>
        <path class="sx-route-glow" d="M88 318 C70 250 96 196 150 182 S230 120 236 82 S320 52 330 120 S300 214 256 236 S210 300 248 330 S160 360 88 318Z" fill="none" stroke="url(#sxRoute)" stroke-width="9" filter="url(#sxBlur)" opacity=".55"/>
        <path class="sx-route" d="M88 318 C70 250 96 196 150 182 S230 120 236 82 S320 52 330 120 S300 214 256 236 S210 300 248 330 S160 360 88 318Z" fill="none" stroke="url(#sxRoute)" stroke-width="4.5" stroke-linecap="round"/>
        <g class="sx-kms"></g>
        <circle class="sx-dot-halo" r="14" fill="#2DD4BF" opacity=".25"/>
        <circle class="sx-dot" r="6.5" fill="#fff" stroke="#2DD4BF" stroke-width="3"/>
      </svg>
      <div class="sx-hud"><div><b class="sx-km">0.00</b><span>km</span></div><div><b class="sx-time">0:00</b><span>time</span></div><div><b>5:37</b><span>avg /km</span></div></div>
    </div>
    <div class="reveal">
      <div class="tour-kicker">{ic('play-circle')} Run replay</div>
      <h2 class="sx-h2">Your run, replayed on the map</h2>
      <p class="sx-p">Finish a run and tap Replay: your route draws itself in Stryka colours, km markers pop in and your pace ticks along. Save it as a short 9:16 video and share it to any app on your phone.</p>
      <ul class="checks"><li>{ic('seal-check')}<span>The start and end of your route are hidden by default</span></li>
        <li>{ic('seal-check')}<span>Picture or video, story, post or square</span></li>
        <li>{ic('seal-check')}<span>All running features are free</span></li></ul>
      <div class="sx-replay-phones">{shot('tour-run-finish', 'Stryka: run replay')}{shot('tour-share-rphoto', 'Stryka: share editor')}</div>
    </div>
  </div>
</section>

<section id="features">
  <div class="wrap">
    <div class="section-head reveal"><h2>Everything in one app</h2><p>{e(a['short'])}</p></div>
    <div class="feature-grid sx-features">{feats}</div>
    <div class="sx-band reveal"><div><b>400+</b><span>exercises in 3D video</span></div><div><b>1,000+</b><span>foods from around the world</span></div>
      <div><b>3</b><span>languages: English, Arabic, Hindi</span></div><div><b>0</b><span>ads</span></div></div>
  </div>
</section>

<section class="alt">
  <div class="wrap split">
    <div class="reveal">
      <h2>{e(st)}</h2>
      <p>{e(sp)}</p>
      <ul class="checks">{checks_html}</ul>
      <div class="legal-links">{legal}</div>
    </div>
    <div class="photo-card reveal"><img src="../assets/img/photos/{photo}.webp" alt="" loading="lazy"></div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="section-head center reveal"><h2>Questions</h2><p>Anything else? Write to <a href="mailto:support@buddhabytes.app">support@buddhabytes.app</a>.</p></div>
    <div class="faq">{faq}</div>
    <div class="sx-cta reveal"><h3>Ready when you are</h3>{play}</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><h2>More from Buddha Bytes</h2></div>
    <div class="mini-apps">{others}</div>
  </div>
</section>

<script src="../assets/js/stryka.js" defer></script>
"""
    out += footer("../")
    return out
