# Crafting tracker data. Recipes: DMZ Codex recipe list (95 recipes, updated Oct 27, 2026; that site was
# later compromised and is no longer used or linked). Nov 15, 2026: every recipe and upgrade cost re-checked
# against COD Central's list (updated Nov 14); all matched except Survivor Box and Staff Emergency Exfil Keycard.
# FOB upgrades: DMZ Codex FOB Upgrade Tracker (Oct 27), Detonated (Oct 25), GamerFuzion (Oct 26).
# Oct 30 re-check: GG Ranked (Oct 25), DMZTracker (Oct 25), CODCentral (Oct 22). Seven "$?" tiers are materials-only;
# Bank VIII-XIII from GG Ranked only; Detonators recipe corrected (6 sources); Stun/Semtex renamed to official names.


def parse(spec):
    """'50 Synthetics, 5 Reactive Metals, $20000, $?' -> [(item, qty)]"""
    out = []
    for part in [p.strip() for p in spec.split(",") if p.strip()]:
        if part.startswith("$"):
            v = part[1:]
            out.append(("cash", None if v == "?" else int(v)))
        else:
            n, name = part.split(" ", 1)
            out.append((name, int(n)))
    return out


def card(name, tag, spec, effect=None):
    return (name, tag, effect, parse(spec))


UPGRADES = [
    card("Bank I", "", "$20000", "Cash cap 250,000"),
    card("Bank II", "", "$50000", "Cash cap 500,000"),
    card("Bank III", "", "$100000, 5 Infantry Invasion Plans", "Cash cap 1,000,000"),
    card("Bank IV", "", "$200000, 5 Ballistic Flight Logs, 5 Regional Combat Notes", "Cash cap 2,000,000"),
    card("Bank V", "", "$500000, 10 Degraded Execution Footage", "Cash cap 5,000,000"),
    card("Bank VI", "", "$500000, 10 Nuclear Program Files, 10 Encrypted Archive", "Cash cap 10,000,000"),
    card("Bank VII", "", "$500000, 10 W.M.D Manifest", "Cash cap 25,000,000"),
    card("Bank VIII", "", "$500000, 10 Foreign Intelligence Targets, 10 Cipher Code Ledger", "Cash cap 50,000,000"),
    card("Bank IX", "", "$500000, 10 Sanctioned Assassination List", "Cash cap 100,000,000"),
    card("Bank X", "", "$500000, 10 Gold Bar", "Cash cap 250,000,000"),
    card("Bank XI", "", "$500000, 10 Gold Skull", "Cash cap 500,000,000"),
    card("Bank XII", "", "20 Gold Bar, 20 Gold Skull, 3 Irradiated Container, 3 Fulton Drop Marker", "Cash cap 1,000,000,000"),
    card("Bank XIII", "", "1 Reactor DRC Locker, 1 Shopping DRC Locker, 1 Air Base DRC Weapons Locker, 5 Door Breacher Charge", "Cash cap 2,000,000,000"),
    card("Stash Item I", "", "$10000, 10 Rigid Synthetics, 10 Electronic Sensors", "+18 item slots"),
    card("Stash Item II", "", "$50000, 20 Detonators, 10 Nylon Cloth, 5 Power Regulator", "+18 item slots"),
    card("Stash Item III", "", "$100000, 20 Binding Catalyst, 20 Stock Rod, 10 Alloyed Plating", "+18 item slots"),
    card("Stash Item IV", "", "5 Gold Skull, 30 Alloyed Plating, 10 Experimental Compounds, 30 Turned Components", "+18 item slots"),
    card("Stash Weapon I", "", "$50000, 20 Reactive Metals, 10 Stock Rod, 5 Comms Module", "+6 weapon slots"),
    card("Stash Weapon II", "", "$100000, 20 Structural Alloy, 20 High-Tenacity Fibers, 10 Turned Components", "+6 weapon slots"),
    card("Stash Weapon III", "", "5 Gold Bar, 30 Stabilized Reagents, 30 Volatile Explosives, 10 Nano-Structured Alloy", "+6 weapon slots"),
    card("Gunsmith I", "", "$50000, 20 Reactive Metals, 10 CPU, 5 Power Regulator", "5% off Gunsmith"),
    card("Gunsmith II", "", "$100000, 20 Nitro Compounds, 10 Comms Module, 10 Military Composites", "5% off Gunsmith"),
    card("MIA Recovery I", "", "5 Regional Combat Notes, 10 Control Units, 10 Rigid Synthetics", "5% off MIA rescues"),
    card("MIA Recovery II", "", "5 Nuclear Program Files, 5 Degraded Execution Footage, 10 Binding Catalyst, 10 Nitro Compounds", "5% off MIA rescues"),
    card("MIA Recovery III", "", "5 W.M.D Manifest, 5 Foreign Intelligence Targets, 10 Power Regulator, 10 Comms Module", "5% off MIA rescues"),
    card("MIA Recovery IV", "", "5 Sanctioned Assassination List, 30 Ballistic Fabric, 30 Nylon Laminate, 10 Prototype RF Module", "5% off MIA rescues"),
    card("Dog Tag Case I", "", "$10000, 10 Rigid Synthetics, 10 Biomaterials", "+20 tag slots"),
    card("Dog Tag Case II", "", "$50000, 20 Detonators, 10 Nylon Cloth, 5 Power Regulator", "+20 tag slots"),
    card("Dog Tag Case III", "", "$100000, 10 Printed Circuit Board, 10 Structural Alloy, 5 Power Regulator", "More tag slots"),
    card("Dog Tag Case IV", "", "$200000, 20 CPU, 10 Stabilized Reagents, 5 Experimental Compounds", "More tag slots"),
    card("Vendor Items I", "", "20 Electronic Sensors, 10 CPU, 10 Printed Circuit Board, 2 Prototype RF Module", "More Vendor stock"),
    card("Vendor Items II", "", "20 Control Units, 10 High-Tenacity Fibers, 10 Nylon Cloth, 2 Nano-Structured Alloy", "More Vendor stock"),
    card("Uncommon Ingredient Printing", "", "$50000, 20 Biomaterials, 10 High-Tenacity Fibers, 5 Comms Module", "Print Uncommon ingredients"),
    card("Epic Ingredient Printing", "", "$100000, 10 Binding Catalyst, 10 Printed Circuit Board, 5 Military Composites", "Print Epic ingredients"),
]

HEALING = [  # in-game printer category: Consumables
    card("Bandage", "Lvl 2", "15 Synthetics, 15 Chemicals"),
    card("Medkit", "Lvl 2", "30 Chemicals, 1 Binding Catalyst, 5 Biomaterials"),
    card("Energy Drink", "Found", "10 Chemicals, 10 Metals"),
    card("Pain Killers", "Found", "15 Electronics, 15 Chemicals"),
    card("Sedative Inhaler", "Lvl 3", "15 Synthetics, 15 Chemicals"),
    card("Radiation Blockers", "Found", "30 Chemicals, 3 Biomaterials"),
    card("Smelling Salts", "Found", "30 Chemicals, 3 Detonators"),
    card("Self-Revive Kit", "Lvl 48", "1 Stabilized Reagents, 5 Biomaterials, 3 Binding Catalyst"),
    card("Door Breacher Charge", "Found", "1 Experimental Compounds, 5 Stock Rod, 3 Volatile Explosives"),
]

ARMOR = [  # in-game printer category: Plate Carriers
    card("1-Plate Armor Vest", "Lvl 2", "25 Synthetics, 25 Metals"),
    card("2-Plate Armor Vest", "Lvl 2", "50 Synthetics, 5 Reactive Metals"),
    card("2-Plate Ballistic Gel Vest", "Found", "50 Synthetics, 3 Binding Catalyst, 10 Reactive Metals"),
    card("2-Plate Helmet Armor Vest", "Found", "50 Synthetics, 3 Structural Alloy, 10 Reactive Metals"),
    card("3-Plate Armor Vest", "Orders", "2 Ballistic Fabric, 5 Nylon Cloth, 10 Reactive Metals"),
    card("3-Plate Ballistic Gel Vest", "Found", "2 Experimental Compounds, 4 Stabilized Reagents, 10 Biomaterials"),
    card("3-Plate Helmet Armor Vest", "Found", "2 Nano-Structured Alloy, 4 Alloyed Plating, 10 Reactive Metals"),
    card("Tempered Armor Vest", "Found", "2 Military Composites, 4 Ballistic Fabric, 10 Rigid Synthetics"),
]

BACKPACKS = [
    card("Small Backpack", "Lvl 2", "25 Synthetics, 25 Metals"),
    card("Medium Backpack", "Lvl 2", "50 Synthetics, 5 Rigid Synthetics"),
    card("Small Secure Backpack", "Found", "50 Metals, 3 Structural Alloy, 10 Rigid Synthetics"),
    card("Medium Scavenger Backpack", "Found", "50 Metals, 3 Nylon Cloth, 10 Rigid Synthetics"),
    card("Medium Weapon Backpack", "Found", "50 Synthetics, 3 High-Tenacity Fibers, 10 Rigid Synthetics"),
    card("Medium Secure Backpack", "Found", "2 Alloyed Plating, 5 Nylon Cloth, 10 Reactive Metals"),
    card("Large Backpack", "Orders", "2 Nylon Laminate, 5 Structural Alloy, 10 Rigid Synthetics"),
    card("Large Scavenger Backpack", "Found", "2 Nylon Laminate, 5 High-Tenacity Fibers, 10 Rigid Synthetics"),
    card("Large Secure Backpack", "Found", "2 Prototype RF Module, 4 Alloyed Plating, 10 Rigid Synthetics"),
    card("Secure Scavenger Backpack", "Found", "2 Military Composites, 4 Nylon Laminate, 10 Reactive Metals"),
]

GEAR = [
    card("Gas Mask", "Lvl 26", "30 Chemicals, 3 Rigid Synthetics"),
    card("Durable Gas Mask", "Found", "30 Chemicals, 1 High-Tenacity Fibers, 5 Biomaterials"),
    card("Weak Night Vision Goggles", "Found", "25 Metals, 5 Control Units"),
    card("Night Vision Goggles", "Orders", "50 Metals, 3 Printed Circuit Board, 10 Control Units"),
    card("Elite Night Vision Goggles", "Found", "2 Power Regulator, 3 CPU, 5 Electronic Sensors"),
    card("Disposable Parachute", "Lvl 55", "30 Chemicals, 3 Rigid Synthetics"),
    card("Parachute", "Found", "2 Turned Components, 5 Nylon Cloth, 10 Rigid Synthetics"),
]

TACTICALS = [
    card("Smoke Grenade", "Lvl 4", "10 Synthetics, 10 Chemicals"),
    card("Concussion Grenade", "Lvl 4", "10 Synthetics, 10 Chemicals"),
    card("Flash", "Orders", "10 Synthetics, 10 Chemicals"),
    card("Snapshot Grenade", "Lvl 9", "10 Synthetics, 10 Chemicals"),
    card("Decoy Grenade", "Orders", "10 Synthetics, 10 Chemicals"),
    card("Shock Stick", "Lvl 17", "10 Synthetics, 10 Chemicals"),
    card("Screamer Mine", "Found", "10 Synthetics, 10 Chemicals"),
    card("Stim", "Found", "15 Synthetics, 15 Chemicals"),
    card("Heartbeat Sensor", "Found", "25 Synthetics, 25 Chemicals"),
    card("Spotter Scope", "Lvl 12", "50 Synthetics, 5 Electronic Sensors"),
]

LETHALS = [
    card("Frag Grenade", "Lvl 7", "10 Chemicals, 10 Metals"),
    card("Throwing Knife", "Lvl 7", "25 Chemicals, 25 Metals"),
    card("Semtex", "Lvl 23", "10 Chemicals, 10 Metals"),
    card("Molotov Cocktail", "Lvl 36", "10 Chemicals, 10 Metals"),
    card("Thermite", "Lvl 41", "10 Chemicals, 10 Metals"),
    card("C4", "Orders", "10 Chemicals, 10 Metals"),
    card("Claymore", "Found", "10 Chemicals, 10 Metals"),
    card("Proximity Mine", "Found", "10 Chemicals, 10 Metals"),
    card("Zip Gun", "Found", "10 Chemicals, 10 Metals"),
    card("Drill Charge", "Found", "15 Chemicals, 15 Metals"),
    card("Trip Wire", "Found", "15 Chemicals, 15 Metals"),
]

FIELD = [
    card("Ammo Box", "Lvl 12", "15 Synthetics, 15 Metals"),
    card("Armor Box", "Lvl 14", "30 Metals, 3 Reactive Metals"),
    card("Recon Drone", "Orders", "30 Metals, 3 Electronic Sensors"),
    card("DDOS", "Orders", "30 Electronics, 3 Detonators"),
    card("Inflatable Decoy", "Lvl 52", "15 Synthetics, 15 Electronics"),
    card("Portable Radar", "Found", "15 Synthetics, 15 Electronics"),
    card("Seeker Drone", "Found", "15 Synthetics, 15 Electronics"),
    card("Smoke Wall", "Found", "15 Electronics, 15 Chemicals"),
    card("Riot Shield", "Found", "15 Synthetics, 15 Metals"),
    card("Rebreather", "Found", "15 Synthetics, 15 Chemicals"),
    card("Razor Wire Trap", "Found", "15 Electronics, 15 Metals"),
    card("Trophy System", "Found", "15 Electronics, 3 Control Units"),
    card("Defibrillator", "Critical Extraction", "30 Electronics, 3 Control Units"),
    card("SAM Airburst Turret", "Found", "30 Metals, 3 Detonators"),
    card("Revive Pistol", "Lvl 64", "2 Power Regulator, 3 Binding Catalyst, 5 Detonators"),
    card("Fulton Drop Marker", "Found", "1 Prototype RF Module, 3 Comms Module, 5 Control Units"),
    # Season 1 boxes (COD Central recipe list, updated Nov 14, 2026; one source)
    card("Consumable Box", "X01 Orders", "120 Synthetics, 2 High-Tenacity Fibers, 4 Biomaterials"),
    card("Medical Box", "X01 Orders", "100 Metals, 1 Stabilized Reagents, 4 Binding Catalyst"),
    card("Hazmat Box", "X01 Orders", "120 Synthetics, 1 Alloyed Plating, 4 Nylon Cloth"),
    card("Utility Box", "Found", "1 Nano-Structured Alloy, 2 Comms Module, 6 Printed Circuit Board"),
]

FIRE = [
    card("UAV", "Lvl 31", "30 Electronics, 2 Structural Alloy, 5 Electronic Sensors"),
    card("Advanced UAV", "Found", "2 Comms Module, 3 Nitro Compounds, 5 Electronic Sensors"),
    card("Care Package", "Lvl 28", "20 Electronics, 2 Control Units, 2 Rigid Synthetics"),
    card("Combat Drone", "Found", "30 Electronics, 2 CPU, 5 Control Units"),
    card("Crossfire", "Found", "2 Prototype RF Module, 3 Volatile Explosives, 5 Electronic Sensors"),
    card("Bomb Glider", "Found", "30 Chemicals, 2 Stock Rod, 5 Control Units"),
    card("Bombing Run", "Found", "30 Chemicals, 2 Nitro Compounds, 5 Control Units"),
    card("Artillery Beacon", "Found", "2 Volatile Explosives, 3 Nitro Compounds, 5 Detonators"),
    card("Railgun Sentry", "Found", "2 Power Regulator, 3 Nitro Compounds, 5 Control Units"),
    card("Impact Warhead", "Found", "2 Turned Components, 3 Nitro Compounds, 5 Detonators"),
]

INGREDIENTS = [
    card("Reactive Metals", "Uncommon Printing", "20 Chemicals, 20 Metals"),
    card("Rigid Synthetics", "Uncommon Printing", "20 Synthetics, 20 Metals"),
    card("Biomaterials", "Uncommon Printing", "20 Synthetics, 20 Chemicals"),
    card("Control Units", "Uncommon Printing", "20 Electronics, 20 Metals"),
    card("Electronic Sensors", "Uncommon Printing", "20 Synthetics, 20 Electronics"),
    card("Detonators", "Uncommon Printing", "20 Electronics, 20 Chemicals"),
    card("Alloyed Plating", "Epic Printing", "100 Metals, 3 Structural Alloy"),
    card("Ballistic Fabric", "Epic Printing", "100 Synthetics, 3 High-Tenacity Fibers"),
    card("Comms Module", "Epic Printing", "100 Electronics, 3 CPU"),
    card("Nylon Laminate", "Epic Printing", "100 Synthetics, 3 Nylon Cloth"),
    card("Power Regulator", "Epic Printing", "100 Electronics, 3 Printed Circuit Board"),
    card("Stabilized Reagents", "Epic Printing", "100 Chemicals, 3 Binding Catalyst"),
    card("Turned Components", "Epic Printing", "100 Metals, 3 Stock Rod"),
    card("Volatile Explosives", "Epic Printing", "100 Chemicals, 3 Nitro Compounds"),
]

BLANK = ("", "", None, [("", 0)] * 4)

SECTIONS = [
    ("FOB UPGRADES", UPGRADES),
    ("HEALING AND CONSUMABLES", HEALING),
    ("ARMOR", ARMOR),
    ("BACKPACKS", BACKPACKS),
    ("GEAR", GEAR),
    ("TACTICALS", TACTICALS),
    ("LETHALS AND TRAPS", LETHALS),
    ("FIELD EQUIPMENT", FIELD),
    ("FIRE SUPPORT", FIRE),
    ("INGREDIENT PRINTING", INGREDIENTS),
    ("NEW RECIPES YOU FIND (WRITE IN)", [BLANK] * 4),
]

if __name__ == "__main__":
    total = sum(len(c) for t, c in SECTIONS if not t.startswith("NEW"))
    print("cards", total, "upgrades", len(UPGRADES), "recipes", total - len(UPGRADES))

X01 = [  # Season 1: X01 black-site printer only (one source, Nov 7, 2026)
    card("3.5-Plate Armor Vest", "X01 Printer", "1 Specter Fabric Sample, 2 Power Regulator, 5 Structural Alloy"),
    card("Survivor Box", "X01 Printer", "1 SR-16 Bio Agent Sample, 2 Ballistic Fabric, 3 High-Tenacity Fibers"),
    card("Argonaut Armor", "X01 Printer", "1 Specter Fabric Sample, 2 Alloyed Plating, 5 High-Tenacity Fibers"),
    card("Encodable Blank Keycard", "X01 Printer", "6 Printed Circuit Board, 8 Control Units"),
    card("Staff Emergency Exfil Keycard", "X01 Printer", "2 CPU, 4 Printed Circuit Board, 8 Control Units"),
    # Legendary ingredients, X01 printer only (Game Rant + MMOexp, checked Nov 10, 2026)
    card("Experimental Compounds", "X01 Printer", "2 Volatile Explosives, 5 Binding Catalyst"),
    card("Military Composites", "X01 Printer", "2 Nylon Laminate, 5 Nylon Cloth"),
    card("Nano-Structured Alloy", "X01 Printer", "2 Turned Components, 5 Structural Alloy"),
    card("Prototype RF Module", "X01 Printer", "2 Power Regulator, 5 CPU"),
]
