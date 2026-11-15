"""Structured loot spots, key rooms and the What's new feed (build 5+ reads these).

Builds 1-4 ignore the extra keys, so this is safe to publish before build 5 ships.

spot : {"for": [ids], "place", "where", "threat", "key", "n", "date"}
  for    weapon id (its Manual), recipe id (the recipe drop) or item id
  place  short name used for grouping ("Cheonwang Peak Array")
  where  the exact container or room
  threat Low / Medium / High / Extreme / Critical / X01, or None when nobody rated it
  key    None when you can walk in, otherwise how you get in
  n      number of reports (1 = a single run)
  date   yyyy-mm-dd of the newest report
room : {"id", "name", "where", "keyFrom", "threat", "loot", "date", "x01"}
news : {"date", "title", "sub", "ref"}   ref = room id, item/weapon/recipe id, or None
"""

SPOTS, ROOMS, NEWS = [], [], []


def S(targets, place, where, threat=None, key=None, n=1, date="2026-11-05"):
    if isinstance(targets, str):
        targets = [targets]
    SPOTS.append({"for": targets, "place": place, "where": where, "threat": threat, "key": key, "n": n, "date": date})


def R(rid, name, where, key_from, threat, loot, date, x01=False, gives=()):
    """A locked room. `gives` are ids found inside; each also becomes a spot."""
    ROOMS.append({"id": rid, "name": name, "where": where, "keyFrom": key_from, "threat": threat,
                  "loot": loot, "date": date, "x01": x01})
    for g in gives:
        S(g, name, where, threat, key_from, 1, date)


def N(date, title, sub, ref=None):
    NEWS.append({"date": date, "title": title, "sub": sub, "ref": ref})


# ---- Key rooms (each `gives` id also gets a spot) ---------------------------------------------
R("room_shopping_drc", "Shopping DRC Locker", "Under NuriGO Mall", "Key is random loot (one came from a Cheonwang Peak Array safe)",
  "Medium–High", "APOC-338, Patriot XMR and Rezi 12 Manuals; Large Secure Backpack (15,000)", "2026-11-05",
  gives=["w_apoc_338", "w_patriot_xmr", "w_rezi_12", "i_nuclear_program_files"])
R("room_reactor_drc", "Reactor DRC Locker", "Underwater in the Reactor 02 pool", "Key is the Operation Fallen Ember reward",
  "High", "Warlord Manual, 3-Plate Ballistic Gel Vest, Large Secure Backpack", "2026-11-05",
  gives=["w_warlord", "i_nuclear_program_files"])
R("room_airbase_drc", "Air Base DRC Weapons Locker", "Chang-san bunker armory", "Key is random loot (one in a duffel at Imjin Farmland)",
  "Extreme", "Cronen Squall Manual (reported as \"Cronin\"), 3-Plate Helmet Armor Vest", "2026-11-05",
  gives=["w_cronen_squall", "i_encrypted_archive"])
R("room_netshin_it", "Netshin IT Room", "Netshin Tech Complex, floor 14", "Key from apartment lockers or random loot",
  "Extreme", "Rezi 12 Manual, Power Regulator, Volatile Explosives, 5 intel items", "2026-11-05",
  gives=["w_rezi_12", "i_power_regulator", "i_volatile_explosives"])
R("room_netshin_security", "Netshin Security Office", "Netshin Tech Complex upper floor, rifle case", "Key",
  "Extreme", "ISO Nightshade Manual", "2026-11-05", gives=["w_iso_nightshade"])
R("room_counting_vault", "Counting Room Vault", "Casino", "Operation Silent Ledger; industrial locker on the Rice Mill catwalk; Haksan School armory",
  "High", "Zip Gun recipe, Gold Skull", "2026-11-05", gives=["r_zip_gun", "i_gold_skull", "i_encrypted_archive"])
R("room_vault_armory", "Vault Armory", "Under the Casino", "Casino carpet, Songdo Wharf duffel, Irradiated Container, Prison Encampment Storage",
  "High", "Cipher Code Ledger, Stabilized Reagents, Alloyed Plating, Nuclear Program Files", "2026-11-05",
  gives=["i_cipher_code_ledger", "i_stabilized_reagents", "i_alloyed_plating", "i_nuclear_program_files", "w_ppsh_41"])
R("room_south_block", "South Block Armory", "Prison Citadel", "Counter in the Citadel Main Control Room (needs its own key)",
  "Critical", "Gold Skull, Sanctioned Assassination List, a recipe", "2026-11-05",
  gives=["i_gold_skull", "i_sanctioned_assassination_list"])
R("room_bank_vault", "Bank Branch Vault", "Wolves branch or Cheongun branch", "Teller counter at Wolves, or the floor behind the teller windows in Cheongun",
  "Medium", "Cipher Code Ledger, 8 intel items, once a Gold Skull", "2026-11-05",
  gives=["i_cipher_code_ledger", "i_infantry_invasion_plans", "i_ballistic_flight_logs"])
R("room_gangbyeon_b", "Gangbyeon Apartment B", "Compound Echo apartments", "Bookshelf or desk in a Compound Echo apartment",
  "Medium", "2 W.M.D Manifests, 3 Degraded Execution Footage, Comms Module, Prison Encampment key", "2026-11-05",
  gives=["i_w_m_d_manifest", "i_comms_module", "i_degraded_execution_footage"])
R("room_hanex_guard", "Hanex Guard Station", "Hanex Bank", "Key is random loot",
  "Extreme", "Power Regulator (loose), Cipher Code Ledger, a Legendary Warlord", "2026-11-05",
  gives=["i_power_regulator", "i_cipher_code_ledger", "i_regional_combat_notes"])
R("room_coin_den", "Coin Mining Den", "NuriGO West, upstairs", "Key is the Operation Shopping Hacks reward",
  None, ".50 GS Manual, 6 CPUs, Nuclear Program Files", "2026-11-05",
  gives=["w_50_gs", "i_cpu", "i_nuclear_program_files"])
R("room_doctor", "The Doctor's Command Office", "Mirae General Hospital, floor 7, rooms 704 and 705", "Drops from The Doctor (not every kill)",
  "Low", "Tempered Armor Vest recipe on one run. A second run had no recipe: Legendary Doctor's Salve rifle (6,900), Volatile Explosives, High-Tenacity Fibers, Encrypted Archive; about 28,000",
  "2026-11-11", gives=["r_tempered_vest", "i_volatile_explosives", "i_high_tenacity_fibers", "i_encrypted_archive"])
R("room_chemist", "The Chemist's Secure Armory", "Haneul Nuclear Reactor I4, a bunker on the northeast side just inside the radiation zone",
  "Drops from The Chemist (not every kill); one was in The Scavenger's backpack",
  None, "W.M.D Manifest (5,000), Legendary Chemical Reaction (5,900), Ballistic Fabric, Nuclear Program Files, 2 Durable Gas Masks, 15 Chemicals; about 32,000",
  "2026-11-11", gives=["i_w_m_d_manifest", "i_ballistic_fabric", "i_nuclear_program_files", "i_regional_combat_notes"])
R("room_militia_depot", "Militia Arms Depot", "Compound Echo apartment block B (G7), one flight up inside the Gangbyeon Apartment B front door",
  "Key is random loot; the front door also needs the Gangbyeon Apartment B key",
  "Medium", "Binding Catalyst, Nuclear Program Files, 2 Degraded Execution Footage, 5 more intel items; about 14,000", "2026-11-14",
  gives=["i_binding_catalyst", "i_nuclear_program_files", "i_degraded_execution_footage", "i_infantry_invasion_plans", "i_ballistic_flight_logs"])
R("room_roze_armory", "Roze's Highrise Armory", "Netshin Tech Complex, floor 14",
  "Drops from Roze on the DBN Headquarters roof (not every kill); also the Operation Grid Assault reward",
  "Extreme", "A Lieutenant crate and two weapon lockers; one visit had the Legendary Kraken sniper", "2026-11-12")
R("room_downtown_lobby", "Downtown Branch Lobby Main", "Hanex Bank downtown branch lobby, north edge of The Grid (G6)", "Key is random loot",
  "Critical", "Encrypted Archive, a Vault Armory key and Bank Branch Vault Access; about 2,900", "2026-11-10", gives=["i_encrypted_archive"])
R("room_gorani", "Gorani's Scout Overlook", "Mujin Pass", "Drops from Lieutenant Gorani",
  None, "Legendary \"Incisor\" rifle, UAV", "2026-11-05")
R("room_barber", "Old Barber Shop", "Barber shop", "Key is random loot",
  "Low", "Cipher Code Ledger, Legendary Revive Pistol, Commandant Office key", "2026-11-05", gives=["i_cipher_code_ledger"])
R("room_hanwoori", "Hanwoori Art Records Room", "The Grid", "Key",
  "Critical", "Screamer Mine and Stim recipes, Power Regulator", "2026-11-05",
  gives=["r_screamer_mine", "r_stim", "i_power_regulator"])
R("room_hoesik", "Hoesik Supply Room", "By the Rice Mill", "Key",
  "Medium", "Impact Warhead recipe (cache), Nylon Laminate on the shelf by the door, 2 Degraded Execution Footage", "2026-11-05",
  gives=["r_impact_warhead", "i_nylon_laminate", "i_degraded_execution_footage"])
R("room_radio", "Haejeok Radio Station", "Imjin Farmland D6, upstairs in the white building under the red mast", "Key is random loot",
  None, "2 Comms Modules, Power Regulator, 5 CPUs, 10 Electronic Sensors, 6 Control Units, safe with 7 intel items; about 25,000", "2026-11-09",
  gives=["i_comms_module", "i_power_regulator", "i_cpu", "i_electronic_sensors", "i_control_units", "i_printed_circuit_board",
         "i_nuclear_program_files", "i_degraded_execution_footage", "i_encrypted_archive"])
R("room_chem_lockers", "Hospital Chemical Lab and Lockers", "Mirae Hospital basement (F5)",
  "Lab key: floor 7 office desk or shelves. Locker keys: morgue table or lab bench, one per locker",
  "Low", "2-Plate Helmet Armor Vest recipe, Binding Catalyst (unlocked cache by the lab door), 7 Detonators, 2 Medkits", "2026-11-08",
  gives=["r_2_plate_helmet_vest", "i_binding_catalyst", "i_detonators", "i_biomaterials"])
R("room_mod_workshop", "Weapons Mod Workshop", "Chang-san Air Base B5, upstairs in the repair garage", "Key is random loot",
  "Extreme", "Small Secure Backpack recipe, Cipher Code Ledger, 2-Plate Helmet Armor Vest; about 17,000", "2026-11-10",
  gives=["r_small_secure_backpack", "i_cipher_code_ledger"])
R("room_police_armory", "Police Station Armory", "Basement of each police station (D2, C4, F4, H5, G7)",
  "Inside each station, usually on an office desk or table",
  "Low–Medium", "Ballistic Fabric (Cheongun), CPUs, a KG-7 Vulcan; 2,600 to 5,100 a station", "2026-11-09",
  gives=["i_ballistic_fabric", "i_cpu"])
R("room_field_depot", "Field Depot", "Chang-san Air Base B5, supply warehouse", "Key is random loot (one from a Wilderness bunk duffel)",
  "Extreme", "Legendary Parachute, Hazard Storehouse key; about 8,500", "2026-11-08")
R("room_haksan", "Haksan School Armory", "Deadtown B7, second-floor classroom", "Key is random loot (one in Chol-Min's Stash Room)",
  None, "Structural Alloy, Encrypted Archive; about 10,000. No recipes or Manuals", "2026-11-09", gives=["i_structural_alloy"])
R("room_foreman", "Imjin Mill Foreman's Office", "Rice Mill D8, upstairs", "Key is random loot",
  "Medium", "About 6,750. No recipes or Manuals", "2026-11-08")
R("room_gas_station", "Gas Station Electrical Room", "Under the Korin Oil station, Construction Zone H7", "Key is random loot",
  None, "Turned Components, 5 CPUs, Printed Circuit Board; about 8,600", "2026-11-09",
  gives=["i_turned_components", "i_cpu", "i_printed_circuit_board"])
R("room_hazard", "Hazard Storehouse", "Haneul Reactor I5, south of the cooling towers (radiation zone)",
  "Key is random loot (Field Depot locker; enemy operator at the Cheongun Outskirts gas station)",
  "High", "2 Binding Catalyst, Radiation Blockers; about 7,250", "2026-11-08", gives=["i_binding_catalyst"])
R("room_mechanic", "Mechanic's Shack", "Cheongun Village F5, south of the clinic", "Key is random loot (one in a military locker on the train)",
  "Low", "Legendary Large Backpack; about 8,400. No recipes or Manuals", "2026-11-08")

# X01
R("x01_superintendent", "X01 Superintendent's Office", "Upper level, west of the Main Warehouse icon", "Keycard is random loot",
  "X01", "Weapons Grade Isotope (12,000), 2 Human Trial Records (8,000 each), Legendary MAR-9, Zip Gun recipe, 2 High-Tenacity Fibers; about 60,000",
  "2026-11-09", x01=True, gives=["r_zip_gun", "i_high_tenacity_fibers", "i_nylon_cloth", "i_nitro_compounds"])
R("x01_cholmin", "X01 Lt. Chol-Min's Stash Room", "Motor Pool E7, above his hall; climb the rope in the cage in his room", "Drops from Lt. Chol-Min",
  "X01", "Medium Scavenger Backpack recipe, Legendary Swaegolja LMG, Cipher Code Ledger, Haksan School Armory key; about 29,000",
  "2026-11-09", x01=True, gives=["r_medium_scavenger_backpack", "i_cipher_code_ledger"])
R("x01_406", "X01 Deep Vault 406", "Deep Vault", "Keycard on the Executive Room desk (3 runs out of 3)",
  "X01", "SR-16 Bio Agent Sample loose on the lab table; 4 safes, about 29,000", "2026-11-07", x01=True,
  gives=["i_sr_16_bio_agent_sample", "i_encrypted_archive"])
R("x01_executive", "X01 Executive Room", "Admin Offices, 2nd floor", "Encode \"Executive Access\" at a Keycard Encoder (Supply Depot or Data Center)",
  "X01", "Weapons Grade Isotope (12,000), R-4 Bio-Compound, Ballistic Fabric, plus the 406 and Maintenance Room cards in a jacket",
  "2026-11-07", x01=True, gives=["i_ballistic_fabric"])
R("x01_audit", "X01 Audit Room", "Main Warehouse top floor, safe", "Jacket or Industrial Locker in the Supply Depot, Bio Lab jacket, Admin surveillance room",
  "X01", "KG-7 Vulcan Manual, Gilded Medal (15,000), Gilded Maritime Relic (7,000)", "2026-11-07", x01=True, gives=["w_kg_7_vulcan"])
R("x01_test_chamber", "X01 Small Test Chamber", "Tech Lab, safe", "Keycard source not reported",
  "X01", "Gold Bar, 2 Gilded Maritime Relics, Encrypted Archive", "2026-11-07", x01=True, gives=["i_gold_bar", "i_encrypted_archive"])
R("x01_maintenance", "X01 Maintenance Room", "Top of Production Assembly", "Encode \"Maintenance Access\", or the Executive Room jacket",
  "X01", "Alloyed Plating, Comms Module, Encrypted Archive", "2026-11-07", x01=True,
  gives=["i_alloyed_plating", "i_comms_module", "i_encrypted_archive"])
R("x01_106", "X01 Deep Vault 106", "Deep Vault", "Enemy operator in a Data Center stairwell",
  "X01", "Legendary Rezi 12, Wz. 55 Striga, intel", "2026-11-07", x01=True)
R("x01_301", "X01 Deep Vault 301", "Deep Vault", "Random; The Captain usually drops it",
  "X01", "Animal Trial Records, Han 86, Regional Combat Notes", "2026-11-07", x01=True, gives=["i_regional_combat_notes"])

# ---- Spots you can walk into (no key) ----------------------------------------------------------
# Manuals
S("w_m4", "Prison Citadel yard", "Tool Chest", "Critical", None, 1, "2026-11-06")
S("w_finn_lmg", "Cheongun Village station", "Rail Depot Storage in the basement", "Low", None, 1)
S("w_vel_46", "Deadtown Re-Education Center", "Military Locker", None, None, 1, "2026-11-03")
S(["w_type_73", "w_ppsh_41", "r_zip_gun"], "Chang-san barracks (Operation Iron Citadel)", "Duffels on the bunks", "Critical", None, 2)
S("r_combat_drone", "Chang-san barracks (Operation Iron Citadel)", "Green footlocker", "Critical", None, 1)
S(["r_pain_killers", "r_energy_drink", "r_drill_charge"], "Chang-san barracks (Operation Iron Citadel)",
  "Mirrored medicine cabinets over the washroom sinks", "Critical", None, 1)
S("w_type_73", "Cheonwang Peak Array", "Filing cabinet", "Medium", None, 1, "2026-11-03")
S(["w_kastov_762", "w_jokr"], "Irradiated Container", "Decontaminate it at Reactor 02; 16 of 16 held a Manual", "High", None, 16, "2026-11-03")
S(["w_rpg_8", "r_advanced_uav"], "Iron Citadel armory, Chang-san bunker", "Weapons Locker", "Extreme", None, 1, "2026-11-03")
S("w_sang_9mm", "Train through Cheongun Outskirts", "Blue duffel on a seat", None, None, 1)
# Recipes
S("r_zip_gun", "Cheongun Village fire station", "Upstairs cache", "Low", None, 1)
S("r_screamer_mine", "Hotel Lucera, Suite 703", "Bedroom weapons locker", "Critical", "Key", 1)
S("r_smelling_salts", "Reactor 02 Control Room", "Chemical Storage", "High", None, 1)
S("r_2_plate_ballistic_gel_vest", "Casino", "Grey filing cabinet in a small office", "High", None, 1)
S("r_2_plate_helmet_vest", "Compound Echo", "Roof crates by the SAM site", "Medium", None, 1)
S("r_large_scavenger_backpack", "Fire station, North Korean Wilderness", "First aid kit on a garage pillar", None, None, 1)
# Ingredients
S(["i_power_regulator", "i_cpu"], "Cheonwang Peak Array", "Server building, 4th floor: server blades and racks", "Medium", None, 3)
S("i_turned_components", "North Korean Wilderness", "Industrial lockers", None, None, 1)
S(["i_turned_components", "i_comms_module"], "Police Weapon Depository, Wolves Stadium", "Lockers and the server blade", None, "Key", 1)
S("i_alloyed_plating", "Bubun Yard", "Tool chest", None, None, 1)
S(["i_alloyed_plating", "i_nylon_laminate"], "Commandant Office", "Weapons locker and military locker", None, "Key (one came from the Old Barber Shop)", 1)
S("i_volatile_explosives", "Oamsik Turtle Island", "Hidden cache", None, None, 1)
S("i_ballistic_fabric", "Shop Records Room", "Inside the room", None, "Key", 1)
S(["i_ballistic_fabric", "i_w_m_d_manifest"], "Irradiated Container", "Decontaminate it at Reactor 02", "High", None, 2, "2026-11-03")
S("i_high_tenacity_fibers", "Chang-san Air Base", "Armory and Barracks", "Extreme", None, 1, "2026-11-10")
S("i_binding_catalyst", "Mirae General Hospital", "Medical tents and the cache by the Chemical Lab door", "Low", None, 2, "2026-11-08")
S("i_nylon_cloth", "Prison Citadel wings", "Also Deadtown underground holding and Mujin Nightclub", "Critical", None, 1)
S("i_specter_fabric_sample", "Inside X01", "Rare random loot; nobody has reported a fixed spot", "X01", None, 1, "2026-11-10")
# Legendary ingredients
S("i_military_composites", "The Colossus", "Not every kill. Reliable spot: behind the armory door in the Chang-san bunker (Operation Iron Citadel)", "Critical", None, 2, "2026-11-11")
S("i_prototype_rf_module", "Deathstalker wreck", "6 of 6 wrecks in one count. Mostly over The Grid (G6); one RPG-8 hit downs it", "High", None, 6, "2026-11-15")
S("i_nano_structured_alloy", "Destroyed Battle Tank", "Vehicle Hatch, Engine and Turret containers. One Impact Warhead destroys it", None, None, 3, "2026-11-12")
S("i_experimental_compounds", "The Colossus", "Drops sometimes", "Critical", None, 2, "2026-11-11")
S("i_experimental_compounds", "Deathstalker wreck", "2 of 6 wrecks in one count", "High", None, 2, "2026-11-15")
S("i_experimental_compounds", "Destroyed Battle Tank", "1 of 3 tanks in one count", None, None, 1, "2026-11-12")
S(["i_power_regulator", "i_nylon_laminate"], "Destroyed Battle Tank", "Wreck containers", None, None, 1, "2026-11-12")
S("i_structural_alloy", "Bale", "His backpack. Deadtown Re-Education Center top floor, or the Chang-san bunker", "Medium", None, 1, "2026-11-12")
S("i_sanctioned_assassination_list", "Roze", "Her backpack. DBN Headquarters roof, The Grid", "Extreme", None, 1, "2026-11-12")
# Gold and Bank intel
S(["i_gold_bar", "i_gold_skull"], "Compound Alpha", "Safes (7 from 33 in one count)", "Medium", None, 7)
S(["i_gold_bar", "i_gold_skull"], "Wolves Stadium", "Safes (about 1 in 8)", None, None, 3)
S("i_sanctioned_assassination_list", "Western bunkers", "Military Lockers", "Extreme", None, 1)
S("i_foreign_intelligence_targets", "Mirae Hospital Electrical Room (B2)", "Server blade", "Low", "Key", 1)
S("i_foreign_intelligence_targets", "Gaming Computers", "About 1 in 18, anywhere", None, None, 1)
S("i_w_m_d_manifest", "DBN HQ, Executive Arms Auction", "Inside the room", None, "Key", 1)
S("i_nuclear_program_files", "Reactor 02 Control Room", "Computer", "High", None, 1)
S("i_regional_combat_notes", "Compound Delta", "About 1 in 5 containers", "Medium", None, 3)

# ---- What's new (sorted newest first at the end of this file) --------------------------------------
N("2026-11-15", "Resupply Run is live", "Trade items at the FOB for six rewards; reported to end before Nov 19")
N("2026-11-15", "Deathstalker drops counted", "Prototype RF Module in 6 of 6 wrecks", "i_prototype_rf_module")
N("2026-11-14", "Militia Arms Depot", "Binding Catalyst and intel items; about 14,000", "room_militia_depot")
N("2026-11-13", "Legendary ingredients sell for cash again", "Patch: 3,500 each. Manuals and recipes now convert when you enter X01 from Hajin")
N("2026-11-12", "Battle Tank loot", "Nano-Structured Alloy in the Hatch, Engine or Turret", "i_nano_structured_alloy")
N("2026-11-11", "The Chemist's Secure Armory", "About 32,000, with a W.M.D Manifest", "room_chemist")
N("2026-11-11", "Bombing Run is off inside X01", "Patch: solos and duos also build Bounty a little faster")
N("2026-11-10", "UAVs are off inside X01", "Patch: UAVs and Advanced UAVs can't be used in X01")
N("2026-11-10", "Failing to exfil now pays some cash", "Patch: Scavenger Bonus, based on loot value and time deployed")
N("2026-11-10", "Weapons Mod Workshop", "Small Secure Backpack recipe, Cipher Code Ledger", "room_mod_workshop")
N("2026-11-09", "X01 Superintendent's Office", "About 60,000 and a Zip Gun recipe", "x01_superintendent")
N("2026-11-09", "X01 Lt. Chol-Min's Stash Room", "Medium Scavenger Backpack recipe", "x01_cholmin")
N("2026-11-09", "Haejeok Radio Station", "2 Comms Modules, Power Regulator, 5 CPUs", "room_radio")
N("2026-11-08", "Hospital Chemical Lockers", "2-Plate Helmet Armor Vest recipe, Binding Catalyst", "room_chem_lockers")
N("2026-11-07", "X01 Audit Room safe", "KG-7 Vulcan Manual", "x01_audit")
N("2026-11-07", "X01 Deep Vault 406", "SR-16 Bio Agent Sample on the lab table", "x01_406")
N("2026-11-06", "Thermal Padding hides you from UAVs", "Patch: so does the Sedative Inhaler; an Advanced UAV still finds you")
N("2026-11-05", "Season 1 guns", "Cronen Osprey at Battle Pass tier 16, CSG-35 at tier 36; both come with their Manual", "w_cronen_osprey")

NEWS.sort(key=lambda n: n["date"], reverse=True)   # stable: same-day entries keep file order
