# Dynasty Warriors 2 Visual Guider Info

Dynasty Warriors 2 Visual Guider is a High End GUI Standalone Stage Data modding tool that simplifies modding Stage Data by providing a visual experience for modding. It comes with full modding support of all stages in DW2, the coordinate guider system is built into it and redesigned, a high end mod manager (explained in Features of Visual Guider For Stage Modding), Genetic Algorithm support which i'll cover in Genetic Algorithm Info, and many more features. Visual Guider isn't ready to release yet but when it is, this repository will have it.

# Features of Visual Guider For Stage Modding

Visual Guider properly converts ingame X and Y coordinates to pixel positions on the minimaps, what this means is the X and Y coordinates used in Dynasty Warriors 2 match what you see in Visual Guideer. I scaled the minimaps to the same geometry as the 3D maps so that X/Y to pixel position is a 1 to 1 match. Which means any coordinate you see in Visual Guider is the correct X and Y coordinate that applies to the game. This is meant to make modding stage data significantly easier so that you can visually see where on the map the units will spawn and where they're located.

An optional toggle for morale bars has been added. Allow me to explain. Every squad now has a morale bar, blue for side 1 and red for side 2. It gets filled based on the morale of the force leader. If the force leader has the morale changed then their morale bar as well as any subofficers, troops, etc that serve either the force leader or one of the underlings has their morale bar updated dynamically to match the force leader. The morale bar moves with the squads, that way nothing is lost visually.

You can mod morale data.

There is now a global morale bar, it dynamically updates based on the total morale of side 1 and side 2. Every stage now has a global morale bar in Visual Guider.

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
<img width="1743" height="923" alt="s1" src="https://github.com/user-attachments/assets/4ed9b25f-425e-4136-b225-aef4b03d8a0c" />
<img width="1743" height="929" alt="s2" src="https://github.com/user-attachments/assets/a45594f6-6441-428e-b04b-65c9367dc16d" />
<img width="1744" height="923" alt="s3" src="https://github.com/user-attachments/assets/dbe216b9-effd-46c9-a3e2-9219ee72b1ca" />
<img width="1744" height="926" alt="s4" src="https://github.com/user-attachments/assets/ed9f1647-6ca8-48f4-847b-66cf55829a9f" />
<img width="1744" height="931" alt="s5" src="https://github.com/user-attachments/assets/aae34dfd-b4ea-4bbf-a4cb-7a7977bc0615" />
<img width="1746" height="924" alt="s6" src="https://github.com/user-attachments/assets/92362ca5-c3c0-408c-b170-586460634085" />
<img width="1747" height="929" alt="s7" src="https://github.com/user-attachments/assets/506313a7-16d7-4941-a811-ef0588602dd6" />
<img width="1743" height="925" alt="s8" src="https://github.com/user-attachments/assets/c42dbdd6-f0e7-423c-9926-05bf62053014" />
<img width="1749" height="929" alt="s9" src="https://github.com/user-attachments/assets/79d64460-d26a-4e01-85b8-487c02e20efd" />
<img width="1746" height="925" alt="s10" src="https://github.com/user-attachments/assets/38dfd1f1-3c9f-4257-be18-86949237068e" />
<img width="1748" height="925" alt="s11" src="https://github.com/user-attachments/assets/07dd13eb-f1ba-43b2-bb72-6a9c15016969" />
<img width="1746" height="926" alt="s12" src="https://github.com/user-attachments/assets/955442db-effb-45a3-a5f4-8960e60da54b" />
<img width="1748" height="925" alt="s13" src="https://github.com/user-attachments/assets/b6bca47b-8d24-40e1-a2fe-1fa7c3016219" />
<img width="1747" height="930" alt="s14" src="https://github.com/user-attachments/assets/486ef7d1-f158-41dd-87c7-2fe37e61d7d7" />
<img width="1746" height="926" alt="s15" src="https://github.com/user-attachments/assets/ce630add-09d4-4c65-8845-7556c12c2272" />

# Genetic Algorithm Info

I have built a Genetic Algorithm as part of the Visual Guider to enhance modding Dynasty Warriors 2. It includes enhanced auto-balancing (the GA calculates the TCP and spawns new squads for the side it detects is underpowered, it ensures squads spawn in valid regions too), a predict feature (the GA runs a calculation of the current TCP for both sides and gives an estimate of the likely outcome), Stage Generation (the GA creates new stage battles, every time you run Generate Stage it will wipe all current squads and spawn new ones at various locations across the map to create new playable battles for the stages). The GA is an optional feature you can use, you're not required to use it.
