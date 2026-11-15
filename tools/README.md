# How this data is updated

`kit.json` at the repo root is the file the Exfil Ledger app downloads. It is generated. Do not edit it by hand: edit the Python files here and rebuild.

| File | What lives in it |
|---|---|
| `data.py` | FOB upgrades and 3D Printer recipes: names, costs, how each unlocks |
| `build_data.py` | Guns (class, Gunsmith price, note), item hints (`FIND`), reserve defaults and recipe notes (`RESERVE`) |
| `build_app_data.py` | `REV`, `AS_OF`, the notice banner, and all Intel text (hot loot spots, Manual spots, recipes, ingredients, keys, X01, quick reference) |
| `spots.py` | Structured loot spots, key rooms and the What's new feed. Build 5 of the app reads these; builds 1 to 4 ignore them |
| `check.py` | Safety check that must pass before a push |

## Steps

1. Edit the data files.
2. In `build_app_data.py`, bump `REV` (today's date as yyyymmdd plus a two-digit counter, always higher than the published one) and set `AS_OF`.
3. `python3 tools/build_app_data.py` writes `kit.json`.
4. `python3 tools/check.py` must end with `OK: safe to publish.` If it prints any `FAIL`, fix your own edit or stop. Never edit `check.py` to make it pass.
5. Add one line to `CHECKLOG.md`, commit `kit.json`, the changed files in `tools/` and `CHECKLOG.md` together, and push to `main`.

Players get the new data the next time they open the app. GitHub can take about 5 minutes to serve it.

## Rules

- **Ids never change and are never removed.** Players' checkmarks are saved by id. New things get new ids. To rename something, change its name and keep its id (see `REC_ID` in `build_data.py`).
- **Intel sections `route` and `manuals` must stay.** The app opens them by id.
- **The map is off limits.** `MAP_URL` and `SAFE_MAP` are changed only by James.
- **Links only go to the hosts in `check.py`'s `ALLOWED_HOSTS`.** Never link to or use dmzcodex.com: in Oct 2026 it started redirecting visitors to scam pages. Adding a host to the list is James's call.
- **Only publish what a source says.** One-source claims are marked "one source" or "1 report". Loot is random, so report finds as places worth checking, not guarantees. No invented spots, prices or counts.
- **Keep Intel short.** Newest finds go at the top of the hot loot spots table with the date. Drop time-limited notes (events) once they have ended.
- **Plain wording.** The readers are two friends playing on an iPad.

## Log

`CHECKLOG.md` gets one line per check: the date, then either `no update needed` or `published rev <rev>: <what changed>`.
