# Frequently Asked Questions

---

## Patching Issues

!!! question "Why is the patching not working?"

    - Make sure you're using the **correct patch** for the Platinum ROM you've obtained
    - If using a dump from your own American cartridge:
        - Copies purchased near Platinum's **original release** → Use **3541 patch**
        - Otherwise → Use **4997 patch**
    - Make sure you're trying to apply the patch to an **`.nds` file** (128 MB)
        - Should **not** still be compressed in `.zip` or `.7z`
        - Definitely should **not** be an `.exe`!
    - The patch to turn Platinum into Renegade Platinum should work **without** unchecking "Checksum validation"
    - If you uncheck it to force the patch through, it'll likely freeze in battles
    - **Mac users:** Use a program called **MultiPatch** instead (Delta Patcher Lite won't work)
    - **Mobile users:** Patching is unreliable on mobile phones; use a PC then transfer the patched ROM

!!! danger "Game frozen when trying to start the first rival battle?"

    This means you've likely used the **wrong ROM base**.

    **Solutions:**

    - Try the patch for the **other ROM base** (3541 vs 4997)
    - If you forced the patch through by unchecking "checksum validation", this will also cause this issue
    - With the **correct ROM base**, you won't need to uncheck "checksum validation"

---

## Updating Renegade Platinum

!!! question "How can I update my Renegade Platinum to a newer version?"

    Renegade Platinum save files are **compatible between versions**, so updating is possible!

    !!! warning "Important Notes"

        - Battery (normal) saves done by the **save menu in-game** will work
        - **Save states will NOT work** if you change the ROM version!
        - Patches must always be applied to a **vanilla Platinum ROM**

    First, get an `.nds` copy of the newest Renegade Platinum.

### Method 1: Export/Import Battery Saves (DeSmuME)

!!! tip "DeSmuME Instructions"

    1. Load your old Renegade Platinum ROM with your current save
    2. Go to **File → Export Backup Memory** to produce a `.sav` file
    3. Open the new ROM
    4. Go to **File → Import Backup Memory** and select the `.sav` you just exported
    5. Your save file should now be active!

### Method 2: The Filename Switch Method

!!! tip "Filename Switch Instructions"

    1. Rename the new version ROM to have the **same filename** as your old version
        - Example: Old is `RenegadePlatinumX.nds`, new is `RenegadePlatinumY.nds`
        - Rename new from `RenegadePlatinumY.nds` → `RenegadePlatinumX.nds`
    2. Replace your old ROM with the new ROM
    3. Boot up the new ROM on the emulator
    4. Your save file should be there!

!!! info "Updating from v1.0.0-v1.0.3"

    If updating from **v1.0.0, v1.0.1, v1.0.2, or v1.0.3** to any newer version while keeping your save file:

    You **must** talk to the NPC found in any of the Pokémon Centers in **Jubilife, Eterna, Hearthome, or Veilstone** to get everything in place in your save.

---

## Randomization

!!! question "Can I randomize Renegade Platinum?"

    **No**, this is not possible via the Universal Pokémon Randomizer.

    **Why not?**

    - Expanded files mean the internal file locations are different from normal
    - The Universal Pokémon Randomizer is unable to handle this
    - This is impossible to add support for

    !!! tip "Manual Randomization Option"

        You **can** do it manually by transplanting files across from a randomized ordinary Platinum.

        See the **RandomiseInstructions.txt** document (or the [Randomise Guide](randomise_guide.md)) for instructions.

---

## Shiny Pokémon

!!! question "Does the boost to the shiny rate affect the Poké Radar shiny patches?"

    **No**, the Poké Radar works off its own RNG system that will force a shiny patch when it rolls the correct number.

    The shiny rate change in this game **doesn't affect** the Poké Radar.

!!! question "Can I get [Pokémon name here] as a shiny?"

    **Yes!** All Pokémon are available as shiny at whatever rate the version you're playing has:

    - **1/512** with shiny boost (default)
    - **1/4096** if you applied the Gen 6+ shiny rate patch
    - **1/8192** if you applied the vanilla shiny rate patch

    !!! warning "Soft Resetting for Shinies"

        You need to **soft reset** to try to get shinies for static encounters.

        **Save states don't reroll the RNG**, so you'll get the same Pokémon every time.

---

## Technical Issues

!!! question "I'm seeing graphical distortion when walking in grass sometimes. Is this a bug?"

    This is a bug, but **not with the hack** - it's a problem with the **emulator** (specifically DeSmuME).

    !!! info "Don't Worry!"

        - The graphical distortion is **harmless**
        - It will go away when the screen is refreshed
        - This problem also happens with the **original Platinum**

---

## Gameplay Questions

!!! question "I finished the Galactic events in Eterna City and am now stuck. What do I do?"

    Go to the **Bike Shop in Eterna City** and talk to the owner.

    After this, you should be able to progress past **Route 206**.

!!! question "Why can't I get into Canalave City? Where am I meant to go?"

    You must now visit **Pal Park** before you can continue into Canalave City.

    !!! tip "What to Do at Pal Park"

        Be sure to talk to **all of the NPCs** at Pal Park. You're after a **specific item** to get past the guard blocking you!

---

## ROM Acquisition

!!! question "Where can I find the ROM base for Renegade Platinum?"

    Can't give you a link here, unfortunately. But they do exist on the Internet.

    !!! info "Requirements"

        - You need a **clean Platinum ROM** (American version)
        - Should be **128 MB (131,072 KB)** in `.nds` format
        - See the [Patching Guide](patching_guide.md) for more details
