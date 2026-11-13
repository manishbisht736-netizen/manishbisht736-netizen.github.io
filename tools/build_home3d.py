"""Build the Stryka-only home page (13 Nov 2026): index.html + assets/js/home3d.js.

  python tools/build_home3d.py

- Text lives here (CHAPTERS, SPECS, plans, FAQ). Keep it true to the app: estimates marked est., no prices
  (they differ by country and are shown in the app), no claims the app doesn't make.
- 3D/motion code: tools/home3d/main.js, bundled + minified with esbuild (npx esbuild) into assets/js/home3d.js.
  three.js r186 (MIT) is vendored from the Design-Library in tools/home3d/vendor/three.
- Screens/clips: assets/img/apps/rise/*.webp and assets/video/stryka/*.webm (see tools/prepare_assets.py and the
  Stryka repo's store/web-motion/record.js).
- The other apps are no longer shown on the site. Their privacy / delete-data / help pages stay online because their
  store listings link to them; their old landing pages are unlinked.
"""
import html, os, re, subprocess

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(SITE, "tools", "home3d")
e = html.escape
PLAY = "https://play.google.com/store/apps/details?id=com.buddhabytes.rise"
IMG, VID, CARDS = "assets/img/apps/rise", "assets/video/stryka", "assets/img/stryka-cards"

# (index label, title, text, spec label, spec value, screen, clip or None, phone side)
CHAPTERS = [
    ("Readiness", "Know when to push",
     "One Readiness number every morning from your sleep, HRV, resting heart rate and training load, compared with your own normal. Then one clear thing to do today.",
     "Compared with", "Your 30-day normal (est.)", "shot-1", "pulse", "l"),
    ("Sleep debt", "The sleep you owe",
     "Stryka adds up the sleep you missed over the last 14 nights, with recent nights counting more, and shows when you're paying it back. Nights with no data are skipped, never counted as short.",
     "Looks back", "14 nights", "tour-ins-heat", None, "r"),
    ("Trends", "Every trend. One place.",
     "HRV, heart rate, sleep, steps, weight and training in week, month, 3-month and year views, each compared with the weeks before. Fitness, fatigue and form with a race-day forecast.",
     "Views", "W · M · 3M · Y", "tour-ins-vitals", "insights", "l"),
    ("Peak hours", "Find your prime time",
     "The energy clock learns from your own sleep, movement and sessions when you tend to perform best, and shows your daily peak window.",
     "Learned from", "Your own data (est.)", "tour-ins-clock", None, "r"),
    ("Runs", "Run on a 3D map",
     "Live GPS on a tilted 3D street map with buildings: pace, splits, elevation and auto-pause. Suggested loops for the distance you pick. Keeps recording with the screen locked.",
     "Running features", "Free", "shot-3", "run", "l"),
    ("Run replay", "Watch it again",
     "Tap Replay and your route draws itself on the real map while your pace ticks along. Save it as a short 9:16 video and share it to any app on your phone. The start and end of your route stay hidden.",
     "Format", "9:16 video", "tour-run-finish", "replay", "r"),
    ("3D coach", "Every move in 3D",
     "Recorded 3D videos for every exercise, with the working muscles lit, set timers and your last weight. My Plan adapts from 30 to 90 minutes, at the gym or at home.",
     "Exercises", "400+", "shot-4", "coach", "l"),
    ("Food", "Snap. Log. Done.",
     "Snap a meal, scan a barcode or search 1,000+ foods from around the world. Calories, protein, carbs and fat against your daily targets (est.), plus water and fasting.",
     "Foods", "1,000+", "shot-5", None, "r"),
    ("Mind", "Breathe. Focus. Rest.",
     "Monk mode for distraction-free focus, guided breathing and real recorded nature sounds for focus, study and sleep.",
     "Price", "Free", "shot-6", None, "l"),
]
# big visuals per chapter: ("c", card) · ("v", clip, poster, crop aspect) · ("i", screen, crop aspect)
VIS = {
    "Readiness": [("c", "readiness"), ("c", "orbs")],
    "Sleep debt": [("c", "sleep-debt"), ("c", "sleep-stages")],
    "Trends": [("c", "trends"), ("c", "vs-normal")],
    "Peak hours": [("c", "energy-clock"), ("c", "perform-best")],
    "Runs": [("v", "run", "shot-3", "540/860")],
    "Run replay": [("v", "replay", "tour-run-finish", "540/900")],
    "3D coach": [("v", "coach", "shot-4", "540/760")],
    "Food": [("c", "food-macros"), ("c", "food-meals")],
    "Mind": [("i", "shot-6", "540/900")],
}
# "The analysis" wall: more insight cards, captions say what each one is
WALL = [("ins-today", "Readiness, explained point by point"), ("ff", "Fitness, fatigue & form with a race forecast"),
        ("stands-out", "What stands out this week"), ("tiles", "Today's vitals vs your 30-day normal"),
        ("heat", "Your aerobic engine in the heat"), ("week", "Weeks on target, not streaks")]
SPECS = [
    ("Works with", "Health Connect", "Steps, sleep, heart rate, HRV and workouts, with your permission"),
    ("Languages", "EN · العربية · हिन्दी", "Full right-to-left Arabic"),
    ("Units", "kg ⇄ lb", "Stored once, shown your way"),
    ("Themes", "Dark · Light · Auto", "Auto follows your phone"),
    ("Ads", "0", "None. Not now, not later"),
    ("Sharing", "Picture or video", "To any app your phone offers"),
    ("Your data", "Yours", "Delete your account and data any time, from the app"),
    ("Health numbers", "Estimates", "Never a diagnosis, never medical advice"),
]
FREE = ["All running: GPS, 3D map, replay and race plans", "Health insights for this week and last week",
        "Monk, Vibes and guided breathing", "Food diary, barcode and water, plus 1 AI food scan a day",
        "About half the workouts and 3 plans", "Sweat Stories, groups and invites"]
PRO = ["Every workout and plan", "Insights for month, 3 months and year", "Unlimited AI food scans",
       "Ask Coach", "Create friend challenges", "Gym progress charts"]
FAQ = [
    ("Is Stryka free?", "You can try every feature free for 7 days from install, with no card needed. After that, keep the free plan or subscribe to Stryka Premium in the app. Prices are shown clearly before you pay."),
    ("Does Stryka work with my watch?", "On Android, Stryka reads steps, sleep, heart rate, HRV and workouts from Health Connect, with your permission. You can also log them yourself. The iPhone version, with Apple Health, is coming soon."),
    ("Do I need gym equipment?", "No. Pick home or no-equipment plans and Stryka only shows exercises you can do with what you have."),
    ("Is Stryka medical advice?", "No. Stryka is a wellness app. Readiness, calories and other numbers are estimates and not medical advice."),
    ("Can I delete my data?", "Yes. Delete your account and data any time from the app, or follow the steps on our delete-data page."),
]


def build():
    t = open(os.path.join(H, "index.template.html"), encoding="utf-8").read()
    mark = open(os.path.join(SITE, "assets", "img", "stryka-mark.svg"), encoding="utf-8").read()
    m = re.search(r'<path transform="([^"]+)"[^>]*\sd="([^"]+)"', mark)
    play_icon = open(os.path.join(SITE, "assets", "icons", "google-play-logo.svg"), encoding="utf-8").read().replace("<svg ", '<svg class="ic" aria-hidden="true" ', 1)
    chs = []
    def fig(v, k, lab):
        if v[0] == "c":
            return f'<figure class="vc v{k}"><img src="{CARDS}/{v[1]}.webp" alt="Stryka: {e(lab)}" loading="lazy" decoding="async"></figure>'
        if v[0] == "v":
            return (f'<figure class="vc v{k} vv" style="aspect-ratio:{v[3]}"><video class="lv" data-src="{VID}/{v[1]}.webm" poster="{IMG}/{v[2]}.webp" '
                    f'muted loop playsinline preload="none" aria-label="Stryka: {e(lab)}"></video></figure>')
        return f'<figure class="vc v{k} vv" style="aspect-ratio:{v[2]}"><img src="{IMG}/{v[1]}.webp" alt="Stryka: {e(lab)}" loading="lazy"></figure>'
    for n, (lab, title, text, sl, sv, scr, vid, side) in enumerate(CHAPTERS, 1):
        vis = "".join(fig(v, k, lab) for k, v in enumerate(VIS[lab], 1))
        chs.append(f'''<section class="ch {'ch-l' if side == 'r' else 'ch-r'}" data-scr="{IMG}/shot-1.webp" data-away="1">
  <div class="ch-in">
    <p class="mono kicker rv">[ {n:02d} / {len(CHAPTERS):02d} ] {e(lab.upper())}</p>
    <h2 class="split rv">{e(title)}</h2>
    <p class="body rv">{e(text)}</p>
    <dl class="spec rv"><dt class="mono">{e(sl.upper())}</dt><dd>{e(sv)}</dd></dl>
  </div>
  <div class="vis rv n{len(VIS[lab])}">{vis}</div>
</section>''')
    wall = "".join(f'<figure class="wc rv"><figcaption class="mono">{e(c)}</figcaption><img src="{CARDS}/{n}.webp" alt="Stryka: {e(c)}" loading="lazy" decoding="async"></figure>' for n, c in WALL)
    specs = "".join(f'<div class="sc rv"><p class="mono">{e(a.upper())}</p><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in SPECS)
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    faq = "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    out = (t.replace("__MARK_TRANSFORM__", m.group(1)).replace("__MARK_D__", m.group(2)).replace("__PLAY_ICON__", play_icon)
            .replace("__PLAY__", PLAY).replace("__CHAPTERS__", "\n".join(chs)).replace("__SPECS__", specs)
            .replace("__FREE__", li(FREE)).replace("__PRO__", li(PRO)).replace("__FAQ__", faq).replace("__WALL__", wall))
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    # /rise/ was Stryka's page: send it to the new home (store listings and old links keep working)
    with open(os.path.join(SITE, "rise", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Stryka</title>'
                '<link rel="canonical" href="https://buddhabytes.app/"><meta http-equiv="refresh" content="0; url=../">'
                '<script>location.replace("../"+location.hash)</script></head><body><a href="../">Stryka</a></body></html>\n')
    subprocess.run(["npx", "-y", "esbuild", os.path.join(H, "main.js"), "--bundle", "--minify", "--format=iife", "--target=es2020",
                    "--alias:three=" + os.path.join(H, "vendor", "three", "three.module.js"),
                    "--outfile=" + os.path.join(SITE, "assets", "js", "home3d.js")], check=True, shell=(os.name == "nt"))
    print("built index.html + assets/js/home3d.js")


if __name__ == "__main__":
    build()
