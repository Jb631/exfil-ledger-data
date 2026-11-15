"""Builds the JSON data block for the DMZ Field Kit page from the same sources as the PDFs and xlsx."""
import json, re, sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

# ---- weapons (DMZ Codex Gunsmith guide, updated Oct 29/30; Manual reports from AllThingsHow, GamingProMax, Skycoach, GamerFuzion, DMZ Codex) ----
# (name, price, tag class, note, price unconfirmed, stable id)
W = lambda name, price=None, tag=None, note=None, approx=False, wid=None: (name, price, tag, note, approx, wid)
WEAPONS = [
    ("Assault Rifles", [W("Han 86", 6000, "default", "Reported starter"), W("M4", 6250, "seen", "One Manual report: Tool Chest, Prison Citadel yard. An M4 blueprint also unlocks it (BlackCell/Vault Edition, Valkyrie bundle)"),
                        W("Hyeon Burst", 5250), W("Kastov 762", 5500, "seen", "Manual: Irradiated Container (Reactor 02)"),
                        W("Patriot XMR", 6500, "seen", "Manual: Shopping DRC Locker (1 report)"), W("Oden"), W("Axion"), W("Cronen Squall", None, "seen", "Manual: Air Base DRC Weapons Locker (1 report)"),
                        W("Cronen Osprey", None, "seen", "Season 1: Battle Pass tier 16 (free) gives its Manual")]),
    ("SMGs", [W("ISO Nightshade", 3000, "seen", "Manual: Netshin Security Office (1 report)", True), W("PPSh-41", 3000, "seen", "Manual: Chang-san barracks during Iron Citadel", True),
              W("VEL 46", 3000, "seen", "Manual: Deadtown Re-Education Center locker (1 report)", True), W("Wz. 55 Striga", 3000, None, "Limited DMZ access (one source)", True),
              W("X-58 Nyx", 3000, approx=True),
              W("CSG-35", None, "seen", "Season 1: Battle Pass tier 36 (free) gives its Manual")]),
    ("Shotguns", [W("Rezi 12", 4000, "seen", "Manual: Netshin IT Room, Shopping DRC Locker"), W("Warlord", 3500, "seen", "Manual: Reactor DRC Locker (1 report)"),
                  W("JAK 12", None, None, "Season 1 event reward (event not named yet)")]),
    ("LMGs", [W("FiNN LMG", 8000, "seen", "Manual: Rail Depot Storage, Cheongun (1 report)"), W("Type 73", 7500, "seen", "Manual: Chang-san barracks, Cheonwang Peak Array"), W("APOC-338", 7750, "seen", "Manual: Shopping DRC Locker")]),
    ("Marksman Rifles", [W("MAR-9", 6500), W("Oris 8.6", 7000), W("Mosin-Nagant", 7500)]),
    ("Sniper Rifles", [W("Signal .50", 14000), W("KG-7 Vulcan", 16000, "seen", "Manual: X01 Audit Room safe (1 report)"), W("Astaroth .57", 24000)]),
    ("Pistols", [W("Sang 9mm", None, "seen", "Manual on the train · some list it as a starter"), W("Krait P68"), W(".50 GS", None, "seen", "Manual: Coin Mining Den (1 report)"), W("Mojave .357")]),
    ("Launchers", [W("RPG-8", None, "seen", "Manual: Iron Citadel armory (1 report)"), W("JOKR", None, "seen", "Manual: Irradiated Container"), W("PILA", None, "seen", "Manual seen (one source)"), W("PM-40 Anvil")]),
    ("Melee", [W("FSS Carbon Edge 1095", wid="w_combat_knife"),
               W("ZLR Talonhawk", None, None, "Season 1 event reward (event not named yet)")]),
]
weapons = []
for cls, rows in WEAPONS:
    for name, price, tag, note, approx, wid in rows:
        weapons.append({"id": wid or "w_" + slug(name), "name": name, "cls": cls, "price": price, "tag": tag,
                        "note": note, "approx": approx})

# ---- items ----
RESOURCES = ["Synthetics", "Electronics", "Chemicals", "Metals"]
VALUABLES = {"Infantry Invasion Plans", "Ballistic Flight Logs", "Regional Combat Notes",
             "Degraded Execution Footage", "Nuclear Program Files", "Encrypted Archive",
             "W.M.D Manifest", "Gold Skull", "Gold Bar", "Foreign Intelligence Targets",
             "Sanctioned Assassination List", "Cipher Code Ledger"}
OTHER = {"Irradiated Container", "Fulton Drop Marker", "Reactor DRC Locker", "Shopping DRC Locker",
         "Air Base DRC Weapons Locker", "Door Breacher Charge", "Specter Fabric Sample", "SR-16 Bio Agent Sample"}
FIND = {
    "Specter Fabric Sample": "Rare random loot inside X01; no fixed spot reported",
    "SR-16 Bio Agent Sample": "X01 Deep Vault 406, loose on the lab table",
    "Biomaterials": "Hospitals, chemical lockers",
    "Binding Catalyst": "Mirae General Hospital, medical tents; 2 at DMZ Level 49",
    "Control Units": "Computers, tech bags",
    "Electronic Sensors": "Tech bags, shops; grey IT bag in the Cheongun Village holding-cell building",
    "Reactive Metals": "Industrial areas, toolboxes; 2 at DMZ Level 11",
    "Rigid Synthetics": "2 at DMZ Level 6",
    "CPU": "Server rooms at Nenshin Tech and Cheonwang Peak Array; crashed large-drone Side Op panel",
    "Comms Module": "Server rooms at Nenshin Tech and Cheonwang Peak Array; crashed large-drone Side Op panel",
    "Power Regulator": "Server blades in the Cheonwang Peak Array server building (4th floor)",
    "Nylon Cloth": "Citadel wings, Deadtown underground holding, Mujin Nightclub",
    "High-Tenacity Fibers": "Colossus drops; blue duffel in a Hajin City barber shop",
    "Military Composites": "The Colossus only, and not every kill. Reliable spot: behind the armory door in the Chang-san bunker (Operation Iron Citadel)",
    "Prototype RF Module": "Deathstalker wreck, 6 of 6 in one count. Mostly over The Grid; one RPG-8 hit downs it",
    "Nano-Structured Alloy": "Destroyed Battle Tank only: Vehicle Hatch, Engine and Turret containers",
    "Experimental Compounds": "Sometimes from The Colossus, Deathstalker wrecks (2 of 6) and Battle Tanks (1 of 3)",
    "Regional Combat Notes": "Care packages, Compound Bravo safe, Special Delivery crate",
    "Infantry Invasion Plans": "Compound Charlie and Delta safes, Signal Breaker",
    "Gold Bar": "Silent Ledger reward; sells for 25,000",
    "Irradiated Container": "Decontaminate one at Reactor 02 to open it",
    "Reactor DRC Locker": "Key comes from Operation Fallen Ember",
    "Shopping DRC Locker": "Key turned up once in a Cheonwang Peak Array safe",
    "Air Base DRC Weapons Locker": "Locker is deep in the Chang-san bunker",
    "Synthetics": "Homes and gas stations",
    "Electronics": "Homes and gas stations",
    "Chemicals": "Homes, gas stations, clinics",
    "Metals": "Homes and gas stations",
}

CATS = [("healing", "Consumables", data.HEALING), ("armor", "Plate Carriers", data.ARMOR),
        ("packs", "Backpacks", data.BACKPACKS), ("tactical", "Tacticals", data.TACTICALS),
        ("lethal", "Lethals", data.LETHALS), ("field", "Field Upgrades", data.FIELD),
        ("fire", "Fire Support", data.FIRE), ("gear", "Gear", data.GEAR),
        ("ingr", "Ingredients", data.INGREDIENTS), ("x01", "X01 Printer", data.X01)]

RESERVE = {
    "3.5-Plate Armor Vest": (0, "X01 printer only; costs from one source"),
    "Survivor Box": (0, "X01 printer only. Sources disagree on the cost: another lists 1 SR-16 Bio Agent Sample, 3 Stabilized Reagents, 6 Nitro Compounds"),
    "Argonaut Armor": (0, "X01 printer only; costs from one source"),
    "Encodable Blank Keycard": (0, "X01 printer only; costs from one source"),
    "Staff Emergency Exfil Keycard": (0, "Recipe is the X01 Orders page 4 reward. Sources disagree on the cost: another lists 80 Electronics, 6 Printed Circuit Board, 10 Control Units"),
    "Consumable Box": (0, "Season 1. Recipe is the X01 Orders page 2 reward (one source)"),
    "Medical Box": (0, "Season 1. Recipe is the X01 Orders page 2 reward (one source)"),
    "Hazmat Box": (0, "Season 1. Recipe is the X01 Orders page 3 reward (one source)"),
    "Utility Box": (0, "Season 1. A found recipe; needs a Nano-Structured Alloy (one source)"),
    "Experimental Compounds": (0, "X01 printer only; also drops sometimes from The Colossus, Deathstalker wrecks and Battle Tanks"),
    "Military Composites": (0, "X01 printer only; also drops from The Colossus"),
    "Nano-Structured Alloy": (0, "X01 printer only; also from destroyed Battle Tanks"),
    "Prototype RF Module": (0, "X01 printer only; also drops from The Deathstalker"),
    "Medkit": (3, "Only heal that fixes a wound and resets the Tourniquet"),
    "Bandage": (2, "Cheap top-up heal"),
    "2-Plate Armor Vest": (2, "Replacement armor after a death"),
    "Medium Backpack": (2, "First pack with a Secure Slot"),
    "Gas Mask": (1, "Reactor and radiation runs"),
    "Armor Box": (1, "Squad replate"),
    "Self-Revive Kit": (1, "Second life; recipe at DMZ Level 48"),
    "3-Plate Armor Vest": (1, "Recipe from an Orders page"),
    "Radiation Blockers": (0, "Needed with Radiation Gear for the reactor"),
    "Disposable Parachute": (0, "3 uses each since Oct 23; recipe at DMZ Level 55"),
    "Small Secure Backpack": (0, "3 Secure Slots"),
    "Medium Secure Backpack": (0, "4 Secure Slots (one source)"),
    "Large Secure Backpack": (0, "4 Secure Slots"),
    "Recon Drone": (0, "Counterfeit Orders"),
    "DDOS": (0, "Underground Orders; also for the Tank"),
    "UAV": (0, "Recipe at DMZ Level 31"),
}

item_names = []
def add_item(n):
    if n != "cash" and n not in item_names:
        item_names.append(n)

for _, _, eff, reqs in data.UPGRADES:
    for it, q in reqs:
        add_item(it)
for _, _, lst in CATS:
    for _, _, _, reqs in lst:
        for it, q in reqs:
            add_item(it)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
         "XI": 11, "XII": 12, "XIII": 13}
NOTES = {
    "Dog Tag Case II": "Every source listing this copies Stash Item II's cost exactly, so it may be a copy error. Check the printer.",
    "MIA Recovery IV": "No cash cost, per one source.",
    "Vendor Items II": "No cash cost, per one source.",
}
for t in ("VIII", "IX", "X", "XI", "XII", "XIII"):
    NOTES["Bank " + t] = "One source (GG Ranked); not confirmed elsewhere yet."
REC_ID = {"Concussion Grenade": "r_stun_grenade", "Semtex": "r_semtex",
          # renamed Oct 30 to match the printer; ids kept so saved checkmarks carry over
          "1-Plate Armor Vest": "r_1_plate_vest", "2-Plate Armor Vest": "r_2_plate_vest",
          "2-Plate Helmet Armor Vest": "r_2_plate_helmet_vest", "3-Plate Armor Vest": "r_3_plate_vest",
          "3-Plate Helmet Armor Vest": "r_3_plate_helmet_vest", "Tempered Armor Vest": "r_tempered_vest",
          "Night Vision Goggles": "r_nvgs", "Parachute": "r_parachute_reusable"}
upgrades, lines = [], []
for name, tag, eff, reqs in data.UPGRADES:
    m = re.match(r"^(.*?)\s+([IVX]+)$", name)
    line, tier = (m.group(1), ROMAN[m.group(2)]) if m else (name, 1)
    cash = [q for it, q in reqs if it == "cash"]
    u = {"id": "u_" + slug(name), "name": name, "line": "l_" + slug(line), "tier": tier, "effect": eff,
         "cash": (cash[0] if cash else 0), "cashKnown": not (cash and cash[0] is None),
         "mats": [["i_" + slug(it), q] for it, q in reqs if it != "cash"]}
    if name in NOTES:
        u["note"] = NOTES[name]
    upgrades.append(u)
    if not any(l["id"] == u["line"] for l in lines):
        lines.append({"id": u["line"], "name": line, "tiers": []})
    next(l for l in lines if l["id"] == u["line"])["tiers"].append(u["id"])

recipes, printed_by = [], {}
for cid, cname, lst in CATS:
    for name, tag, eff, reqs in lst:
        r = {"id": REC_ID.get(name, "r_" + slug(name)), "name": name, "cat": cid, "tag": tag,
             "mats": [["i_" + slug(it), q] for it, q in reqs]}
        m = re.match(r"^Lvl (\d+)$", tag)
        if m:
            r["unlock"] = "level"; r["lvl"] = int(m.group(1))
        elif tag == "Uncommon Printing":
            r["unlock"] = "u_uncommon_ingredient_printing"
        elif tag == "Epic Printing":
            r["unlock"] = "u_epic_ingredient_printing"
        else:
            r["unlock"] = "toggle"
        if name in RESERVE:
            r["reserve"], r["why"] = RESERVE[name]
        printed_by["i_" + slug(name)] = r["id"]
        recipes.append(r)

items = []
for n in item_names:
    kind = "resource" if n in RESOURCES else "valuable" if n in VALUABLES else "other" if n in OTHER else "ingredient"
    iid = "i_" + slug(n)
    items.append({"id": iid, "name": n, "kind": kind, "step": 10 if kind == "resource" else 1,
                  "find": FIND.get(n), "print": printed_by.get(iid)})

ids = [x["id"] for x in weapons + items + upgrades + recipes]
assert len(ids) == len(set(ids)), "slug collision"
for u in upgrades:
    for i, q in u["mats"]:
        assert any(x["id"] == i for x in items), i

out = {"asOf": "Oct 30, 2026", "weapons": weapons, "items": items, "upgrades": upgrades,
       "lines": lines, "recipes": recipes, "cats": [[c, n] for c, n, _ in CATS]}
json.dump(out, open(sys.argv[1], "w"), separators=(",", ":"))
print("weapons", len(weapons), "items", len(items), "upgrades", len(upgrades), "lines", len(lines),
      "recipes", len(recipes), "reserve defaults", sum(1 for r in recipes if r.get("reserve")))
