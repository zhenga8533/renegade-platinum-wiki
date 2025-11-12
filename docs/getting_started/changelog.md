# Changelog

Full version history for Pokémon Renegade Platinum.

---

## v1.3.0 - 16/04/2019

### Breaking Changes

!!! danger "Patching System Changed"
    The patching system for the hack has changed significantly:

    - **Two base patches** now available: one for 3541 ROMs, one for 4997 ROMs
    - Use the appropriate patch for your ROM version
    - Additional patches can be applied on top of Renegade Platinum:
        - Classic mode
        - Main series shiny rates
        - Speed up patch
    - **Must uncheck "Checksum validation"** in Delta Patcher Lite when applying multiple additional patches, or you'll get `XD3_INVALID_INPUT` errors
    - See the README in the additional patches folder for details

!!! info "Standard Version Changes"
    The standard Renegade Platinum (after initial patch) now uses what was previously known as the **Complete and Shiny Boosted version**:

    - All Pokémon changes are present
    - Shiny rate is **1/512** by default

### New Features

!!! success "Additions"
    - **Battle Steven** in Oreburgh City after defeating the Pokémon League
    - **Hidden Power teller NPC** in Jubilife Trainers' School (tells type, not power)
    - **Obedience check disabled** for traded Pokémon - all Pokémon listen to you at all times
    - **Pokédex encounter locations** now accurately listed (thanks to Mikelan98!)

### Pokémon Changes (Both Versions)

**Evolution Level Adjustments:**

- Spheal → Sealeo at **Level 24** (was 32)
- Sealeo → Walrein at **Level 40** (was 44)
- Aron → Lairon at **Level 24** (was 32)
- Lairon → Aggron at **Level 40** (was 42)

**Moveset Adjustments:**

- Sealeo, Walrein, Lairon, and Aggron level-up moves adjusted
- Oddish, Gloom, and Vileplume level-up moves reshuffled
- Oddish and Gloom now learn Sludge by level

**TM/HM Compatibility:**

- Glalie can now learn **Rock Tomb** by TM
- Zigzagoon, Linoone, Gligar, and Gliscor can now learn **Rock Climb** by HM

### Changes

- Celestic Town "glasses" man now gives **all items at once** instead of time-dependent
- Boy at Oreburgh City entrance now gives you an **Oval Stone** (helpful for Happiny)
- Item changes document now lists **key item locations**
- Added FAQ entry about **Poké Radar shiny boost interaction**

### Bug Fixes

- Modified Maylene's dialogue on Route 217 to prevent text cutoff with long player names
- Fullmoon Island rock now uses Moss Rock overworld (prevents accidental Rock Smash destruction)
- Fixed fishing encounter errors in wild document
- Fixed Route 213 Floatzel encounter listing error
- Fixed trainer names with "nd" instead of "&"
- Fixed some trainers' rematch teams
- Fixed incorrect level on one of Lucian's Pokémon
- Fixed Victory Road trainers incorrectly knowing Shadow Force on Dusknoir/Banette

---

## v1.2.1 - 18/01/2019

### Pokémon Changes (Both Versions)

- Glalie can now learn **Rock Polish** by TM

### Changes

- NPC that fixes saves from earlier versions no longer affects Celebi event
- Can now interact with Celestic Town shrine again after updating to v1.2.1
- Celebi event should now work properly (players who already caught Celebi can get a second one!)

### Bug Fixes

- Fixed bug where Celebi event failed to activate
- If you previously collected the GS Ball from the shrine, the event should work now

---

## v1.2.0 - 14/01/2019

### New Features

!!! success "Additions"
    - **Berry seller** in Berry Master's house (Route 208) sells unobtainable Berries (Liechi, Salac, etc.)
    - **Moss Rock and Ice Rock** returned - give Leaf Stone and Ice Stone respectively
    - Added **Type Changes** documentation with justifications
    - Added **Frequently Asked Questions** document

### Pokémon Changes (Both Versions)

**Moveset Additions:**

- Chikorita, Bayleef, Meganium: Learn **Draining Kiss** and **Moonblast** by level
- Totodile, Croconaw, Feraligatr: Learn **Night Slash** by level
- Milotic: Learns **Moonblast** by level
- Glalie: Learns **Rock Slide** by level and TM; **Stone Edge, Rock Smash, Rock Climb** by TM/HM

### Pokémon Changes (Complete Version Only)

!!! info "Type Changes"
    - **Meganium** → Grass/Fairy
    - **Feraligatr** → Water/Dark
    - **Milotic** → Water/Fairy
    - **Glalie** → Ice/Rock

### Bug Fixes

- Fixed Ghost-type attacks being neutral against Dark-type Pokémon
- Fixed Ghost-type attacks being not very effective against Dragon-type Pokémon
- Fixed save upgrade NPC sometimes breaking Celebi event
- Fixed Deoxys event by modifying the event (now works on previously broken saves if League defeated)
- Fixed Wayward Cave trainer pair not triggering double battle
- Fixed Volkner using two normal Rotom instead of Heat/Wash forms in Battleground rematch
- Fixed Snowpoint Temple guards allowing battle with only one Pokémon (causing glitch send-out)
- Fixed Veilstone Department Store NPC reference to Counter Pokétch app
- Fixed Combusken and Blaziken learning Fire Blast instead of Flare Blitz

---

## v1.1.2 - 02/01/2019

### Bug Fixes

- Fixed Stealth Rock doing seemingly random amounts of damage
- Fixed Old Chateau new NPCs crashing the game
- Fixed Eevee in intro reverting to Buneary
- Fixed Pokémon Changes document listing wrong Charizard ability

---

## v1.1.1 - 01/01/2019

### Bug Fixes

- Fixed game crash when interacting with Galactic grunts harassing Honey seller in Floaroma Meadow

---

## v1.1.0 - 01/01/2019

### Breaking Changes

!!! danger "ROM Base Changed"

    Base ROM changed from **3541** to **4997** (4998 on some sites). This should match dumps from genuine American Platinum cartridges (unless bought near initial release).

### Breaking Bug Fixes

!!! warning "Important for Save File Transfers"

    - Trigger script indexes changed to prevent potential bugs
    - GS Ball now replaces **Loot Sack** instead of Shoal Shell (Shell Bell sprite fixed)

!!! danger "IMPORTANT - Trigger Fixes"

    If carrying a save file from an older version:

    1. **Immediately** go to Pokémon Center in Eterna, Hearthome, Veilstone, or Jubilife
    2. Talk to NPC in center of room to synchronize trigger scripts
    3. Failure to do so may cause roadblocks to reappear or events to repeat

!!! warning "GS Ball Item Change"

    GS Balls in inventory from previous saves will now be Shoal Shells. This doesn't affect Celebi event, but you must complete the trigger synchronization step above.

### New Features

!!! success "Additions"

    - **Nature stat displays** now show stat boost/reduction after nature name
    - **Remoraid** now on Route 208 (earlier Mantyke evolution from Jubilife Egg)
    - **Rock Climb** now Rock-type move (power reduced to 80)
    - Rowan gives **10 Repels** after giving Poké Radar
    - **Sand Tomb replaced with Bulldoze** from later generations
    - **Nurse in Iron Island** big room heals Pokémon
    - **In-game menu decapitalized**
    - **Move Deleter** now in Oreburgh City
    - **Azure Flute** requires viewing diploma (nearly complete National Dex)
    - **Pokémon Center nurse dialogue reduced**
    - **Gardenia quest changed** - find her on Route 216 instead of showing her Snover

### Changes

- Dawn and Lucas now use **Seals on their starter** in later battles
- Roark, Gardenia, and Fantina teams adjusted slightly
- Pal Park destination dialogue updated for clarity
- Old Chateau maid only gives Old Gateau if you don't have one
- Traynee lists stat training options in High, Medium, Low order
- Traynee's stat training teams use harmless moves only

### Pokémon Changes (Both Versions)

**Moveset Changes:**

- Illumise: Learns **Draining Kiss** and **Moonblast** by level; no longer learns Charge Beam or Thunderbolt by level (still TM!)
- Mudkip, Marshtomp, Swampert: Learn **Aqua Tail** earlier
- Roselia: Learns **Sludge** and **Sludge Bomb** by level; no longer learns Leaf Storm (Roserade still does!)
- Swablu and Altaria: Learn **Moonblast** earlier
- Venusaur: Learns **Earth Power** by level
- Wailmer and Wailord: Learn **Body Slam** by level; no longer learn Thrash

**TM/HM Compatibility:**

- Leafeon: Now compatible with **Cut** HM
- Monferno, Infernape, Azumarill, Electivire, Dusknoir: Now compatible with **Drain Punch** TM
- Ninetales: Now compatible with **Psychic** and **Shadow Ball** TMs
- Shedinja: Now compatible with **Swords Dance** TM

**Other:**

- Unown catch rate: **225 → 255**

### Pokémon Changes (Complete Version Only)

!!! info "Type/Stat/Ability Changes"

    - **Altaria** → Dragon/Fairy; stats buffed slightly (again)
    - **Arbok** → Slight stat buff
    - **Dusknoir** → Gets **Iron Fist** instead of Frisk when evolved from Frisk Dusclops (doesn't apply to pre-patch Dusclops)
    - **Illumise** → Bug/Fairy; stats buffed (again)
    - **Sceptile** → Grass/Dragon; stats adjusted slightly
    - **Seviper** → Poison/Dark; stats modified (again)
    - **Swablu** → Fairy/Flying; stats buffed slightly (again)
    - **Typhlosion** → Gets **Adaptability**; stats modified (again)
    - **Vibrava/Flygon** → Get **Compoundeyes** when evolved from Hyper Cutter Trapinch
    - **Volbeat** → Stats buffed (again)

!!! warning "Ability Note"

    New abilities won't retroactively apply to existing Pokémon in carried-over saves. Only applies to new Pokémon or upon evolution.

### Bug Fixes

- All trainers now correctly have post-defeat dialogue
- Barry's starter has Seal again in Pastoria City onwards
- Charmander, Charmeleon, Blastoise now correctly learn Dragon Pulse by TM
- Fairy-type now displays correctly in Pokédex (thanks to Mikelan98!)
- Fixed Crasher Wake and Gym guide reappearing
- Fixed Wayward Cave crash when leaving after Mira joins
- Fixed incorrect Surf wild data on Route 208
- Fixed temporary Route 209 guard allowing you past after blocking once
- Fixed early Rock Climb access to Mt. Coronet summit
- Fixed sitting on top of Eevee Poké Ball when KOed early
- Postgame island Dark/Normal trainers now always challengeable
- Fixed Eterna Forest trainer saying "My MEDITITE!"
- Fixed inaccessible Route 213 Heart Scale location
- Fixed forced double battles not blocking progress with only one Pokémon

### Known Issues

- Evolving Wailmer into Wailord near Regi room disables warp until map reload
- Gengar's mini sprite looks strange on Pokétch
- Some trainer names appear odd (double battles, Frontier Brain battles)
- Some trainers (Dawn/Lucas) give $0 upon victory
- Rowan's briefcase event may act strangely if done after Distortion World

---

## v1.0.3 - 27/12/2018

### Features

- Bidoof and Bibarel: Learn **TM75 Swords Dance**
- Tropius: Learns **TM59 Dragon Pulse**
- Trapinch: Now appears in Oreburgh Mine (10% rate)
- Ampharos: Learns **Dragon Pulse** at Level 30, **Thunder Punch** at Level 1
- Traynee now **heals you** after any battle
- Item/Move Changes documents now outline what was replaced
- Wild Giratina now holds **Griseous Orb**
- Baby Pokémon (Pichu, Cleffa, Igglybuff, Togepi, Azurill, Budew, Chingling, Happiny) now have **base happiness 180**
- Slowpoke, Slowbro, Slowking: Learn **HM07 Waterfall**
- Item/Move Changes documents explicitly state replacements

### Bug Fixes

- Fixed Dunsparce and Purugly not appearing with Poké Radar on Routes 208 and 209
- Slowbro now correctly learns TM55 Scald
- Fixed Nidoking's level-up moves matching document
- Fixed various documentation typos

---

## v1.0.2 - 23/12/2018

### Documentation Fixes

- Fixed Maylene's Lucario having wrong item listed

### Game Fixes

- Fixed incorrect level-up moves, including Wood Hammer Glaceon
- Fixed Blastoise not learning Dark Pulse by TM
- Fixed Breloom not learning False Swipe by TM
- Fixed Wormadam Sandy/Trash forms not having Battle Armor in Complete version

---

## v1.0.1 - 22/12/2018

!!! success "Save Compatibility"

    Saves from v1.0.0 are fully compatible with this version.

### Changes

- Dratini, Dragonair, Dragonite: Learn **Aqua Jet** by level
- Heracross: Learns **Bullet Seed** by TM
- Beldum, Metang, Metagross: **Catch rate 3 → 45**
- Added **Evolution Changes** document

### Documentation Fixes

- Fixed Scald description in Move Changes document
- Added unlisted gift Pokémon to Special Events guide
- Added unlisted NPCs to NPC Changes guide
- Fixed Mars' Purugly moveset error
- Added Egg Cycles note to Pokémon Changes document
- Fixed Munchlax incorrectly listed as wild on Route 203
- Fixed Lasses Sarah and Samantha having swapped Pokémon

### Game Fixes

- Fixed Cubone not appearing on Route 203 outside of morning
- Fixed incorrect Route 228 encounters (day/night)
- Fixed Pachirisu's stats not adding up (+5 to Sp. Atk base)
- Fixed Scald incorrectly coded as contact move
- Fixed NPC stating Rock Smash rocks existed in Ravaged Path
- Fixed NPC/item overlap on Route 209
- Fixed ledge jump exploit on Route 203
- Fixed incorrect level-up moves, including Wood Hammer Glaceon (thanks @BurnSombreroBrn)
- Fixed Dawn using Lucas' dialogue on Route 202
- Fixed bike dismount softlock on Route 206
- Fixed walking through Galactic grunt blockade on Route 205
- Fixed Traynee's unlock requirement (Maylene instead of Wake)
- Fixed Pokétch coupon dialogue references
- Fixed Secret Potion/Black Glasses spacing typos
- Fixed Cheryl's Eterna Forest dialogue typo

### Known Issues

- Fairy-types incorrectly listed as Ghost-types in Pokédex
- Standing on Poké Ball when fainting early in game
- Eterna Forest Psychic mentions Meditite when they don't have one
- Glitch send-out in scripted double battles with one Pokémon
- Some trainers (Dawn/Lucas) give $0 upon victory
- Some trainers have no post-defeat dialogue

---

## v1.0.0 - 21/12/2018

!!! success "Initial Release"

    First public release of Pokémon Renegade Platinum!
