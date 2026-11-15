"""Safety check for a rebuilt kit.json. Run from the repo root before every push:

    python3 tools/check.py

It compares the new kit.json with the copy already published (git HEAD:kit.json).
Exit code 0 = safe to publish. Any FAIL line = do not push; fix the data or stop and report.

Why each rule exists:
- Players' progress is saved by id, so an id that disappears or changes wipes somebody's checkmarks.
- The app opens Intel sections "route" and "manuals" by id.
- The app's map viewer may only open the hosts in safeMap. In Oct 2026 a fan site started redirecting
  visitors to scam pages, so the map and every link in this file stay on a short list of known hosts.
"""
import datetime
import json
import re
import subprocess
import sys

# Links may only point at these sites (or their subdomains). Adding a host here is a human decision.
ALLOWED_HOSTS = {
    "callofduty.com", "codcentral.net", "codmunity.gg", "dmzmap.com", "dmzradar.com", "dmztracker.gg",
    "gamerant.com", "gamerfuzion.com", "allthings.how", "ggranked.com", "github.com",
}
BANNED_TEXT = ("dmzcodex", "oceanpoet")
REQUIRED_SECTIONS = ("route", "manuals")
ID_LISTS = ("weapons", "items", "upgrades", "recipes", "cats", "lines")

fails, notes = [], []


def fail(msg):
    fails.append(msg)


raw = open("kit.json", encoding="utf-8").read()
try:
    new = json.loads(raw)
except ValueError as e:
    print("FAIL kit.json is not valid JSON:", e)
    sys.exit(1)
old = json.loads(subprocess.run(["git", "show", "HEAD:kit.json"], capture_output=True, text=True, check=True).stdout)

# --- rev and basics
if new.get("schema") != old.get("schema"):
    fail(f"schema changed {old.get('schema')} -> {new.get('schema')} (older builds can't read a new schema)")
rev = new.get("rev")
if not isinstance(rev, int) or not re.fullmatch(r"20\d{8}", str(rev)):
    fail(f"rev must be an integer yyyymmddNN, got {rev!r}")
else:
    if rev <= old["rev"]:
        fail(f"rev must go up: published {old['rev']}, new {rev}")
    try:
        day = datetime.date(int(str(rev)[:4]), int(str(rev)[4:6]), int(str(rev)[6:8]))
        if day > datetime.date.today() + datetime.timedelta(days=1):
            fail(f"rev date {day} is in the future")
    except ValueError:
        fail(f"rev {rev} does not start with a real date")
for key in ("asOf", "notice"):
    if not isinstance(new.get(key), str) or not new[key].strip():
        fail(f"{key} is missing or empty")
if len(raw) > 1_000_000:
    fail(f"kit.json is {len(raw):,} bytes; something is wrong")

# --- ids: nothing published may disappear, nothing may be duplicated
for k in ID_LISTS:
    old_ids = [x["id"] for x in old.get(k, [])]
    new_ids = [x["id"] for x in new.get(k, [])]
    gone = sorted(set(old_ids) - set(new_ids))
    if gone:
        fail(f"{k}: ids removed or renamed: {gone}")
    dupes = sorted({i for i in new_ids if new_ids.count(i) > 1})
    if dupes:
        fail(f"{k}: duplicate ids {dupes}")
    added = sorted(set(new_ids) - set(old_ids))
    if added:
        notes.append(f"{k}: added {added}")
    old_names = {x["id"]: x.get("name") for x in old.get(k, [])}
    for x in new.get(k, []):
        if x["id"] in old_names and old_names[x["id"]] != x.get("name"):
            notes.append(f"{k}: {x['id']} renamed {old_names[x['id']]!r} -> {x.get('name')!r}")

# --- intel sections the app opens by id
sections = [s["id"] for s in new.get("intel", [])]
for sid in REQUIRED_SECTIONS:
    if sid not in sections:
        fail(f"intel section {sid!r} is missing")
dropped = sorted(set(s["id"] for s in old.get("intel", [])) - set(sections))
if dropped:
    notes.append(f"intel sections dropped: {dropped}")
for s in new.get("intel", []):
    for b in s.get("blocks", []):
        if b.get("type") not in ("p", "note", "table", "steps", "kv", "links"):
            fail(f"intel {s['id']}: unknown block type {b.get('type')!r} (the app would show nothing)")

# --- the map never changes without James
for key in ("mapURL", "safeMap"):
    if new.get(key) != old.get(key):
        fail(f"{key} changed. The map is only changed by James, never by an automatic update")

# --- links and banned text
low = raw.lower()
for word in BANNED_TEXT:
    if word in low:
        fail(f"banned text {word!r} found")
for url in sorted(set(re.findall(r"https?://[^\s\"\\<>)]+", raw))):
    host = re.sub(r"^www\.", "", re.sub(r"^https?://", "", url).split("/")[0].split(":")[0].lower())
    if not any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS):
        fail(f"link to a host that is not on the allowed list: {url}")
    if url.startswith("http://"):
        fail(f"link is not https: {url}")

# --- everything the app looks up by id exists
item_ids = {i["id"] for i in new.get("items", [])}
upgrade_ids = {u["id"] for u in new.get("upgrades", [])}
cat_ids = {c["id"] for c in new.get("cats", [])}
for x in new.get("upgrades", []) + new.get("recipes", []):
    for m in x.get("mats", []):
        if m.get("i") not in item_ids:
            fail(f"{x['id']}: unknown ingredient {m.get('i')!r}")
        if not isinstance(m.get("q"), int) or m["q"] <= 0:
            fail(f"{x['id']}: bad quantity for {m.get('i')!r}: {m.get('q')!r}")
for r in new.get("recipes", []):
    if r.get("cat") not in cat_ids:
        fail(f"{r['id']}: unknown category {r.get('cat')!r}")
    if r.get("unlock") not in ("level", "toggle") and r.get("unlock") not in upgrade_ids:
        fail(f"{r['id']}: unknown unlock {r.get('unlock')!r}")
    if r.get("unlock") == "level" and not isinstance(r.get("lvl"), int):
        fail(f"{r['id']}: level recipe without a level")
for line in new.get("lines", []):
    for t in line.get("tiers", []):
        if t not in upgrade_ids:
            fail(f"line {line['id']}: unknown tier {t!r}")
known = {x["id"] for k in ("weapons", "items", "recipes") for x in new.get(k, [])}
room_ids = [r["id"] for r in new.get("rooms", [])]
if len(room_ids) != len(set(room_ids)):
    fail("rooms: duplicate ids")
gone_rooms = sorted({r["id"] for r in old.get("rooms", [])} - set(room_ids))
if gone_rooms:
    fail(f"rooms: ids removed or renamed: {gone_rooms}")
for s in new.get("spots", []):
    for t in s.get("for", []):
        if t not in known:
            fail(f"spot at {s.get('place')!r}: unknown target {t!r}")
    if not re.fullmatch(r"20\d\d-\d\d-\d\d", str(s.get("date"))):
        fail(f"spot at {s.get('place')!r}: bad date {s.get('date')!r}")
for n in new.get("news", []):
    if n.get("ref") is not None and n["ref"] not in known and n["ref"] not in room_ids:
        fail(f"news {n.get('title')!r}: unknown ref {n.get('ref')!r}")

# --- report
print(f"rev {old['rev']} -> {new.get('rev')}   asOf {new.get('asOf')}   {len(raw):,} bytes")
print("counts:", ", ".join(f"{k} {len(new.get(k, []))}" for k in ID_LISTS + ("intel", "spots", "rooms", "news")))
for n in notes:
    print("note:", n)
if fails:
    for f in fails:
        print("FAIL", f)
    print(f"\n{len(fails)} problem(s). Do not push.")
    sys.exit(1)
print("OK: safe to publish.")
