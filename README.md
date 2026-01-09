# Dynasty Warriors 2 Visual Guider Info

Dynasty Warriors 2 Visual Guider is a High End GUI Standalone Stage Data modding tool that simplifies modding Stage Data by providing a visual experience for modding. It comes with full modding support of all stages in DW2, the coordinate guider system is built into it and redesigned, a high end mod manager (explained in Features of Visual Guider For Stage Modding), Genetic Algorithm support which i'll cover in Genetic Algorithm Info, Auto pnach generation (review Generate Pnach Section), and many more features.

# Requirements To Use Visual Guider

Python 3 as well as Pillow. Pillow is an imaging library. To install pillow, open a command prompt and type the command `pip install pillow` , then press enter.

The US version of Dynasty Warriors 2.

# Credits

Credit goes to Michael, Passion Wagon, Aurvi, and The Tempest for documentation with Stage/Morale Data. I only take credit for the code and design of Visual Guider. Michael, Passion Wagon, Aurvi, and The Tempest have helped a lot with understanding Stage Data.

# Features of Visual Guider For Stage Modding

Visual Guider properly converts ingame X and Y coordinates to pixel positions on the minimaps, what this means is the X and Y coordinates used in Dynasty Warriors 2 match what you see in Visual Guideer. I scaled the minimaps to the same geometry as the 3D maps so that X/Y to pixel position is a 1 to 1 match. Which means any coordinate you see in Visual Guider is the correct X and Y coordinate that applies to the game. This is meant to make modding stage data significantly easier so that you can visually see where on the map the units will spawn and where they're located.

An optional toggle for morale bars has been added. Allow me to explain. Every squad now has a morale bar, blue for side 1 and red for side 2. It gets filled based on the morale of the force leader. If the force leader has the morale changed then their morale bar as well as any subofficers, troops, etc that serve either the force leader or one of the underlings has their morale bar updated dynamically to match the force leader. The morale bar moves with the squads, that way nothing is lost visually.

You can mod morale data.

There is now a global morale bar, it dynamically updates based on the total morale of side 1 and side 2. Every stage now has a global morale bar in Visual Guider.

You can generate a pnach file of your mod if you prefer pnach instead of file mods.

I have updated every label in Squad Editor to have hover infos, when you hover over a label a description will be displayed explaining what the value is/does. Also, several entries have been updated to have a more user friendly value display such as direction, orders, unit type, ai type, etc. For example, He Jin's Unit Type now displays Commander: 1, to change his or anyone's value that has a string as part of the fields you mod the value that comes after the colon (i.e., i'd change He Jin's Unit Type to NPC Officer by setting the 1 to 4) and that would update the string attached with the value.

I have added a combobox that lists all integer values for character ids, converted to integer so that all you have to do is scroll or filter by typing the name of a unit to see their id value to use.

I also added a Stat Randomizer feature, all units on the map will have their attack, defense, life, and ai level randomly assigned a value if you choose to use Stat Randomizer.

Enhanced auto-balancing (the GA calculates the TCP and spawns new squads for the side it detects is underpowered, it ensures squads spawn in valid regions too), a predict feature (the GA runs a calculation of the current TCP for both sides and gives an estimate of the likely outcome), Stage Generation (the GA creates new stage battles, every time you run Generate Stage it will wipe all current squads and spawn new ones at various locations across the map to create new playable battles for the stages), and a Show Guards toggle which basically allows squads to have their guards displayed as well in the V-like formation you see ingame.

Whenever you move a squad or squads with multi-select, the bodyguards for each squad move with their squad leader and retain the formation. The direction a squad leader faces is also the direction the guards in the formation will face as well. I thought displayable squad guards would be a rad feature to have.

A Multi-Select feature where you can select more than 1 squad, move them around as a group, and either keep their values but update their current coordinates automatically or change the entries that say "<Mixed>" to a value you specify so all units get that value. So this essentially makes batch modding easier, you can either mod squads 1 by 1 or batch squad mod.

Auto populating the entire map with all units on the stage for both sides, you can mod all units in the stage, you can move around the image, zoom in/out, clicking on a marker highlights which unit is selected and displays their stage data, clicking a unit in the listbox takes you directly to the unit you selected, add new units to the stage or delete, dragging the marker of a unit auto updates the current coordinates so you don't have manually type them, selecting a marker/unit from the list or on the map changes the color to green to visually show the current unit selected, filter to find units faster, etc.

Visual Guider also comes with a Mod Creator/Mod Manager as part of it to make it a standalone tool. The new mod manager has collision detection to ensure mods that mod the same data don't conflict as well as displaying info like author of the mod, version of mod, mod description, images of mod, etc. Mods you select in Mod Manager show preview images of the mod too. I custom designed the mod format (think of it like a mini container) that is created with Mod Created to be shareable, as long as you/others have the Visual Guider tool you can apply/disable any mods created with Visual Guider without issue. It's meant to be designed in a way that makes sharing custom stages easy.

There are Genetic Algorithm features as part of Visual Guider which I cover in Genetic Algorithm Info.

# Screenshots of Visual Guider
<img width="1833" height="934" alt="s1" src="https://github.com/user-attachments/assets/c1eae034-b8a5-4c17-8941-2d37e6873e17" />
<img width="1837" height="929" alt="s2" src="https://github.com/user-attachments/assets/d37ec1d3-bc54-4917-9297-f215e570cf66" />
<img width="1840" height="929" alt="s3" src="https://github.com/user-attachments/assets/fff692fe-dd08-4543-a99f-0331aee3cf36" />
<img width="1830" height="934" alt="s4" src="https://github.com/user-attachments/assets/2085a9c0-05e6-45e1-b5dd-ee238c4f5bd0" />
<img width="1832" height="924" alt="s5" src="https://github.com/user-attachments/assets/96e1be59-cc72-4b97-8567-0a1f7f7946d8" />
<img width="1835" height="929" alt="s6" src="https://github.com/user-attachments/assets/cafd77ee-c774-4fc5-ae28-bc2d35e2a275" />
<img width="1834" height="923" alt="s7" src="https://github.com/user-attachments/assets/d5d87b25-70ec-4e2d-848a-bfbe0eefb865" />
<img width="1834" height="927" alt="s8" src="https://github.com/user-attachments/assets/1604eefa-59ad-4516-b5bb-e8d62ab27499" />
<img width="1836" height="929" alt="s9" src="https://github.com/user-attachments/assets/be06fc09-b653-442d-9404-91edbe496101" />
<img width="1834" height="927" alt="s10" src="https://github.com/user-attachments/assets/7a478bcc-3934-41d3-8ef3-35b81692de87" />
<img width="1839" height="926" alt="s11" src="https://github.com/user-attachments/assets/b91fc651-b893-4cc3-b9d1-6d41e7847063" />
<img width="1836" height="925" alt="s12" src="https://github.com/user-attachments/assets/59038ce7-3dbf-41ed-9b66-1c7f42ea687a" />
<img width="1834" height="929" alt="s13" src="https://github.com/user-attachments/assets/d4288599-50e8-42a2-9a9f-5cef16275e31" />
<img width="1834" height="927" alt="s14" src="https://github.com/user-attachments/assets/7aff0d20-c0c4-4893-ab60-7c5239ec2307" />

# Genetic Algorithm Info

I have built a Genetic Algorithm as part of the Visual Guider to enhance modding Dynasty Warriors 2. It includes enhanced auto-balancing (the GA calculates the TCP and spawns new squads for the side it detects is underpowered, it ensures squads spawn in valid regions too), a predict feature (the GA runs a calculation of the current TCP for both sides and gives an estimate of the likely outcome), Stage Generation (the GA creates new stage battles, every time you run Generate Stage it will wipe all current squads and spawn new ones at various locations across the map to create new playable battles for the stages). The GA is an optional feature you can use, you're not required to use it.

The GA isn't perfect though, sometimes a squad may be set to spawn in unplayable zones like water or out of the map. It's easy to fix that though, just click on the marker/squad and place it wherever you want on the map.

# Generate Pnach Section

Visual Guider can automatically generate pnach mods if you prefer to use pnach over file mods. Keep in mind if you personally mod DW2's bin file, it may change the CRC. If you play and find no pnach codes were applied, check to see what the current CRC is of Dynasty Warriors 2 (PCSX2's show console will inform you of the current CRC when playing). By default the pnach filename is 5B665C0B but you can change it to something like 5B665C0B_Custom_Stage, 5B665C0B_Maxed Forces, etc. If DW2 has a different CRC then just rename the filename to the current CRC to apply the pnach mod.

# Mod Manager Section

Mod Manager is only for file mods, it's not used for pnach handling. It automatically creates backups of the stages and morale data to ensure if you disable a mod, the original data is returned.
