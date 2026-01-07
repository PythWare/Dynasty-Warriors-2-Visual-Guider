# Dynasty Warriors 2 Visual Guider Info

Dynasty Warriors 2 Visual Guider is a High End GUI Standalone Stage Data modding tool that simplifies modding Stage Data by providing a visual experience for modding. It comes with full modding support of all stages in DW2, the coordinate guider system is built into it and redesigned, a high end mod manager that includes collision detection between mods as well as preview images for each mod, Genetic Algorithm support which i'll cover in Genetic Algorithm Info, and many more features. Visual Guider isn't ready to release yet but when it is, this repository will have it.

# Features of Visual Guider For Stage Modding

Visual Guider properly converts ingame X and Y coordinates to pixel positions on the minimaps, what this means is the X and Y coordinates used in Dynasty Warriors 2 match what you see in Visual Guideer. I scaled the minimaps to the same geometry as the 3D maps so that X/Y to pixel position is a 1 to 1 match. Which means any coordinate you see in Visual Guider is the correct X and Y coordinate that applies to the game. This is meant to make modding stage data significantly easier so that you can visually see where on the map the units will spawn and where they're located. A Show Guards toggle is also added which basically allows squads to have their guards displayed as well in the V-like formation you see ingame. Whenever you move a squad or squads with multi-select, the bodyguards for each squad move with their squad leader and retain the formation. The direction a squad leader faces is also the direction the guards in the formation will face as well. I thought displayable squad guards would be a rad feature to have, seeing guards of each squad displayed with their squad leader is so rad to me.

The list of other features are:

A Multi-Select feature where you can select more than 1 squad, move them around as a group, and either keep their values but update their current coordinates automatically or change the entries that say "<Mixed>" to a value you specify so all units get that value. This essentially makes batch modding easier, you can either mod squads 1 by 1 or batch squad mod. There's also auto populating the entire map with all units on the stage for both sides, you can mod all units in the stage, you can move around the image, zoom in/out, clicking on a marker highlights which unit is selected and displays their stage data, clicking a unit in the listbox takes you directly to the unit you selected, add new units to the stage or delete, dragging the marker of a unit auto updates the current coordinates so you don't have manually type them, selecting a marker/unit from the list or on the map changes the color to green to visually show the current unit selected, filter to find units faster, etc.

There are Genetic Algorithm features as part of Visual Guider which I cover in Genetic Algorithm Info.

# Screenshots of Visual Guider Version 0.8
<img width="1528" height="855" alt="u42" src="https://github.com/user-attachments/assets/0de25cc5-5b94-4c01-bd00-36e07c7ef5cf" />
<img width="1524" height="852" alt="u43" src="https://github.com/user-attachments/assets/78572b9d-b589-4d89-8d58-44b13321fe30" />
<img width="1526" height="850" alt="u44" src="https://github.com/user-attachments/assets/19582c9a-755d-4392-a91d-4c0040103f4a" />
<img width="1527" height="856" alt="u45" src="https://github.com/user-attachments/assets/fffc1c46-20c9-49fb-800d-32a14ea8276c" />
<img width="1523" height="855" alt="u46" src="https://github.com/user-attachments/assets/fdc6f973-b688-4153-afb0-386927c7b896" />
<img width="1526" height="848" alt="u47" src="https://github.com/user-attachments/assets/2a3d584c-3fa8-40b6-9aef-2e467c096dad" />
<img width="1525" height="851" alt="u48" src="https://github.com/user-attachments/assets/63eb8b72-f3f8-4ea1-bd34-37249cdd98ab" />
<img width="1525" height="850" alt="u49" src="https://github.com/user-attachments/assets/889d6dd2-e57c-4e02-bf9d-d8da99eda5f1" />
<img width="1526" height="850" alt="u50" src="https://github.com/user-attachments/assets/f8a3c1ad-bfdd-4c0b-baa9-6bba27c6207a" />
<img width="1523" height="848" alt="u51" src="https://github.com/user-attachments/assets/5109a180-77ae-4b28-97a5-b729df411ea0" />
<img width="1525" height="853" alt="u52" src="https://github.com/user-attachments/assets/d9994621-ed66-4bc7-83de-6002d7842ba6" />
<img width="1527" height="858" alt="u53" src="https://github.com/user-attachments/assets/edc0f944-cbb6-420e-afec-f184fb787453" />
<img width="1528" height="855" alt="u54" src="https://github.com/user-attachments/assets/69a97da3-4a4b-4ba7-bd20-b8bf1ec2975e" />
<img width="1663" height="883" alt="u55" src="https://github.com/user-attachments/assets/b090b5c1-2087-42cc-a54f-e87d9f7ef753" />
<img width="1525" height="858" alt="u56" src="https://github.com/user-attachments/assets/798094a0-d1f7-4196-a7f3-93e3645b733e" />


# Genetic Algorithm Info

I have built a Genetic Algorithm as part of the Visual Guider to enhance modding Dynasty Warriors 2. It includes enhanced auto-balancing (the GA calculates the TCP and spawns new squads for the side it detects is underpowered, it ensures squads spawn in valid regions too), a predict feature (the GA runs a calculation of the current TCP for both sides and gives an estimate of the likely outcome), Stage Generation (the GA creates new stage battles, every time you run Generate Stage it will wipe all current squads and spawn new ones at various locations across the map to create new playable battles for the stages). The GA is an optional feature you can use, you're not required to use it.
