"""Build the home page and one landing page per app from the APPS list below.

Run after changing app text or screenshots:  python tools/build_site.py
(Images come from tools/prepare_assets.py.) Keep each app's text in line with its store listing:
no medical claims, no fake numbers, and say "coming soon" until the Play listing is live.
"""
import html, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(SITE, "assets", "icons")
YEAR_JS = "<script>document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear())</script>"
REVEAL_JS = ("<script>(()=>{const o=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');"
             "o.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(e=>o.observe(e))})()</script>")
PLAY_SOON = "Coming soon to Google Play"


def ic(name):
    svg = open(os.path.join(ICONS, f"{name}.svg"), encoding="utf-8").read()
    return svg.replace("<svg ", '<svg class="ic" aria-hidden="true" ', 1)


e = html.escape

APPS = [
    dict(
        slug="rise", name="Rise", title="Rise: Fitness, Diet & Focus", kind="Fitness · Food · Focus",
        accent="#2DD4BF", accent_text="#0F766E", ink="#06201C", hero="#0B1413",
        short="Train with 3D exercise videos, track runs and regional food, and find calm with Monk mode.",
        lead="Workouts with real 3D exercise videos, runs, food tracking with 1,045 regional foods, a health score and calm focus, all in one app built for the Gulf and South Asia.",
        features=[
            ("barbell", "3D exercise videos", "382 recorded 3D clips across 269 movements, with plans for the gym, home or no equipment at all."),
            ("person-simple-run", "Runs", "Live pace, distance, splits and laps, plus a calendar of upcoming races near you."),
            ("bowl-food", "1,045 regional foods", "Gulf and South Asian dishes, barcode scanning and water tracking, with calories and protein at a glance."),
            ("heartbeat", "Health score", "One easy number for how your week is going. Estimates, never a diagnosis."),
            ("brain", "Monk mode", "A distraction-free focus timer. Leave the app and your plant waits for you."),
            ("headphones", "Vibes", "Soundscapes for focus, calm, sleep, the drive home or your workout."),
            ("users-three", "Sweat Stories & Groups", "Share workouts, cheer friends on and train together in a supportive feed."),
            ("calendar-check", "A plan that fits", "A weekly calendar that adapts to your goal, level and the days you can train."),
        ],
        shots=["Today's workout", "Workout player", "Food photo log", "Monk mode", "Sweat Stories", "Run tracking"],
        split=("Honest numbers, healthy habits", "Rise is built to help you show up, not to keep you scrolling.",
               ["Everything is free during launch", "No fake streak pressure or countdown offers",
                "Health numbers are labelled as estimates", "Delete your account and data any time from the app"],
               "rise-2"),
        faq=[
            ("Is Rise free?", "Yes. Everything in Rise is free during launch. If paid plans arrive later, prices will be real and shown clearly in the app before you pay."),
            ("Does Rise work with my watch?", "Watch and Health Connect support is coming soon. Until then you can log steps, sleep and workouts yourself."),
            ("Do I need gym equipment?", "No. Pick home or no-equipment plans and Rise only shows exercises you can do with what you have."),
            ("Is Rise medical advice?", "No. Rise is a wellness app. Calories, health score and other numbers are estimates and not medical advice."),
        ],
        legal=[("Privacy policy", "../privacy.html"), ("Delete account & data", "../delete-data.html")],
    ),
    dict(
        slug="noora", name="NOORA", title="NOORA: Fasting & Ramadan", kind="Intermittent fasting · Ramadan",
        accent="#E7B75A", accent_text="#9A6A12", ink="#1D1B18", hero="#0E1320",
        short="The honest fasting companion: evidence-labelled stages, a safety check first and a free Ramadan mode.",
        lead="The intermittent fasting app that tells you the truth. Evidence-labelled fasting stages, a safety check before any plan, and a free Ramadan mode with your country's prayer times.",
        features=[
            ("hourglass-medium", "An honest fasting ring", "Six stages, each marked Strong, Some, Animal-lab or Myth. No fake “detox” mode."),
            ("shield-check", "Safety check first", "A 60-second screening keeps every plan right for you before you start."),
            ("moon-stars", "Free Ramadan mode", "Suhoor and iftar countdowns, hydration pacing, excused days and qada, and diabetes guidance."),
            ("calendar-check", "Sunnah fasts", "Monday & Thursday, Ayyam al-Bid, Shawwal Six, Arafah and Ashura, with Hijri dates."),
            ("camera", "Camera meal log", "Snap a meal and see honest calorie ranges instead of fake-precise numbers."),
            ("cooking-pot", "Gulf & Arab recipes", "Kabsa, machboos, harees, lentil soup, fattoush and more for breaking your fast."),
            ("trend-up", "Weekly goals, not streaks", "Aim for 5 of 7 days, with 2 free breaks a month. No guilt."),
            ("translate", "Arabic first", "Full right-to-left Arabic interface with optional Arabic-Indic digits, plus English."),
        ],
        shots=["Fasting ring", "Today", "Ramadan mode", "Meals"],
        split=("Real science, real prices", "NOORA never paywalls safety. The free plan stays useful for good.",
               ["Safety features, Ramadan mode and protein tracking are always free",
                "Every claim carries an evidence label", "Prayer times for 14 Arab countries",
                "NOORA Plus has real prices, never fake discounts"], "noora-2"),
        faq=[
            ("Is NOORA free?", "The core app is free forever, including safety screening, Ramadan mode, macros, core plans and 3 camera scans a day. NOORA Plus unlocks every plan and unlimited scans."),
            ("Is fasting safe for me?", "NOORA asks a short safety check first and only offers plans that fit. If you're pregnant, have diabetes or another condition, talk to your doctor. NOORA is not a medical device."),
            ("Which languages?", "Arabic (right-to-left) and English."),
        ],
        legal=[],
    ),
    dict(
        slug="kairo", name="Kairo", title="Kairo: Day Planner & Focus", kind="Planner · Focus · Shared tasks",
        accent="#FF7A59", accent_text="#C2462A", ink="#2A0E05", hero="#13222A",
        short="Turn a messy list into a realistic, time-boxed and forgiving day. Share tasks by email. No ads.",
        lead="Kairo turns a messy list into a realistic, time-boxed, forgiving day. Plan in three minutes, focus deeply, and share tasks with anyone by email.",
        features=[
            ("sun-horizon", "Plan in 3 minutes", "Check your energy, pick what matters and cap it with the 1-3-5 guide. A Reality Bar shows what really fits."),
            ("timer", "Deep focus", "Pomodoro, Flowtime or until the block ends, with 8 soundscapes and a park-it pad for stray thoughts."),
            ("envelope-simple", "Share by email", "Assign a task to anyone, track its status and hand off the next step, with comments and history."),
            ("calendar-check", "Calendar & timeline", "Month, week and agenda views with every task, deadline and reminder."),
            ("kanban", "Boards & projects", "A mini Kanban for projects, plus an Eisenhower matrix and an Upcoming week."),
            ("feather", "Capture in 2 seconds", "Quick add understands “Call Maya tomorrow 3pm 20m #work”."),
            ("moon", "Close the day kindly", "A 2-minute shutdown. Unfinished tasks go to a Rescue Tray, not a red overdue wall."),
            ("users", "Made for every brain", "Focus-friendly (ADHD), low-stimulus, dyslexia-friendly and high-contrast modes."),
        ],
        shots=["Today", "Week calendar", "Focus timer", "Shared board"],
        split=("Private by design", "Your plan is yours. Kairo has no ads and no analytics.",
               ["Tasks you don't share stay on your phone", "Export everything any time",
                "Estimates improve from your own history, on your phone", "Free, with no in-app purchases"], "kairo-2"),
        faq=[
            ("Is Kairo free?", "Yes. Kairo 1.0 is free, with no ads and no in-app purchases."),
            ("Do the people I share with need Kairo?", "No. Assign-by-email works with anyone; the task arrives in their own email or chat app."),
            ("Is Kairo a medical app?", "No. Kairo is a productivity tool. Its focus-friendly modes are design choices, not treatment."),
        ],
        legal=[("Privacy policy", "privacy.html")],
    ),
    dict(
        slug="mauna", name="Mauna", title="Mauna: Calm Home Screen", kind="Calm Android launcher",
        accent="#00CBA9", accent_text="#007A66", ink="#04211C", hero="#0A1211",
        short="Your phone, quiet by default. A calm launcher with a breath before noisy apps.",
        lead="Mauna, Sanskrit for “sacred silence”, turns your Android phone into a calm home screen without giving up WhatsApp, maps, banking or your camera.",
        features=[
            ("house-simple", "Seven apps, not seventy", "Your home screen shows only your Essential Seven. Everything else is one quick search away."),
            ("wind", "A breath before noisy apps", "A short breathing pause asks what you're here for. Open it for 5, 10 or 15 minutes, or earn a seed."),
            ("bell-simple-slash" if False else "moon-stars", "Calm Digest", "Chosen apps send notifications in three calm batches a day. Calls, alarms and codes always come through."),
            ("plant", "Calm Days, not guilt", "Aim for 4 calm days out of 7. Freeze Leaves cover busy days, and Sunday brings a short reflection."),
            ("palette", "56 themes", "Dark and light, nature, spiritual calm, ink and paper, and retro handsets with a working T9 keypad."),
            ("game-controller", "A tiny retro arcade", "Snake, Bricks, Blocks and Pairs, capped at 3 rounds a day so it stays a treat."),
            ("heart", "Senior Mode", "Big tiles, large text, spoken labels, family call tiles and an SOS tile. Always free."),
            ("translate", "English, العربية, हिन्दी", "Full right-to-left layout for Arabic."),
        ],
        shots=["Home", "Breath Gate", "Retro theme", "Senior Mode"],
        split=("Nothing leaves your phone", "Mauna doesn't even ask for internet permission.",
               ["No ads, no account, no trackers", "Everything stays on your device",
                "Erase all Mauna data from Settings any time", "Free during launch"], "mauna-2"),
        faq=[
            ("Will I lose access to my apps?", "No. Every app is still one quick search away. Mauna only adds a gentle pause before the ones you mark as noisy."),
            ("Will I miss important notifications?", "Calls, alarms, one-time codes and the people you name always come through straight away."),
            ("Is Mauna for iPhone?", "Mauna is an Android launcher. iPhone doesn't allow replacing the home screen."),
        ],
        legal=[("Privacy policy", "privacy.html")],
    ),
    dict(
        slug="unwind", name="Unwind", title="Unwind: Relax, Breathe & Sleep", kind="Breathing · Sleep · Calm games",
        accent="#6CC3B2", accent_text="#2F7F70", ink="#0B1715", hero="#0E1A1E",
        short="Self-care in minutes: breathing, meditations, sleep stories, nature sounds and calm games. No ads.",
        lead="Short breathing exercises, guided meditations, sleep stories, real nature sounds and soothing games help you relax and manage everyday stress, one to ten minutes at a time.",
        features=[
            ("hand-heart", "Start with how you feel", "Anxious, low, bored, can't focus, can't sleep or on the move: Unwind suggests what fits."),
            ("wind", "Breathe", "7 guided patterns with a glowing guide and soft haptics, plus an SOS calmer minute from any screen."),
            ("flower-lotus", "Meditate", "10 guided meditations from 3 to 10 minutes, and a timer with singing-bowl bells."),
            ("moon-stars", "Sleep", "6 sleep stories over slow nature video. The screen dims as you read."),
            ("music-notes", "Sounds", "Real rain, ocean, forest and fireplace recordings. Mix your own, with a gentle sleep timer."),
            ("puzzle-piece", "30 calm games", "Tide Pool, Koi Pond, Sand Garden, Worry Lanterns, a Daily Calm puzzle and more."),
            ("plant", "Your garden", "Every finished activity grows your garden. Missed days simply become rest days."),
            ("lifebuoy", "Help when you need it", "Free helplines for more than 20 countries, one tap away."),
        ],
        shots=["How do you feel?", "Breathe", "Relax", "Sleep story", "Your garden"],
        split=("Made to feel calm", "Silent-first, one-handed and offline. Everything has a natural end.",
               ["No sign-up, no ads, no tracking", "Moods, worries and notes stay on your phone",
                "15 soothing themes, reduced motion and a simple & large mode", "English, Arabic, Hindi and Urdu"], "unwind-2"),
        faq=[
            ("Is Unwind free?", "Yes. Everything in Unwind is free."),
            ("Can Unwind treat anxiety?", "No. Unwind is a general wellness app that helps you relax. It does not diagnose or treat any condition. If you often feel low or anxious, please talk to a doctor."),
            ("Does it need the internet?", "No. Unwind works offline and keeps your data on your phone."),
        ],
        legal=[("Privacy policy", "privacy.html"), ("Delete your data", "delete-data.html")],
    ),
    dict(
        slug="dailygrowth", name="Daily Growth", title="Habit Tracker: Daily Growth", kind="Habits · Journeys · Insights",
        accent="#FFB37A", accent_text="#2F7D61", ink="#3A2410", hero="#13241D",
        short="Forgiving streaks, a minimum version for every habit, guided Journeys and Lumi, a companion that grows with you.",
        lead="A habit tracker that forgives. Do the full or the minimum version, let Shields cover busy days, and follow guided Journeys with Lumi growing alongside you.",
        features=[
            ("plant", "Small wins count", "Every habit has a minimum version. Momentum never resets to zero."),
            ("shield-check", "Forgiving streaks", "Shields cover the days you can't, rest days are built in, and you can repair a streak within 48 hours."),
            ("compass", "34 Journeys", "727 days of guided content across 12 topics, from sleep and focus to money and breaking free."),
            ("list-checks", "105 blueprints", "Ready-made habits with six ways to track: check, counter, timer, routine, journal and quit."),
            ("chart-bar", "Insights", "Consistency, momentum, a year heatmap, peak hours and a weekly review story."),
            ("sparkle", "Meet Lumi", "A companion that grows from Egg to Radiant and never goes backwards."),
            ("users-three", "Circles", "Up to 8 people cheer, nudge and gift each other a Shield."),
            ("palette", "16 themes", "Warm Bloom by default, Bloom Night, larger text, a readable font and high contrast."),
        ],
        shots=["Today", "Journeys", "Insights", "Bloom Night"],
        split=("Your habits, your data", "Private backup, local-only mode and full export.",
               ["Journal text is never backed up unless you opt in", "Export or import JSON and CSV any time",
                "One gentle reminder a day by default, with quiet hours", "Delete your account from the app"], "dailygrowth-2"),
        faq=[
            ("Is Daily Growth free?", "Yes. Everything is free during launch. Lumi's shop uses Glow you earn, never real money."),
            ("What if I miss a day?", "Nothing breaks. Shields cover missed days automatically, and Never Miss Twice helps you get back on track."),
            ("Do I need an account?", "No sign-up form. Daily Growth creates an anonymous account for backup, or you can use local-only mode."),
        ],
        legal=[("Privacy policy", "privacy.html"), ("Delete account & data", "delete-data.html")],
    ),
]


def shot_count(slug):
    d = os.path.join(SITE, "assets", "img", "apps", slug)
    return len([f for f in os.listdir(d) if f.startswith("shot-")])


def head(title, desc, url, image, root, style=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{root}assets/img/bb-logo.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://buddhabytes.app/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{root}assets/fonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/site.css">
<script>document.documentElement.classList.add("js")</script>
{style}</head>
<body>
"""


def nav(root, links):
    items = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in links)
    return f"""<nav class="site-nav">
  <div class="wrap">
    <a class="brand" href="{root or './'}"><img src="{root}assets/img/bb-logo.svg" alt=""> Buddha Bytes</a>
    <div class="nav-links">{items}<a href="mailto:support@buddhabytes.app" class="nav-cta">Contact</a></div>
  </div>
</nav>
"""


def footer(root):
    apps = "".join(f'<a href="{root}{a["slug"]}/">{e(a["name"])}</a>' for a in APPS)
    return f"""<footer>
  <div class="wrap">
    <span>© <span data-year>2026</span> Buddha Bytes · Dubai</span>
    <div class="foot-links">{apps}<a href="mailto:support@buddhabytes.app">support@buddhabytes.app</a></div>
  </div>
</footer>
{YEAR_JS}
{REVEAL_JS}
</body>
</html>
"""


def phone(src, alt, cls="phone", lazy=True):
    lz = ' loading="lazy"' if lazy else ""
    return f'<div class="{cls}"><img src="{src}" alt="{e(alt)}"{lz}></div>'


def accent_style(a):
    return (f"<style>:root{{--accent:{a['accent']};--accent-ink:{a['ink']};--hero-bg:{a['hero']};--accent-text:{a['accent_text']}}}"
            f"@media (prefers-color-scheme:dark){{:root{{--accent-text:{a['accent']}}}}}</style>\n")


def app_page(a):
    n = shot_count(a["slug"])
    caps = a["shots"] or a.get("captions") or [f"{a['name']} screen {i}" for i in range(1, n + 1)]
    img = f"../assets/img/apps/{a['slug']}"
    stack = "".join(phone(f"{img}/shot-{i}.webp", caps[i - 1], lazy=False) for i in (2, 1, 3) if i <= n)
    others = "".join(
        f'<a href="../{o["slug"]}/"><img src="../assets/img/apps/{o["slug"]}/icon.png" alt="" loading="lazy"><span>{e(o["name"])}<small>{e(o["kind"])}</small></span></a>'
        for o in APPS if o is not a)
    feats = "".join(f'<div class="feature reveal"><div class="fi">{ic(i)}</div><h4>{e(t)}</h4><p>{e(d)}</p></div>'
                    for i, t, d in a["features"])
    shots = "".join(f'<figure>{phone(f"{img}/shot-{i}.webp", caps[i - 1], "phone sm")}<figcaption>{e(caps[i - 1])}</figcaption></figure>'
                    for i in range(1, n + 1))
    st, sp, checks, photo = a["split"]
    checks_html = "".join(f"<li>{ic('seal-check')}<span>{e(c)}</span></li>" for c in checks)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in a["faq"])
    legal = "".join(f'<a href="{h}">{ic("lock-simple")} {e(t)}</a>' for t, h in a["legal"])
    legal_block = f'<div class="legal-links">{legal}</div>' if legal else ""
    out = head(f"{a['title']} | Buddha Bytes", a["short"], f"https://buddhabytes.app/{a['slug']}/",
               f"assets/img/photos/{a['slug']}.webp", "../", accent_style(a))
    out += nav("../", [("Features", "#features"), ("Screens", "#screens"), ("FAQ", "#faq"), ("All apps", "../#apps")])
    out += f"""
<header class="photo-hero">
  <img class="bg" src="../assets/img/photos/{a['slug']}.webp" alt="">
  <div class="wrap">
    <div>
      <img class="hero-icon" src="{img}/icon.png" alt="{e(a['name'])} app icon">
      <div class="eyebrow">{e(a['kind'])}</div>
      <h1>{e(a['title'])}</h1>
      <p class="lead">{e(a['lead'])}</p>
      <div class="hero-actions">
        <span class="btn btn-primary">{ic('google-play-logo')} {PLAY_SOON}</span>
        <a class="btn btn-ghost" href="#features">See what's inside</a>
      </div>
    </div>
    <div class="hero-stack" aria-hidden="true">{stack}</div>
  </div>
</header>

<section id="features">
  <div class="wrap">
    <div class="section-head reveal"><h2>What's inside</h2><p>{e(a['short'])}</p></div>
    <div class="feature-grid">{feats}</div>
  </div>
</section>

<section id="screens" class="alt">
  <div class="wrap"><div class="section-head center reveal"><h2>A look inside</h2><p>Real screens from the app.</p></div></div>
  <div class="shot-strip">{shots}</div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <h2>{e(st)}</h2>
      <p>{e(sp)}</p>
      <ul class="checks">{checks_html}</ul>
      {legal_block}
    </div>
    <div class="photo-card reveal"><img src="../assets/img/photos/{photo}.webp" alt="" loading="lazy"></div>
  </div>
</section>

<section id="faq" class="alt">
  <div class="wrap">
    <div class="section-head center reveal"><h2>Questions</h2><p>Anything else? Write to <a href="mailto:support@buddhabytes.app">support@buddhabytes.app</a>.</p></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><h2>More from Buddha Bytes</h2></div>
    <div class="mini-apps">{others}</div>
  </div>
</section>

"""
    out += footer("../")
    os.makedirs(os.path.join(SITE, a["slug"]), exist_ok=True)
    with open(os.path.join(SITE, a["slug"], "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


def home():
    cards = "".join(f"""
      <a class="app-card reveal" href="{a['slug']}/" style="--accent:{a['accent']};--accent-ink:{a['ink']};--hero-bg:{a['hero']}">
        <img class="bg" src="assets/img/photos/{a['slug']}.webp" alt="" loading="lazy">
        <div class="top"><img src="assets/img/apps/{a['slug']}/icon.png" alt=""><div><h3>{e(a['name'])}</h3><div class="kind">{e(a['kind'])}</div></div></div>
        <p>{e(a['short'])}</p>
        <span class="tag">{PLAY_SOON}</span>
        <div class="peek">{phone(f"assets/img/apps/{a['slug']}/shot-1.webp", a['title'] + ' screenshot')}</div>
        <span class="go" aria-hidden="true">{ic('arrow-right')}</span>
      </a>""" for a in APPS)
    principles = [
        ("hand-heart", "Help first, never manipulate", "No dark patterns, fake counters or guilt-driven streaks. Our apps end on purpose."),
        ("lock-simple", "Private by design", "No ads in any app. We collect only what a feature needs, and you can delete it any time."),
        ("seal-check", "Honest claims", "Health numbers are labelled as estimates, evidence is graded, and prices are real."),
        ("translate", "Made for the Gulf & South Asia", "Regional food, Ramadan, Hijri dates, and English, Arabic and Hindi across our apps."),
        ("flower-lotus", "Calm by design", "Gentle motion, soothing themes and reminders that respect your time."),
        ("users", "For everyone", "Senior Mode, larger text, reduced motion, high contrast and focus-friendly modes."),
    ]
    pr = "".join(f'<div class="feature reveal"><div class="fi">{ic(i)}</div><h4>{e(t)}</h4><p>{e(d)}</p></div>' for i, t, d in principles)
    stack = "".join(phone(f"assets/img/apps/{s}/shot-1.webp", "", lazy=False) for s in ("unwind", "rise", "dailygrowth"))
    out = head("Buddha Bytes | Calm, honest apps for everyday life",
               "Buddha Bytes is an independent app studio in Dubai making calm, honest apps: Rise, NOORA, Kairo, Mauna, Unwind and Daily Growth.",
               "https://buddhabytes.app/", "assets/img/photos/home.webp", "")
    out += nav("", [("Apps", "#apps"), ("Approach", "#approach"), ("About", "#about")])
    out += f"""
<header class="photo-hero">
  <img class="bg" src="assets/img/photos/home.webp" alt="">
  <div class="wrap">
    <div>
      <div class="eyebrow">An independent app studio · Dubai</div>
      <h1>Calm, honest apps for everyday life</h1>
      <p class="lead">Six apps that help you move, eat, focus, rest and grow a little better, without ads, dark patterns or noise.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#apps">Explore our apps {ic('arrow-right')}</a>
        <a class="btn btn-ghost" href="#approach">Our approach</a>
      </div>
    </div>
    <div class="hero-stack" aria-hidden="true">{stack}</div>
  </div>
</header>

<section id="apps">
  <div class="wrap">
    <div class="section-head reveal"><h2>Our apps</h2><p>Each one does one thing well. All are coming soon to Google Play.</p></div>
    <div class="app-grid">{cards}
    </div>
  </div>
</section>

<section id="approach" class="alt">
  <div class="wrap">
    <div class="section-head reveal"><h2>One rule: help first</h2><p>Every Buddha Bytes app follows the same principles.</p></div>
    <div class="feature-grid">{pr}</div>
  </div>
</section>

<section id="about">
  <div class="wrap about-grid">
    <div class="reveal">
      <h2 style="font-size:clamp(1.8rem,3.6vw,2.6rem);margin:0 0 14px">About Buddha Bytes</h2>
      <p>Buddha Bytes is an independent app studio based in Dubai. We design for genuine, healthy engagement: clear numbers, honest defaults and features people actually asked for, instead of streaks and pressure designed to keep you scrolling.</p>
      <p>Our apps are built for the Gulf and South Asia first, with regional food, Ramadan and local languages, and work for anyone, anywhere.</p>
      <div class="stat-row"><div><b>6</b><span>apps</span></div><div><b>0</b><span>ads</span></div><div><b>3</b><span>languages</span></div></div>
    </div>
    <div class="contact-card reveal" id="contact">
      <img class="bg" src="assets/img/photos/mauna.webp" alt="" loading="lazy">
      <h3>Get in touch</h3>
      <p>Questions, feedback or support requests. We read everything.</p>
      <p><a href="mailto:support@buddhabytes.app">support@buddhabytes.app</a></p>
    </div>
  </div>
</section>

"""
    out += footer("")
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


if __name__ == "__main__":
    for a in APPS:
        app_page(a)
    home()
    print("built", len(APPS) + 1, "pages")
