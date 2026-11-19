"""Builds kit.json for the Exfil Ledger app.

Run from anywhere:  python3 tools/build_app_data.py
In the data repo (github.com/Jb631/exfil-ledger-data) it writes kit.json at the repo root, which is the
file the app downloads. Inside the app's Xcode project it writes ExfilLedger/kit.json and data/kit.json.
Then run:  python3 tools/check.py   (must pass before anything is pushed)
Before running: bump REV (yyyymmdd + 2-digit counter, must go up every time) and AS_OF below.
Edit game data in data.py (upgrades, recipes) and build_data.py (guns, item hints, reserve defaults);
Intel text lives further down in this file.
The app ships this file in its bundle and also downloads the newest copy from GitHub,
so this script is also what produces each data update.
"""
import json, subprocess, sys

import os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = 1
REV = 2026111901          # yyyymmdd + 2-digit counter; bump on every data update
AS_OF = "Nov 19, 2026"

TMP = os.path.join(tempfile.gettempdir(), "exfil_ledger_src.json")
subprocess.run([sys.executable, os.path.join(HERE, "build_data.py"), TMP], check=True)
src = json.load(open(TMP))

mats = lambda pairs: [{"i": i, "q": q} for i, q in pairs]

weapons = [{"id": w["id"], "name": w["name"], "cls": w["cls"], "price": w["price"], "tag": w["tag"],
            "note": w["note"], "approx": bool(w.get("approx"))} for w in src["weapons"]]
items = [{"id": i["id"], "name": i["name"], "kind": i["kind"], "find": i["find"], "print": i["print"]} for i in src["items"]]
upgrades = [{"id": u["id"], "name": u["name"], "line": u["line"], "tier": u["tier"], "effect": u["effect"],
             "cash": u["cash"] or 0, "cashKnown": u["cashKnown"], "mats": mats(u["mats"]), "note": u.get("note")}
            for u in src["upgrades"]]
recipes = [{"id": r["id"], "name": r["name"], "cat": r["cat"], "tag": r["tag"], "unlock": r["unlock"],
            "lvl": r.get("lvl"), "mats": mats(r["mats"]), "reserve": r.get("reserve") or 0, "why": r.get("why")}
           for r in src["recipes"]]
cats = [{"id": c, "name": n} for c, n in src["cats"]]

P = lambda t: {"type": "p", "text": t}
NOTE = lambda t: {"type": "note", "text": t}
TABLE = lambda h, rows: {"type": "table", "headers": h, "rows": rows}
STEPS = lambda xs: {"type": "steps", "items": xs}
KV = lambda rows: {"type": "kv", "rows": rows}
LINKS = lambda *ls: {"type": "links", "links": [{"title": t, "url": u} for t, u in ls]}

ingr = sorted([i for i in src["items"] if i["find"] and i["kind"] not in ("resource",)], key=lambda i: i["name"])

intel = [
    {"id": "route", "title": "Hot loot spots", "subtitle": "Newest reported finds · " + AS_OF, "blocks": [
        P("The best recent finds players have reported. Loot is random every match and most of these are from one run, so treat them as places worth checking, not guarantees."),
        NOTE("**Lieutenant dog tag cash now goes to every squad member (Nov 16 patch).** Guides list a tag at 25,000 on extract; the patch notes give no amount, so check your extraction summary. **Events:** Resupply Run is listed as ending Nov 19. War Chest is listed as starting Nov 19: opening a container scores 5 points and a safe 50, on a leaderboard that resets every three hours (one source). Wager Match is listed as running to Dec 2."),
        TABLE(["Spot", "Threat", "What's been found"], [
            ["Deathstalker wreck. It flies mostly over The Grid (G6), and a new one arrives 7 to 8 minutes after a kill", "Varies", "Prototype RF Module in 6 of 6 wrecks, Experimental Compounds in 2 of 6. One RPG-8 hit brings it down; its three containers can scatter when it falls · Nov 15"],
            ["Militia Arms Depot, Compound Echo apartment block B (G7), one flight up inside the Gangbyeon Apartment B door (both keys are random loot)", "Medium", "Binding Catalyst, Nuclear Program Files, 2 Degraded Execution Footage, 5 more intel items; about 14,000 · Nov 14"],
            ["The Chemist's Secure Armory, Haneul Reactor I4, a bunker on the northeast side just inside the radiation (key drops from The Chemist, not every kill)", "Not rated", "About 32,000: W.M.D Manifest (5,000), Legendary Chemical Reaction (5,900), Ballistic Fabric, Nuclear Program Files, 2 Durable Gas Masks · Nov 11"],
            ["The Doctor's Command Office, Mirae Hospital floor 7, rooms 704 and 705 (key drops from The Doctor, not every kill)", "Low", "About 28,000 on a second run: Legendary Doctor's Salve rifle (6,900), Volatile Explosives, High-Tenacity Fibers, Encrypted Archive. No recipe that time · Nov 11"],
            ["X01 Superintendent's Office, upper level of the Main Warehouse (keycard is random loot)", "X01", "About 60,000 in one opening: Weapons Grade Isotope (12,000), 2 Human Trial Records (8,000 each), a Legendary MAR-9, Zip Gun recipe · Nov 9"],
            ["X01 Lt. Chol-Min's Stash Room, above his hall in the Motor Pool (key drops from Chol-Min; climb the rope in the cage in his room)", "X01", "Medium Scavenger Backpack recipe, Legendary Swaegolja LMG (8,000), Cipher Code Ledger, Combat Drone; about 29,000 · Nov 9"],
            ["Haejeok Radio Station, Imjin Farmland D6, upstairs in the white building under the red mast (key is random loot)", "Not rated", "Best electronics room so far: 2 Comms Modules, Power Regulator, 5 CPUs, 10 Electronic Sensors, 6 Control Units, plus a safe of intel; about 25,000 · Nov 9"],
            ["Hospital Chemical Lockers, Mirae Hospital basement lab (lab key on floor 7; locker keys in the morgue and on a lab bench, one per locker)", "Low", "2-Plate Helmet Armor Vest recipe, Binding Catalyst, 7 Detonators · Nov 8"],
            ["Weapons Mod Workshop, Chang-san Air Base B5, upstairs in the repair garage (key is random loot)", "Extreme", "Small Secure Backpack recipe, Cipher Code Ledger, 2-Plate Helmet Armor Vest · Nov 10"],
            ["X01 Audit Room safe (Main Warehouse top floor). Keycard from a jacket or Industrial Locker in the Supply Depot", "X01", "KG-7 Vulcan Manual, Gilded Medal of Absolute Loyalty (15,000), Gilded Maritime Relic (7,000) · Nov 7"],
            ["X01 Deep Vault Room 406. Keycard was on the X01 Executive Room desk 3 runs out of 3", "Critical", "SR-16 Bio Agent Sample loose on the lab table; 4 safes worth about 29,000 (R-4 Bio-Compounds, Animal Trial Records, Encrypted Archive) · Nov 7"],
            ["X01 Small Test Chamber safe (Tech Lab)", "X01", "Gold Bar, 2 Gilded Maritime Relics; Encrypted Archive loose · Nov 7"],
            ["Shopping DRC Locker under NuriGO Mall (key is random loot)", "Medium–High", "Patriot XMR and Rezi 12 Manuals in one opening, plus a Large Secure Backpack (15,000) · Nov 5"],
            ["Netshin Tech Complex floor 14, IT Room (key)", "Extreme", "Rezi 12 Manual, Power Regulator, Volatile Explosives, 5 intel items · Nov 5"],
            ["Netshin Tech Complex upper floor, Security Office rifle case (key)", "Extreme", "ISO Nightshade Manual · Nov 5"],
            ["Reactor DRC Locker, underwater in the Reactor 02 pool (key from Operation Fallen Ember)", "High", "Warlord Manual, 3-Plate Ballistic Gel Vest, Large Secure Backpack · Nov 5"],
            ["Air Base DRC Weapons Locker, Chang-san bunker armory (key is random loot)", "Extreme", "A Cronen Squall Manual (reported as \"Cronin\"), 3-Plate Helmet Armor Vest · Nov 5"],
            ["Prison Citadel yard, Tool Chest", "Critical", "M4 Manual, the only one reported · Nov 3–6"],
            ["Battle Tank. It drives loops: north and south of NuriGO Mall, Construction Zone, between City Hall and DBN Headquarters, NuriGO West, Rice Mill, Songdo Wharf, Heavenly Luck Casino", "Varies", "The only source of Nano-Structured Alloy. Check all three containers on the wreck: Vehicle Hatch, Engine and Turret. One Impact Warhead destroys it; a JOKR takes 6 to 9 hits · Nov 12"],
        ]),
        P("**Best containers for Manuals** (one guide's counts): Irradiated Container 16 out of 16, Elite Weapons Locker 3 out of 5, ordinary Weapons Locker about 1 in 22, Safe about 1 in 57, Filing Cabinet about 1 in 64."),
        NOTE("Found something good? Tell James where and what, and it goes in here for the whole squad."),
        LINKS(("COD Central loot counts", "https://codcentral.net/blog/mw4-dmz-loot-data/"),
              ("DMZ Map best loot", "https://dmzmap.com/guides/best-loot")),
    ]},
    {"id": "manuals", "title": "Weapon Manual spots", "subtitle": "By gun · " + AS_OF, "blocks": [
        P("In loot they show up named **MANUAL:** plus the gun. Only the player who extracts it gets the unlock, but you can hand one to a squadmate before exfil. Put it in a Secure Slot the moment you grab it."),
        TABLE(["Gun", "Where it's been found", "Threat"], [
            ["M4", "Tool Chest in the Prison Citadel yard (1 report)", "Critical"],
            ["Patriot XMR", "Shopping DRC Locker under NuriGO Mall (1 report)", "Medium–High"],
            ["Rezi 12", "Netshin floor 14 IT Room weapons locker; Shopping DRC Locker", "Extreme / Medium–High"],
            ["ISO Nightshade", "Netshin Security Office rifle case (1 report)", "Extreme"],
            ["Warlord", "Reactor DRC Locker in the Reactor 02 pool (1 report)", "High"],
            ["Cronen Squall", "Air Base DRC Weapons Locker, Chang-san bunker (1 report, written as \"Cronin\")", "Extreme"],
            ["KG-7 Vulcan", "X01 Audit Room safe (1 report)", "X01"],
            [".50 GS", "Footlocker upstairs in the Coin Mining Den, NuriGO West; key from Operation Shopping Hacks (1 report)", "Not rated"],
            ["FiNN LMG", "Rail Depot Storage, Cheongun Village station basement (1 report)", "Low"],
            ["VEL 46", "Military Locker, Deadtown Re-Education Center (1 report)", "Not rated"],
            ["Type 73", "Blue duffel in the Chang-san barracks during Iron Citadel; filing cabinet at Cheonwang Peak Array", "Critical / Medium"],
            ["PPSh-41", "Duffel in the Chang-san barracks during Iron Citadel; Vault Armory weapons locker under the Casino (one player called it a blueprint)", "Critical / High"],
            ["APOC-338", "Shopping DRC Locker under NuriGO Mall", "Medium–High"],
            ["Kastov 762", "Irradiated Container (decontaminate it at Reactor 02)", "High"],
            ["JOKR", "Irradiated Container", "High"],
            ["RPG-8", "Weapons Locker in the Iron Citadel armory, Chang-san bunker (1 report)", "Extreme"],
            ["Sang 9mm", "Blue duffel on a seat of the train through Cheongun Outskirts (1 report)", "Not rated"],
        ]),
        P("**Best farm so far:** launch Operation Iron Citadel, loot the Chang-san Air Base barracks and the three houses there, then leave without finishing it. One guide got Manuals almost every run."),
        P("**Season 1 guns:** unlocking one on the Battle Pass gives you its Manual: Cronen Osprey (assault rifle) at tier 16, CSG-35 (SMG) at tier 36, both free. Owning a blueprint from BlackCell, a store bundle or the Vault Edition also unlocks the base gun, which is how the M4 comes with BlackCell (Perimeter Lance)."),
        P("Nothing new since Nov 10: the boss and key-room write-ups from Nov 10 to 15 list guns as loot but no Manuals."),
        NOTE("No spot reported yet for: Han 86, Hyeon Burst, Oden, Axion, X-58 Nyx, Oris 8.6, Mosin-Nagant, Signal .50, Astaroth .57, Krait P68, Mojave .357."),
        LINKS(("COD Central, Weapon Manuals", "https://codcentral.net/blog/mw4-dmz-weapon-manuals/"),
              ("COD Central, Irradiated Container", "https://codcentral.net/blog/mw4-dmz-irradiated-container/")),
    ]},
    {"id": "recipes", "title": "Recipe drop spots", "subtitle": "Where printer recipes have turned up", "blocks": [
        TABLE(["Recipe", "Where it's been found", "Threat"], [
            ["Zip Gun", "Blue duffel in the Chang-san barracks (Iron Citadel); Counting Room Vault weapons locker in the Casino; upstairs cache at the Cheongun Village fire station; X01 Superintendent's Office weapons locker", "Critical / High / Low / X01"],
            ["Medium Scavenger Backpack", "LT Crate in Lt. Chol-Min's Stash Room, X01 Motor Pool (1 report)", "X01"],
            ["Small Secure Backpack", "Weapons Mod Workshop, Chang-san Air Base repair garage (1 report)", "Extreme"],
            ["Combat Drone", "Green footlocker in the Chang-san barracks (Iron Citadel)", "Critical"],
            ["Pain Killers, Energy Drink, Drill Charge", "Mirrored medicine cabinets over the sinks in the Chang-san barracks washroom", "Critical"],
            ["Screamer Mine", "Lucera Suite 703 bedroom weapons locker (Hotel Lucera); Hanwoori Art Records Room in The Grid", "Critical"],
            ["Stim", "Hanwoori Art Records Room in The Grid", "Critical"],
            ["Impact Warhead", "Cache in the Hoesik Supply Room by the Rice Mill (key)", "Medium"],
            ["Smelling Salts", "Chemical Storage in the Reactor 02 Control Room", "High"],
            ["Tempered Armor Vest", "The Doctor's crate in his Command Office, Mirae Hospital floor 7 (key drops from The Doctor). A second run on Nov 11 had no recipe", "Low"],
            ["2-Plate Ballistic Gel Vest", "Grey filing cabinet in a small Casino office", "High"],
            ["2-Plate Helmet Armor Vest", "Roof crates by the SAM site at Compound Echo; Hospital Chemical Lockers in the Mirae Hospital basement", "Medium / Low"],
            ["Large Scavenger Backpack", "First aid kit on a pillar in the fire station garage, North Korean Wilderness", "Not rated"],
            ["Advanced UAV", "Armory locker in the Iron Citadel bunker", "Extreme"],
        ]),
        P("**New in the printer list (Season 1):** Consumable Box and Medical Box recipes are the X01 Orders page 2 reward, Hazmat Box is page 3, and Utility Box is a found recipe. All four are in Crafting under Field Upgrades. One source."),
        P("**By container** (no spot given): Trophy System in filing cabinets and tool chests; Claymore in tool boxes and safes; Heartbeat Sensor in duffels and tool boxes; Stim in safes, caches and luggage; 2-Plate Helmet Armor Vest came from a safe 6 times out of 7."),
        LINKS(("COD Central recipes", "https://codcentral.net/blog/mw4-dmz-3d-printer-recipes/"),
              ("All Things How, barracks loot", "https://allthings.how/?p=297369")),
    ]},
    {"id": "ingredients", "title": "Rare ingredients and Bank intel", "subtitle": "Farm spots for the hard ones", "blocks": [
        TABLE(["Legendary ingredient", "Drops from"], [["Military Composites", "The Colossus only, and not every kill. He roams, but he's reliably behind the armory door in the Chang-san bunker during Operation Iron Citadel"],
            ["Prototype RF Module", "Deathstalker wreck: 6 of 6 in one count. Mostly over The Grid; one RPG-8 hit downs it"],
            ["Nano-Structured Alloy", "Destroyed Battle Tank only: Vehicle Hatch, Engine and Turret containers"],
            ["Experimental Compounds", "Sometimes from The Colossus, Deathstalker wrecks (2 of 6) and Battle Tanks (1 of 3)"]]),
        P("Each legendary ingredient sells for 3,500. A bug that paid materials instead of cash was fixed Nov 13."),
        P("**Or print them in X01.** The X01 3D Printer (Production Assembly, grid E5; one guide puts it in the small office off the west mezzanine) makes all four, and they are now in Crafting under X01 Printer: Experimental Compounds 2 Volatile Explosives + 5 Binding Catalyst · Military Composites 2 Nylon Laminate + 5 Nylon Cloth · Nano-Structured Alloy 2 Turned Components + 5 Structural Alloy · Prototype RF Module 2 Power Regulator + 5 CPU."),
        TABLE(["Ingredient", "Reported spots"], [
            ["Power Regulator", "Netshin IT Room, Hanex Guard Station (loose), Hanwoori Art Records Room, Cheonwang Peak Array server racks, Haejeok Radio Station, Battle Tank wrecks"],
            ["Turned Components", "Industrial lockers in the North Korean Wilderness; Police Weapon Depository at Wolves Stadium; hidden cache in the Construction Zone during Special Delivery; Gas Station Electrical Room under the Korin Oil station (H7)"],
            ["Alloyed Plating", "Bubun Yard tool chest; Commandant Office weapons locker; Vault Armory; X01 Maintenance Room"],
            ["Stabilized Reagents", "Vault Armory under the Casino"],
            ["Volatile Explosives", "Hidden cache on Oamsik Turtle Island; Netshin IT Room; The Doctor's Command Office"],
            ["Ballistic Fabric", "Shop Records Room; X01 Executive Room; Irradiated Containers; Cheongun Village police armory; The Chemist's Secure Armory"],
            ["Binding Catalyst", "Hazard Storehouse at the Haneul Reactor (2); unlocked cache by the Mirae Hospital Chemical Lab door; Militia Arms Depot"],
            ["High-Tenacity Fibers", "X01 Superintendent's Office (2); Chang-san Air Base Armory and Barracks; The Doctor's Command Office"],
            ["Structural Alloy", "Haksan School Armory; Bale's backpack (Deadtown Re-Education Center top floor, or the Chang-san bunker)"],
            ["Nylon Laminate", "Commandant Office military locker; Hoesik Supply Room shelf by the door; Battle Tank wrecks"],
            ["Comms Module", "Haejeok Radio Station (2); Police Weapon Depository server blade; Gangbyeon Apartment B; X01 Maintenance Room"],
        ]),
        P("**Gold Bars and Gold Skulls come from safes.** All 42 in one count did. Best odds: Compound Alpha (7 from 33 safes), Wolves Stadium (about 1 in 8). Safe run: Compounds Echo, Bravo, Alpha, Charlie, Foxtrot. Guaranteed ones: first clear of Operation Silent Ledger gives 1 Gold Bar, Orders page 24 gives 2."),
        TABLE(["Bank intel item", "Where to look"], [
            ["Sanctioned Assassination List", "South Block Armory in the Citadel; the western bunkers; Military Lockers; Roze's backpack (DBN Headquarters roof)"],
            ["Foreign Intelligence Targets", "Mirae Hospital Electrical Room (B2) server blade; Gaming Computers (about 1 in 18)"],
            ["W.M.D Manifest", "Gangbyeon Apartment B (2 at once); Executive Arms Auction in DBN HQ; the western bunkers; Irradiated Containers; The Chemist's Secure Armory"],
            ["Nuclear Program Files", "Vault Armory; Utility Maintenance Storage; Reactor 02 Control Room computer; Coin Mining Den; both DRC Lockers; Militia Arms Depot; The Chemist's Secure Armory"],
            ["Encrypted Archive", "X01 Deep Vault 406 and Small Test Chamber; Counting Room Vault; Air Base DRC Locker"],
            ["Degraded Execution Footage", "Gangbyeon Apartment B (3), Hoesik Supply Room (2), Mirae Electrical Room (2)"],
            ["Regional Combat Notes", "Compound Delta (about 1 in 5); Hanex Bank and Cheonwang Peak Array (about 1 in 8); Hanex Guard Station"],
            ["Infantry Invasion Plans, Ballistic Flight Logs", "Almost every key room; Bank Branch Vault gave 2 of each"],
        ]),
        P("After Uncommon Ingredient Printing, Reactive Metals, Rigid Synthetics, Biomaterials, Control Units, Electronic Sensors and Detonators each print from 20 + 20 basic resources."),
        LINKS(("COD Central ingredients", "https://codcentral.net/blog/mw4-dmz-ingredient-locations/"),
              ("COD Central gold", "https://codcentral.net/blog/mw4-dmz-gold-bar-gold-skull/"),
              ("Game Rant, X01 legendary printing", "https://gamerant.com/mw4-dmz-legendary-materials-x01-3d-printer-location/")),
    ]},
    {"id": "keys", "title": "Keys, vaults and safes", "subtitle": "Worth running, and what was inside", "blocks": [
        TABLE(["Key", "Where the key comes from", "What's been inside", "Threat"], [
            ["Shopping DRC Locker", "Random loot (one came from a Cheonwang Peak Array safe)", "APOC-338, Patriot XMR, Rezi 12 Manuals; Large Secure Backpack", "Medium–High"],
            ["Reactor DRC Locker", "Operation Fallen Ember reward", "Warlord Manual, 3-Plate Ballistic Gel Vest, Large Secure Backpack", "High"],
            ["Air Base DRC Weapons Locker", "Random loot (one in a duffel at Imjin Farmland)", "Cronen Squall Manual, 3-Plate Helmet Armor Vest", "Extreme"],
            ["Netshin IT Room", "Apartment lockers or random loot", "Rezi 12 Manual, Power Regulator, Volatile Explosives, 5 intel items", "Extreme"],
            ["Counting Room Vault", "Operation Silent Ledger; industrial locker on the Rice Mill catwalk; Haksan School armory", "Zip Gun recipe, Gold Skull", "High"],
            ["Vault Armory", "Casino carpet, Songdo Wharf duffel, Irradiated Container, Prison Encampment Storage", "Cipher Code Ledger, Stabilized Reagents, Alloyed Plating, Nuclear Program Files", "High"],
            ["South Block Armory", "Counter in the Citadel Main Control Room (needs its own key)", "Gold Skull, Sanctioned Assassination List, a recipe", "Critical"],
            ["Bank Branch Vault Access", "Teller counter at the Wolves branch, or the floor behind the teller windows in Cheongun", "Cipher Code Ledger, 8 intel items, once a Gold Skull", "Medium"],
            ["Gangbyeon Apartment B", "Bookshelf or desk in a Compound Echo apartment", "2 W.M.D Manifests, Comms Module, Prison Encampment key", "Medium"],
            ["Hanex Guard Station", "Random loot", "Power Regulator, Cipher Code Ledger, a Legendary Warlord", "Extreme"],
            ["Coin Mining Den", "Operation Shopping Hacks reward", ".50 GS Manual, 6 CPUs, Nuclear Program Files", "Not rated"],
            ["The Doctor's Command Office", "The Doctor (not every kill)", "Tempered Armor Vest recipe on one run; about 28,000 and no recipe on another (Volatile Explosives, High-Tenacity Fibers, a Legendary rifle)", "Low"],
            ["The Chemist's Secure Armory", "The Chemist, in the Haneul Reactor radiation zone (not every kill); one turned up in The Scavenger's backpack", "W.M.D Manifest, Ballistic Fabric, Nuclear Program Files, 2 Durable Gas Masks; about 32,000", "Not rated"],
            ["Militia Arms Depot", "Random loot. The front door also needs the Gangbyeon Apartment B key", "Binding Catalyst, Nuclear Program Files, 2 Degraded Execution Footage; about 14,000", "Medium"],
            ["Roze's Highrise Armory", "Roze, on the DBN Headquarters roof (not every kill); also the Operation Grid Assault reward", "Netshin floor 14: a Lieutenant crate and two weapon lockers. One visit had the Legendary Kraken sniper", "Extreme"],
            ["Supreme Leader's Bunker Access Card", "Bale (not every kill); also the Operation Iron Citadel reward", "A bunker deep under Chang-san Air Base. Contents not reported", "Extreme"],
            ["Kang's Arms Incinerator", "The Warden (Kang) at the prison. It hasn't dropped in one guide's kills", "A room in the prison's central block. Contents not reported", "Critical"],
            ["Gorani's Scout Overlook", "Lieutenant Gorani at Mujin Pass", "Legendary \"Incisor\" rifle, UAV", "Not rated"],
            ["Old Barber Shop", "Random loot", "Cipher Code Ledger, Legendary Revive Pistol, Commandant Office key", "Low"],
            ["X01 Superintendent's Office", "Random loot", "Weapons Grade Isotope, 2 Human Trial Records, Legendary MAR-9, Zip Gun recipe; about 60,000", "X01"],
            ["X01 Lt. Chol-Min's Stash Room", "Lt. Chol-Min", "Medium Scavenger Backpack recipe, Legendary Swaegolja, Cipher Code Ledger, Haksan School Armory key", "X01"],
            ["Haejeok Radio Station", "Random loot", "2 Comms Modules, Power Regulator, 5 CPUs, safe with 7 intel items; about 25,000", "Not rated"],
            ["Hospital Chemical Lab and Lockers", "Lab key: floor 7 office desk or shelves. Locker keys: morgue table, lab bench", "2-Plate Helmet Armor Vest recipe, Binding Catalyst, 2 Medkits", "Low"],
            ["Weapons Mod Workshop", "Random loot", "Small Secure Backpack recipe, Cipher Code Ledger; about 17,000", "Extreme"],
            ["Police Station Armory", "Inside each police station, usually on an office desk or table", "Ballistic Fabric, CPUs, a KG-7 Vulcan; 2,600 to 5,100 a station", "Low–Medium"],
            ["Field Depot", "Random loot (one from a Wilderness bunk duffel)", "Legendary Parachute, Hazard Storehouse key; about 8,500", "Extreme"],
            ["Skip unless you're passing", "Haksan School Armory, Imjin Mill Foreman's Office, Gas Station Electrical Room, Hazard Storehouse, Mechanic's Shack, Downtown Branch Lobby Main", "3,000 to 10,000 each, no recipes or Manuals. The Downtown Branch Lobby did hold a Vault Armory key", "Low–Critical"],
        ]),
        P("Also: the Mechanic's Shack key has turned up in a green military locker on the train, and the Hazard Storehouse key on an enemy operator at the Cheongun Outskirts gas station and in a Field Depot military locker."),
        P("**The Scavenger** drives an LTV loop with his men (River Heights G7 to G8, Expressway No. 1 H5, Tong-il Village D3, Deadtown B7). His backpack can hold other Lieutenants' keys."),
        LINKS(("DMZ Map keys", "https://dmzmap.com/keys/shopping-drc-locker"),
              ("COD Central keys", "https://codcentral.net/blog/mw4-dmz-netshin-it-room-key/"),
              ("COD Central, The Chemist's Secure Armory", "https://codcentral.net/blog/mw4-dmz-the-chemists-secure-armory-key/"),
              ("COD Central, Militia Arms Depot", "https://codcentral.net/blog/mw4-dmz-militia-arms-depot-key/")),
    ]},
    {"id": "x01", "title": "X01 loot", "subtitle": "Season 1 black site", "blocks": [
        P("**Getting in and out.** The entrance is a facility on the edge of Hajin near the northern border: hit the gate switch, then take the elevator with your whole squad inside. Exfils close as the match goes on, so finish the steps inside to get out. Ghost is your Watcher in there."),
        TABLE(["Room", "Keycard", "What's been inside"], [
            ["Deep Vault 406", "On the Executive Room desk (3 runs out of 3)", "SR-16 Bio Agent Sample loose on the lab table; 4 safes, about 29,000"],
            ["Executive Room (Admin Offices, 2nd floor)", "Encode \"Executive Access\" at a Keycard Encoder (Supply Depot or Data Center)", "Weapons Grade Isotope (12,000), R-4 Bio-Compound, Ballistic Fabric, plus the 406 and Maintenance Room cards in a jacket"],
            ["Audit Room (Main Warehouse top floor)", "Jacket or Industrial Locker in the Supply Depot, Bio Lab jacket, Admin surveillance room", "KG-7 Vulcan Manual, Gilded Medal (15,000), Gilded Maritime Relic (7,000)"],
            ["Small Test Chamber (Tech Lab)", "Not stated", "Gold Bar, 2 Gilded Maritime Relics, Encrypted Archive"],
            ["Maintenance Room (top of Production Assembly)", "Encode \"Maintenance Access\" or the Executive Room jacket", "Alloyed Plating, Comms Module, Encrypted Archive"],
            ["Superintendent's Office (upper level, west of the Main Warehouse icon)", "Random loot", "Weapons Grade Isotope, 2 Human Trial Records (8,000 each), Legendary MAR-9, Zip Gun recipe; about 60,000"],
            ["Lt. Chol-Min's Stash Room (Motor Pool, E7)", "Drops from Lt. Chol-Min", "Medium Scavenger Backpack recipe, Legendary Swaegolja, Cipher Code Ledger"],
            ["Deep Vault 106", "Enemy operator in a Data Center stairwell", "Legendary Rezi 12, Wz. 55 Striga, intel"],
            ["Deep Vault 301", "Random; The Captain usually drops it", "Animal Trial Records, Han 86, Regional Combat Notes"],
        ]),
        TABLE(["Boss", "Where, and what it drops"], [["The Captain", "Main Warehouse and Logistics Tunnel. Deep Vault keycard (usually 301) and helmet pieces for the Threat Briefing, paid on exfil"],
            ["Wheelson", "Logistics Tunnel. Remote Module that opens the emergency exfil gate in the Power Generators"],
            ["Knuckle", "Dark server room in the Data Center. Rezi 12, Dog Tags, backpack"],
            ["The Wrench", "Motor Pool. Type 73 and a backpack that usually has a killstreak and a vest"],
            ["Blix", "Deep Vault only, not every match. Rezi 12 and a backpack that usually has a keycard"]]),
        P("**Samples for the X01 printer recipes:** SR-16 Bio Agent Sample is on the lab table in Deep Vault 406. Specter Fabric Sample is rare random loot inside X01; nobody has reported a fixed spot."),
        P("**Argonaut Armor without the Specter Fabric:** kill The Captain for a Deep Vault Access Card, hack the Core Room in the Deep Vault (northwest corner, lower levels) and take the suit from its display case. That's repeatable. X01 Orders page 5 also gives one, once. The Staff Emergency Exfil Keycard recipe is the X01 Orders page 4 reward."),
        P("**Patches:** UAVs and Advanced UAVs (Nov 10) and the Bombing Run (Nov 11) can't be used inside X01. Insurance now works if you die in X01 after deploying from Hajin (Nov 12), and Manuals, recipes and Dog Tags brought in from Hajin convert properly (Nov 13). Killing players in there raises your Bounty Level more slowly (Nov 7)."),
        LINKS(("DMZ Map X01", "https://dmzmap.com/x01"),
              ("Game Rant, Argonaut Armor", "https://gamerant.com/mw4-dmz-argonaut-armor-locations-blueprint/"),
              ("COD Central, Superintendent's Office", "https://codcentral.net/blog/mw4-dmz-x01-superintendents-office-keycard/"),
              ("COD Central, Deep Vault 406", "https://codcentral.net/blog/mw4-dmz-x01-deep-vault-406-keycard/"),
              ("Game Rant, Deep Vault", "https://gamerant.com/mw4-dmz-x01-unlock-deep-vault/")),
    ]},
    {"id": "reference", "title": "Quick reference", "subtitle": "Cash, Bank caps, levels", "blocks": [
        TABLE(["Source", "Pays"], [["Dynamic Op", "10,000–20,000, straight to the Bank"], ["Orders page", "20,000 on most pages"], ["Side Op", "2,000"],
            ["Mission step", "500"], ["Lieutenant", "10,000 first kill each"], ["Commander", "50,000 first kill each"],
            ["Lieutenant dog tag", "25,000 on extract in two guides; since Nov 16 the cash goes to every squad member"],
            ["Manual or recipe", "5,000 on extract"], ["Gold Bar", "25,000 to sell (Stash Weapon III and Bank X and XII need them)"],
            ["Legendary ingredient", "3,500 to sell"]]),
        P("**Scavenger Bonus (Nov 10):** if you die or miss exfil you now get some cash anyway, based on the value of what you had looted and how long you were deployed. Story Missions don't count. No amounts published."),
        P("**Hiding from UAVs (Nov 6):** Thermal Padding, Thermal Padding Pro and the Sedative Inhaler now hide you from UAVs and upgraded UAV Towers. An Advanced UAV still finds you. A bug that let Operators with the UAV Upgrade trait see you anyway was fixed Nov 12. Mini Tracker's radius was cut slightly on Nov 10."),
        P("**Nov 16 patch:** the UAV Upgrade Pro trait now zooms the minimap out 1.5x, down from 3x. Loot from a destroyed Deathstalker wreck can be pinged, and a weapon extracted in the Backpack Weapon slot now equips properly on your next run."),
        P("**Nov 11 to 13 patches:** solos and duos build Bounty a little faster, Wager Match trophies drop more often, and a finished 3D Printer recipe can be untracked again. Activision says changes to DMZ time-to-kill are in testing."),
        P("**Bank caps:** Start 100,000 · I 250,000 · II 500,000 · III 1M · IV 2M · V 5M · VI 10M · VII 25M · VIII 50M · IX 100M · X 250M · XI 500M · XII 1B · XIII 2B. Cash over the cap is lost."),
        P("**Levels that matter:** 10 Gunsmith · 15 third Operator · 25 Gunsmith 5% off · 37 3-Plate vest · 48 Self-Revive Kit recipe · 55 Disposable Parachute · 70 +18 item slots. Police Stations: D2, C4, F4, H5, G7. Compounds: Foxtrot B4, Charlie D4, Alpha E7, Bravo F8, Echo G7, Delta H4."),
    ]},
    {"id": "sources", "title": "Where this comes from", "subtitle": "Re-checked " + AS_OF, "blocks": [
        P("Loot spots, costs and prices come from fan sites and player reports, re-checked " + AS_OF + ". Printer recipes and upgrade costs were compared on Nov 15 with COD Central's list (updated Nov 14) and match, except Survivor Box and Staff Emergency Exfil Keycard, where sources disagree. When the game disagrees with this app, trust the game and tell James."),
        LINKS(("COD Central", "https://codcentral.net/blog/mw4-dmz-weapon-manuals/"), ("DMZ Map", "https://dmzmap.com/x01"),
              ("GG Ranked upgrades", "https://ggranked.com/games/call-of-duty-modern-warfare-4/modes/dmz/database/recipes?category=upgrades"),
              ("DMZ Radar upgrades", "https://dmzradar.com/upgrades.html"),
              ("Season 1 patch notes", "https://www.callofduty.com/patchnotes/2026/11/call-of-duty-modern-warfare-4-season-1-patch-notes")),
    ]},
]

# Oct 30, 2026: dmzcodex.com started loading a script (oceanpoet.com) that sends visitors to
# scam pages (fake virus alerts, fake ad-blocker downloads). Don't link to it until that's gone.
BLOCKED_HOSTS = ("dmzcodex.com",)
MAP_URL = "https://github.com/Jb631/exfil-ledger-data/blob/main/MAP.md"
NOTICE = "Nov 16 patch: Lieutenant dog tag cash now goes to every squad member. Resupply Run is listed as ending Nov 19, and War Chest as starting the same day (one source)."
# Build 4+ open this in the locked viewer; the page itself may only go to these hosts.
SAFE_MAP = {"url": "https://codmunity.gg/dmz/map", "hosts": ["codmunity.gg"]}
for sec in intel:
    kept = []
    for b in sec["blocks"]:
        if b["type"] == "links":
            b["links"] = [l for l in b["links"] if not any(h in l["url"] for h in BLOCKED_HOSTS)]
            if not b["links"]:
                continue
        kept.append(b)
    sec["blocks"] = kept
    if sec["id"] == "sources":
        sec["blocks"].insert(1, P("DMZ Codex was one of these sources. On Oct 30 its site started sending visitors to scam pages, so the app no longer links to it."))
assert "dmzcodex" not in json.dumps(intel)

out = {"schema": SCHEMA, "rev": REV, "asOf": AS_OF, "notice": NOTICE, "mapURL": MAP_URL, "safeMap": SAFE_MAP, "weapons": weapons, "items": items, "upgrades": upgrades,
       "lines": src["lines"], "recipes": recipes, "cats": cats, "intel": intel}

# Build 5+: structured spots, key rooms and the What's new feed (older builds ignore these keys).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spots as _spots
_known = {x["id"] for x in weapons + items + recipes}
_rooms = {r["id"] for r in _spots.ROOMS}
assert len(_rooms) == len(_spots.ROOMS), "duplicate room id"
for s in _spots.SPOTS:
    for t in s["for"]:
        assert t in _known, ("unknown spot target", t)
for n in _spots.NEWS:
    assert n["ref"] is None or n["ref"] in _known or n["ref"] in _rooms, n
assert "dmzcodex" not in json.dumps([_spots.SPOTS, _spots.ROOMS, _spots.NEWS])
out["spots"], out["rooms"], out["news"] = _spots.SPOTS, _spots.ROOMS, _spots.NEWS

# integrity checks the app relies on
ids = {i["id"] for i in items}
for u in upgrades + recipes:
    for m in u["mats"]:
        assert m["i"] in ids, (u["name"], m)
uids = {u["id"] for u in upgrades}
for r in recipes:
    assert r["unlock"] in ("level", "toggle") or r["unlock"] in uids, r
    assert r["unlock"] != "level" or isinstance(r["lvl"], int), r
for l in src["lines"]:
    assert all(t in uids for t in l["tiers"])
if os.path.isdir(os.path.join(ROOT, "ExfilLedger")):      # the app's Xcode project
    targets = (os.path.join(ROOT, "ExfilLedger", "kit.json"), os.path.join(ROOT, "data", "kit.json"))
else:                                                     # the data repo
    targets = (os.path.join(ROOT, "kit.json"),)
for target in targets:
    with open(target, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
print("kit.json rev", REV, "weapons", len(weapons), "items", len(items), "upgrades", len(upgrades), "recipes", len(recipes), "intel", len(intel))
