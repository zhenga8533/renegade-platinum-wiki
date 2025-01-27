---

## Base Patch

1.  Obtain a Platinum ROM. Ideally this would be a dump of your personal American Platinum cartridge. If looking online, you may see some Platinum ROMs listed with the number 3541 and some with 4997 or 4998. Any of these should be fine. I can’t give a download link here so you’ll have to find it yourself. Make sure the file type of the download is either .nds, or an .nds file included in a compressed archive such as a .7z or .zip. It absolutely should not be an .exe.

2.  Open the DeltaPatcherLite.exe included in the downloaded ZIP file. This is only available for Windows users; Mac users may be able to use the MultiPatch tool which you can find online for a similar result.

3.  Make sure your Platinum ROM is extracted from any archives it came in when downloaded. It must be an .nds file. It should not be a .7z, a .zip, an .exe, or anything else. It must be an .nds file. It should also be 128 MB aka 131,072 KB.

4.  Select your .nds Platinum ROM with the folder button on the top box. Again, it should be .nds. Then for the bottom box, you’ll want to hit the folder button and select the patch that fits with your ROM. If you’re using a 3541 ROM or a cart dump from a cartridge that was obtained near Platinum’s original release, then use “RenegadePlatinum3541.xdelta”. If you’re using a 4997 ROM, 4998 ROM or a cart dump from a cartridge obtained sometime after Platinum’s original release, then use “RenegadePlatinum4997.xdelta”.

    - Your Delta Patcher Lite should look like this after selecting the correct files: ![Delta Patcher Lite](../assets/patching/delta_patcher_lite.jpg)

5.  Hit the cog icon and select “Backup original file” if you don’t want your ROM to be totally replaced with Renegade Platinum. Then, hit “Apply Patch” and the ROM you selected should be transformed into Renegade Platinum (or the patched version ROM will be copied and appended with PATCHED if you chose to “backup original file”).

    - **You should not need to turn off “Checksum validation”. If you do this to force the patch through, it will likely cause crashes when playing.**

    - If you get an error about an XD3_INVALID_INPUT, then the Platinum ROM base and the XDelta patch do not match. Check your ROM again to make sure it’s an .nds file and that you’re using the patch that matches it as dictated by the instructions in 4. If there was no number listed with the ROM and it fails with both patches, you can probably assume that this base won’t work (possibly due to being European or something to that effect).

6.  Assuming the patching finished successfully, you should now have a Renegade
    Platinum ROM ready to go. If you want to add any extras to it (remove non-canon
    Pokémon changes, speed up the game, or change the shiny rate) then go into the
    “Additional Patches” folder inside the “Patches” folder and consult the README file
    there for instructions on how to apply them.

7.  After patching your base ROM and applying additional patches (if any), you can then
    play this Renegade Platinum file using any DS emulator. Options include:

    - DeSmuME for PC. Turn off Bus-Level Timing and turn on “Use Dynamic Recompiler” in Emulator Options to improve speed as in the image below. Please note that the underground will not work unless Bus-Level Timing is turned on. ![Emulation Settings](../assets/patching/emulation_settings.jpg)
    - DraStic for Android. It costs a small fee but is very good. Otherwise you can use another emulator called Free DS.
    - iNDS for iOS.
    - Whatever other options you know of. Flashcards, 3DS custom firmware etc. Any DS emulator that supports the normal Platinum should work!

---

## Additional Patches

To apply these extra patches, you first need a Renegade Platinum ROM, produced by patching a normal Platinum ROM with the appropriate "RenegadePlatinum3541.xdelta" or "RenegadePlatinum4997.xdelta" patch, dependent on your Platinum ROM.

1. Open DeltaPatcherLite.exe.
2. Select your Renegade Platinum ROM as the "original file".
3. Select a patch of your choice as the "XDelta patch".
4. Click on the cog icon that's next to "Apply patch" and click on "Checksum validation", such that it becomes UNCHECKED. Checksum validation is on by default, and will cause you to get XD3_INVALID_INPUT errors if you try to apply multiple additional patches.
5. Click "Apply patch". This should be successful and apply the patch to the Renegade Platinum ROM.
6. To apply another patch, just change what you have selected as "XDelta patch" and hit "Apply patch" again.

Note that you should be able to apply one of these patches on top of Renegade Platinum without needing to remove the checksum validation, so you should get a choice of one of these patches even if you cannot use Delta Patcher Lite and have to use a patcher that can't remove the checksum validation.

### 1/4096 Shiny Rate

Shiny_Rate_1_4096.xdelta: Changes the shiny rate to be 1/4096, equal to the games that are Gen 6 and onwards. By default, the shiny rate is 1/512. This does not affect the chance of the Poké Radar forcing a shiny patch.

### 1/8192 Shiny Rate

Shiny_Rate_1_8192.xdelta: Changes the shiny rate to be 1/8192, equal to the games that are Gen 5 and before. By default, the shiny rate is 1/512. This does not affect the chance of the Poké Radar forcing a shiny patch.

### Classic Version

ClassicVersion.xdelta: Removes any changes to Pokémon that modify their types, stats or abilities to something that isn't in the main series as of Gen 7.

### Speed Up Patch

SpeedUpPatch.xdelta: Changes a few things to speed up the normally sluggish pace of Gen 4 games.

- Instant text. This means you can just mash A to get through dialogue if desired.
- Gauge animation cut. HP and EXP bars won't have the slow increase/decrease they normally do. (Note: This doesn't affect small HP bars so may not be noticeable early.)
- FPS cap removed. Ordinarily locked to 30, the game will now run as fast as it can up to a maximum of 60. Most noticeable in battles. You can see an example of how this works [here](https://www.youtube.com/watch?v=P7P6tjsuNxY){:target="\_blank"}.
