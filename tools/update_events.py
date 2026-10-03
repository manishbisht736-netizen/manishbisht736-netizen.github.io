"""Monthly refresh of events.json (Rise race calendar) using Gemini with Google Search grounding (free tier).
Run by .github/workflows/update-events.yml. Needs env GEMINI_API_KEY. Safe by design:
- only keeps events with an ISO date in the next 12 months and an https link,
- never deletes an existing future event just because Gemini left it out,
- refuses to write if the answer looks broken (too few events), so a bad month changes nothing.
Local test: GEMINI_API_KEY=... python tools/update_events.py --dry-run"""
import datetime as dt, json, os, re, sys, urllib.request

MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
KEY = os.environ.get('GEMINI_API_KEY', '')
PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'events.json')
DRY = '--dry-run' in sys.argv
today = dt.date.today()
horizon = today + dt.timedelta(days=380)

PROMPT = f"""Today is {today.isoformat()}. Search the web for the official dates of major public running, walking and cycling
events open to amateurs in the UAE, Saudi Arabia, Qatar, Oman, Bahrain, Kuwait and India between {today.isoformat()} and {horizon.isoformat()}.
Include big city marathons, half marathons, 10K races, Dubai Run, Dubai Ride and the Dubai Fitness Challenge.
Only include an event if you found its date on the organiser's site or in reputable news.
Answer ONLY with a JSON array inside a ```json code block. Each item:
{{"n": event name, "city": city, "cc": two-letter country code, "date": "YYYY-MM-DD" (race day; first day if several),
 "end": "YYYY-MM-DD" or null, "dist": distances like "42.2 km · 21.1 km · 10 km", "sport": "run"|"ride"|"walk"|"challenge",
 "status": "confirmed" if the organiser or major news published the date, else "expected",
 "url": official registration or event page (https), "source": the page where you found the date (https),
 "lat": start-area latitude (number), "lng": start-area longitude (number)}}"""


def ask():
    body = {"contents": [{"parts": [{"text": PROMPT}]}], "tools": [{"google_search": {}}], "generationConfig": {"temperature": 0.2}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
                                 data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        j = json.load(r)
    text = "".join(p.get("text", "") for c in j.get("candidates", []) for p in c.get("content", {}).get("parts", []))
    m = re.search(r"```json\s*(\[.*?\])\s*```", text, re.S) or re.search(r"(\[\s*{.*}\s*\])", text, re.S)
    if not m:
        raise SystemExit("Gemini answer had no JSON list; nothing changed")
    return json.loads(m.group(1))


def slug(e):
    return re.sub(r"[^a-z0-9]+", "-", f"{e['n']} {e['date'][:4]}".lower()).strip("-")


def valid(e):
    try:
        d = dt.date.fromisoformat(e["date"])
        end = dt.date.fromisoformat(e["end"]) if e.get("end") else d
    except Exception:
        return False
    return (today <= end and d <= horizon and str(e.get("url", "")).startswith("https://") and e.get("n") and e.get("city")
            and len(str(e.get("cc", ""))) == 2 and e.get("sport") in ("run", "ride", "walk", "challenge"))


def main():
    if not KEY:
        raise SystemExit("GEMINI_API_KEY is not set")
    old = json.load(open(PATH, encoding="utf-8"))
    found = [e for e in ask() if isinstance(e, dict) and valid(e)]
    if len(found) < 4:
        raise SystemExit(f"Only {len(found)} valid events came back; keeping the current list")
    by = {}
    for e in old.get("events", []):  # keep current future events (Gemini may simply have missed them)
        if valid(dict(e, cc=e.get("cc", "XX"))):
            by[e["id"]] = e
    for e in found:
        e = {k: e.get(k) for k in ("n", "city", "cc", "date", "end", "dist", "sport", "status", "url", "lat", "lng")}
        for k in ("lat", "lng"):
            if not isinstance(e.get(k), (int, float)): e.pop(k, None)
        if not e.get("end"):
            e.pop("end", None)
        e["status"] = e["status"] if e.get("status") in ("confirmed", "expected") else "expected"
        e["id"] = slug(e)
        # same event, new date: replace the old entry with the same name and year
        for k, o in list(by.items()):
            if o["n"].lower() == e["n"].lower() and o["date"][:4] == e["date"][:4]:
                del by[k]
        by[e["id"]] = e
    events = sorted(by.values(), key=lambda e: e["date"])
    out = dict(old, updated=today.isoformat(), events=events)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not DRY:
        open(PATH, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
        print(f"events.json updated: {len(events)} events")


if __name__ == "__main__":
    main()
