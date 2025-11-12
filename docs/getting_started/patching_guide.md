# Patching Guide

This guide will walk you through patching a clean Pokémon Platinum ROM to create Renegade Platinum.

---

## Prerequisites

!!! warning "Important File Requirements"

    - You need a **clean Platinum ROM** (American version)
    - ROM must be in `.nds` format (may be in `.zip` or `.7z` archive)
    - ROM should be **128 MB (131,072 KB)** in size when extracted
    - **Never use `.exe` files** - these are not legitimate ROM files

!!! info "Obtaining the Patch"

    Download the Renegade Platinum patch from [Drayano's Google Drive](https://t.co/pljSVD0yyG).

---

## Step 1: Obtain the Base ROM

1. Obtain a clean **Pokémon Platinum** ROM
   - Ideally from a dump of your personal cartridge
2. Ensure the file is `.nds` format or contained in a `.zip`/`.7z` archive
3. Extract the ROM if it's in an archive

!!! tip "ROM Version Numbers"

    You may see some Platinum ROMs listed with the number **3541** and some with **4997** or **4998**. Any of these should work fine with the appropriate patch.

---

## Step 2: Choose a Patching Tool

Select the appropriate patching tool for your platform:

=== "Windows"

    **Delta Patcher Lite** (Recommended)

    - Included in the Renegade Platinum download ZIP file
    - Simple graphical interface
    - Continue to Step 3 below

=== "Mac"

    **MultiPatch**

    - Search online for MultiPatch tool
    - Similar functionality to Delta Patcher Lite
    - Follow similar steps to Windows instructions

=== "Web-based (Any Device)"

    **ROM Patcher JS**

    - Visit [https://www.marcrobledo.com/RomPatcher.js/](https://www.marcrobledo.com/RomPatcher.js/)
    - Works on any device with a web browser
    - No installation required

---

## Step 3: Apply the Base Patch

!!! tip "Step-by-Step Instructions (Windows - Delta Patcher Lite)"

    **3.1 - Select the Original File**

    1. Open `DeltaPatcherLite.exe`
    2. Click the folder button next to **"original file"**
    3. Select your clean `.nds` Platinum ROM
        - Must be extracted `.nds` file (131,072 KB)

    **3.2 - Select the Patch File**

    1. Click the folder button next to **"XDelta patch"**
    2. Choose the correct patch for your ROM version:
        - **`RenegadePlatinum3541.xdelta`** - For 3541 ROMs or early cart dumps
        - **`RenegadePlatinum4997.xdelta`** - For 4997/4998 ROMs or later cart dumps

    !!! warning "Choosing the Correct Patch"

        If you don't know which version your ROM is, try one patch. If it fails with an `XD3_INVALID_INPUT` error, try the other patch.

    **3.3 - Patch the ROM**

    1. (Optional) Click the **cog icon** and select **"Backup original file"** if you don't want your ROM replaced
    2. Click **"Apply Patch"** to begin patching
    3. Wait for completion
    4. You now have a Renegade Platinum ROM!

!!! danger "Important - Checksum Validation"

    **Do NOT uncheck "Checksum validation"** for the base patch. If you disable this to force the patch through, it will likely cause crashes when playing.

!!! info "Patch Result"

    Both the 3541 ROM + patch and the 4997 ROM + patch produce the **same** Renegade Platinum ROM, which can then have additional patches applied to it.

---

## Step 4: Apply Additional Patches (Optional)

!!! example "Optional Patch Types"

    - **Classic Version** (`ClassicVersion.xdelta`) - Removes custom Pokémon type/stat/ability changes
    - **Speed Up Patch** (`SpeedUpPatch.xdelta`) - Instant text, no HP/EXP animations, 60 FPS
    - **Shiny Rate Patches** - Change shiny rate to 1/4096 or 1/8192 (default is 1/512)

### Applying Additional Patches

!!! warning "Must Disable Checksum Validation"

    Unlike the base patch, additional patches **require** you to **uncheck "Checksum validation"** to apply multiple patches. This is safe for additional patches.

**Steps:**

1. In Delta Patcher Lite, select your **Renegade Platinum ROM** as the **"original file"**
2. Select an additional patch as the **"XDelta patch"**
3. Click the **cog icon** next to "Apply patch"
4. Click **"Checksum validation"** to **UNCHECK** it
5. Click **"Apply patch"**
6. To apply another patch, change the **"XDelta patch"** selection and click **"Apply patch"** again

!!! tip "Single Additional Patch"

    If you only want to apply **one** additional patch, you should be able to do so without disabling checksum validation.

---

## Available Additional Patches

### Classic Version (`ClassicVersion.xdelta`)

!!! info "What This Does"

    Removes any changes to Pokémon that modify their types, stats, or abilities to something that isn't in the main series as of Gen 7.

    **Use this if you want:**

    - Pokémon stats to match Ultra Sun/Ultra Moon exactly
    - No custom buffs (e.g., no buffed Butterfree or Ledian)
    - No custom types (e.g., no Bug/Dragon Flygon)
    - No custom abilities (e.g., no Technician Weavile)

---

### Speed Up Patch (`SpeedUpPatch.xdelta`)

!!! success "What This Does"

    Changes a few things to speed up the normally sluggish pace of Gen 4 games:

    - **Instant text** - Mash A to get through dialogue instantly
    - **Gauge animation cut** - HP and EXP bars jump to positions instantly (may not be noticeable early with small HP bars)
    - **FPS cap removed** - Game runs up to 60 FPS (normally locked to 30), most noticeable in battles

    [:octicons-arrow-right-24: See example video](https://www.youtube.com/watch?v=P7P6tjsuNxY)

---

### Shiny Rate Patches

=== "1/4096 Shiny Rate"

    **File:** `Shiny_Rate_1_4096.xdelta`

    !!! info "What This Does"

        Changes the shiny rate to **1/4096**, equal to Gen 6 and onwards games.

        - Default Renegade Platinum rate is **1/512**
        - Does not affect Poké Radar shiny patches

=== "1/8192 Shiny Rate"

    **File:** `Shiny_Rate_1_8192.xdelta`

    !!! info "What This Does"

        Changes the shiny rate to **1/8192**, equal to Gen 5 and before (vanilla Platinum rate).

        - Default Renegade Platinum rate is **1/512**
        - Does not affect Poké Radar shiny patches

---

## Step 5: Play the Game

Now you can play Renegade Platinum using a DS emulator!

### Recommended Emulators

=== "PC"

    **DeSmuME**

    - Popular and stable
    - **Performance Tips:**
        - Turn **OFF**: Advanced Bus-Level Timing (Config → Emulation Settings)
        - Turn **ON**: Use Dynamic Recompiler
        - Found in: Config → Emulation Settings → Advanced

    !!! warning "Underground Note"

        The underground will **not work** unless Bus-Level Timing is turned **on**.

    **MelonDS**

    - Modern alternative
    - Generally faster than DeSmuME

=== "Android"

    **DraStic** (Paid)

    - Best performance and compatibility
    - Small one-time fee
    - Very good DS emulator

    **Free Alternatives:**

    - **Free DS** - Free alternative to DraStic
    - Other DS emulators available on Play Store

=== "iOS"

    **iNDS**

    - Free DS emulator for iOS devices

=== "Other Options"

    **Hardware Options:**

    - Flashcards
    - 3DS with custom firmware
    - Any DS emulator that supports normal Platinum should work!

---

## Troubleshooting

!!! danger "Common Issues"

    **`XD3_INVALID_INPUT` error when patching**

    - The Platinum ROM base and XDelta patch do not match
    - Check your ROM is `.nds` format (128 MB / 131,072 KB)
    - Try the **other** base patch (3541 vs 4997)
    - If no number was listed with the ROM and it fails with both patches, the ROM base won't work (possibly European or modified)

    **Game crashes or freezes at first rival battle**

    - Wrong ROM base detected
    - Try the **other** base patch (3541 vs 4997)
    - Ensure you did **not** disable checksum validation for the base patch

    **Can't apply multiple additional patches (`XD3_INVALID_INPUT`)**

    - You must **uncheck "Checksum validation"** when applying additional patches
    - See Step 4 above for detailed instructions

!!! tip "Read the README Files"

    The download includes README files in each patch folder. If you have problems, make sure you've read these first!

---

!!! success "Ready to Play!"

    Once patching is complete, you're ready to start your Renegade Platinum adventure! Check out the [FAQ](faq.md) if you have any questions.
