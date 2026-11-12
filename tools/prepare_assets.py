"""Copy and compress the website's images and fonts.

Sources: the owner's Design Library (photos, fonts, Phosphor icons) and each app's own repo
(app icons and screenshots). Run on the owner's PC:  python tools/prepare_assets.py
Every file used is listed in CREDITS.md.
"""
import glob, os, shutil
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = r"C:\Users\user\Documents\Design-Library"
if not os.path.isdir(LIB):
    LIB = r"D:\Desktop\Design-Library"
PHOTOS = r"D:\Desktop\Design-Library\05-Photos"
HOME = r"C:\Users\user"
STRYKA = rf"{HOME}\Documents\Codex\2026-10-31\ac\work\stryka"
STRYKA_RAW = rf"{STRYKA}\store\screenshots-play-1314\src\raw"
# Stryka feature-tour screens (12 Nov 2026), saved as tour-<name>.webp; rows are defined in build_site.py
STRYKA_TOUR = ("ins-heat", "ins-vitals", "ins-ff", "ins-clock", "run-loop", "run-finish", "share-rphoto")
SHOTS_TMP = os.environ.get("SHOTS_DIR", "")  # fresh screenshots of Fastwise/Kairo/Mauna (optional)

IMG = os.path.join(SITE, "assets", "img")

# Hero photos (Unsplash licence) from the Design Library, by Unsplash photo id
PHOTO_IDS = {
    "home": "4iTVoGYY7bM", "rise": "a6FHROHuQ9o", "fastwise": "tIL1v1jSoaY", "kairo": "tPRFj3A1rxo",
    "mauna": "SyGaxTcJl3g", "unwind": "oQl0eVYd_n8", "dailygrowth": "OlexUO10-wM",
    # second photo for each app page's "privacy / promise" block
    "rise-2": "n2RKRotiNoM", "fastwise-2": "MljwsnGwdOY", "kairo-2": "Lks7vei-eAg", "mauna-2": "lA_EKRdsMcE",
    "unwind-2": "W7AyAs7azHc", "dailygrowth-2": "GUKZev71amQ",
}

ICONS = {
    "rise": rf"{STRYKA}\store\icon-512.png",
    "fastwise": rf"{HOME}\fasting-app\assets\icon-only.png",
    "kairo": rf"{HOME}\kairo-app\store\icon-512.png",
    "mauna": rf"{HOME}\mauna-app\store\icon-512.png",
    "unwind": rf"{HOME}\sukoon-app\store\icon-512.png",
    "dailygrowth": rf"{HOME}\habit-tracker-app\assets\icon-only.png",
}

SCREENS = {
    "rise": [rf"{STRYKA_RAW}\{n}.jpg" for n in ("pulse", "ins-ov", "run-live", "player-plank", "food", "monk")],
    "unwind": [rf"{HOME}\sukoon-app\store\screenshots\{n}.png" for n in
               ("01-now", "04-breathe", "03-relax", "06-sleep-story", "07-garden")],
    "dailygrowth": [rf"{HOME}\habit-tracker-app\docs\screens\{n}.png" for n in
                    ("bloom-today", "bloom-journeys", "bloom-insights", "bloom-night-today")],
}
for app in ("fastwise", "kairo", "mauna"):
    if SHOTS_TMP:
        SCREENS[app] = sorted(glob.glob(os.path.join(SHOTS_TMP, app, "[0-9].png")))

ICON_NAMES = """barbell person-simple-run bowl-food camera heartbeat brain headphones users-three moon-stars
hourglass-medium shield-check calendar-check cooking-pot seal-check timer kanban envelope-simple list-checks
sun-horizon wind house-simple palette game-controller lock-simple translate flower-lotus leaf music-notes plant
compass chart-bar sparkle puzzle-piece moon lifebuoy hand-heart arrow-right google-play-logo heart users
book-open-text trend-up feather arrow-left bed chart-line-up clock cube gauge map-trifold play-circle share-network""".split()


def save_webp(src, dst, width, quality=78):
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)


def main():
    for key, pid in PHOTO_IDS.items():
        src = [p for p in glob.glob(os.path.join(PHOTOS, "*", "*.jpg")) if pid in p][0]
        save_webp(src, os.path.join(IMG, "photos", f"{key}.webp"), 1800, 72)
    for app, src in ICONS.items():
        im = Image.open(src).convert("RGBA").resize((256, 256), Image.LANCZOS)
        os.makedirs(os.path.join(IMG, "apps", app), exist_ok=True)
        im.save(os.path.join(IMG, "apps", app, "icon.png"), optimize=True)
    for app, files in SCREENS.items():
        out = os.path.join(IMG, "apps", app)
        for old in glob.glob(os.path.join(out, "shot-*.webp")):
            os.remove(old)
        for i, src in enumerate(files, 1):
            save_webp(src, os.path.join(out, f"shot-{i}.webp"), 540, 80)
    for n in STRYKA_TOUR:
        save_webp(os.path.join(STRYKA_RAW, f"{n}.jpg"), os.path.join(IMG, "apps", "rise", f"tour-{n}.webp"), 540, 82)
    fonts = os.path.join(SITE, "assets", "fonts")
    os.makedirs(fonts, exist_ok=True)
    for fam, weights in (("fraunces", (400, 600)), ("plus-jakarta-sans", (400, 500, 700, 800))):
        for w in weights:
            shutil.copy(os.path.join(LIB, "06-Fonts", fam, f"{fam}-latin-{w}-normal.woff2"), fonts)
        shutil.copy(os.path.join(LIB, "06-Fonts", fam, "LICENSE-OFL.txt"), os.path.join(fonts, f"{fam}-OFL.txt"))
    icons = os.path.join(SITE, "assets", "icons")
    os.makedirs(icons, exist_ok=True)
    for n in ICON_NAMES:
        shutil.copy(os.path.join(LIB, "01-Icons-Phosphor", "svg", "duotone", f"{n}-duotone.svg"),
                    os.path.join(icons, f"{n}.svg"))
    shutil.copy(os.path.join(LIB, "01-Icons-Phosphor", "LICENSE.txt"), os.path.join(icons, "PHOSPHOR-LICENSE.txt"))
    print("done")


if __name__ == "__main__":
    main()
