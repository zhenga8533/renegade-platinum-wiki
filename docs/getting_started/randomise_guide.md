# Randomization Guide

Manual guide for randomizing Renegade Platinum using the Universal Pokémon Randomizer.

!!! warning "Important Limitations"

    You **cannot** randomize everything due to how the hack has changed things. See the limitations section below for details.

---

## Limitations

!!! danger "What You CANNOT Randomize"

    The following features will likely cause crashes if you try to import them from the randomizer:

    - **Trainer battles**
    - **Gift Pokémon**
    - **TMs**
    - **Field items**
    - **Static encounters** (legendaries)

!!! warning "Text Changes Won't Transfer"

    You cannot carry any text changes the randomizer makes across, which may cause issues in cases where text changes are essential:

    - **Starters** - Pictures won't change in Rowan's briefcase (rely on cries only)
    - **In-game trades** - Text will still reflect original trades, making it hard to figure out what they want

!!! info "System Requirements"

    This process requires a **computer** (not a phone). Works on **Windows**; Mac/Linux may work if you find an alternative to crystaltile2.

---

## Tools Required

You need the following:

- **Vanilla Platinum ROM** (clean, unpatched)
- **Renegade Platinum ROM**
- **Universal Pokémon Randomizer** - [Download here](https://pokehacks.dabomstew.com/randomizer/)
- **crystaltile2** - [Download here](https://www.romhacking.net/utilities/818/)

---

## Randomization Steps

### Step 1: Randomize Vanilla Platinum

!!! tip "Step 1"

    1. Open the **Universal Pokémon Randomizer**
    2. Load your **vanilla Platinum ROM**
    3. Configure randomization settings (see limitations above)
    4. Save the randomized ROM

---

### Step 2: Open Randomized Platinum in crystaltile2

!!! tip "Step 2"

    1. Open your **randomized Platinum ROM** in crystaltile2
    2. Click the **DS icon** near the top (two icons left of the ? button in the blue circle)
        - This opens the file explorer for the ROM

---

### Step 3: Export Files from Randomized Platinum

!!! tip "Step 3"

    1. In the file explorer, **right-click** any file and select **"Export"** to save it to your PC
    2. Export the files corresponding to the elements you randomized
    3. See the **File Mapping Table** below for file locations

---

## File Mapping Table

!!! info "File Locations"

    Use this table to find which files correspond to which randomized elements:

    | Content | File Path |
    |---------|-----------|
    | **Pokémon Base Stats, Abilities, Types** | `poketool/personal/pl_personal.narc` |
    | **Pokémon Evolutions** | `poketool/personal/evo.narc` |
    | **Starter Pokémon** | `FSI.CT/overlay9_0078.bin` (near top of explorer) |
    | **In-Game Trades** | `fielddata/pokemon_trade/fld_trade.narc` |
    | **Moves** | `poketool/waza/pl_waza_tbl.narc` |
    | **Pokémon Movesets** | `poketool/personal/wotbl.narc` |
    | **Wild Pokémon** | `fielddata/encountdata/pl_enc_data.narc` |

---

### Step 4: Open Renegade Platinum in crystaltile2

!!! tip "Step 4"

    1. Open your **Renegade Platinum ROM** in crystaltile2
    2. Click the **DS icon** to bring up the file explorer

---

### Step 5: Import Files into Renegade Platinum

!!! tip "Step 5"

    1. **Right-click** on the file you want to replace (use same names from File Mapping Table)
    2. Select **"Import"**
    3. Choose the `.narc` file you exported from the randomized Platinum
    4. The file will be inserted into the ROM
    5. Repeat for all files you want to import

---

### Step 6: Save and Close

!!! tip "Step 6"

    1. Close crystaltile2
    2. Click **"Yes"** to the shutdown prompt
    3. The ROM should save automatically despite the message

!!! success "Done!"

    Open your edited Renegade Platinum ROM in your emulator, and your randomized changes should be active!

---

## Caveats and Known Issues

### Text Changes

!!! warning "Text Won't Update"

    Text changes will **not** carry across, as Renegade Platinum adds many extra text strings and changes existing ones (move names, Pokémon names, etc.), making it infeasible to transfer.

---

### Randomized Starters

!!! info "Starter Pictures Won't Change"

    - Pictures in Rowan's briefcase won't change (randomizer doesn't know how)
    - Normally, cries and text would change, but Renegade Platinum retains original text
    - **You must rely on cries alone** to figure out what the new starters are. Good luck!

---

### Randomized In-Game Trades

!!! warning "Trade Text Won't Update"

    If you've randomized the requested Pokémon for in-game trades, you'll have an **extremely hard time** figuring out what they want, as the text will still reflect the original trade.

---

### Randomized Wild Pokémon Levels

!!! warning "Wild Levels Remain Vanilla"

    If you've randomized wild Pokémon, the **levels will still be those of original Platinum**, instead of the boosted levels in Renegade Platinum.

??? tip "Alternative: Action Replay Code for Random Wild Pokémon"

    If wild Pokémon levels are a problem, use this AR code to get **almost entirely random Pokémon on each wild encounter**:

    ```
    B2101D40 00000000
    DA000000 000233EC
    D4000000 00000001
    D3000000 00000000
    D7000000 02FFFD00
    92FFFD00 000001ED
    D5000000 00000001
    D0000000 00000000
    B2101D40 00000000
    C0000000 0000000B
    D7000000 000233EC
    DC000000 00000006
    D2000000 00000000
    ```

---

!!! question "Need Help?"

    If you have questions about randomization, check the [FAQ](faq.md) or ask the community!
