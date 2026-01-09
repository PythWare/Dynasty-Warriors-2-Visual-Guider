import os, io, struct, shutil, json, random, math, copy, colorsys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configs and data maps

LILAC = "#C8A2C8"
LILAC_LIGHT = "#E6E6FA"
CYAN_BTN = "#00FFFF"
GOLD_BTN = "#FFD700"
ORANGE_BTN = "#FFA500"
DW2_MODS_DIR = "DW2_Mods"
BACKUP_DIR = "Backups"
STATE_FILE = "mod_state.json"

MAP_FILES = [
    "YellowTurban.png", "HuLaoGate.png", "GuanDu.png", "ChangBan.png", 
    "ChiBi.png", "HeFei.png", "YiLing1.png", "WuZhangPlains.png"
]

STAGE_EXTENSIONS = [
    ".DW2YTR", ".DW2HLG", ".DW2GD", ".DW2CBan", 
    ".DW2CBi", ".DW2HF", ".DW2YL", ".DW2WZP"
]

STAGE_NAMES = [
    "Yellow Turban Rebellion", "Hu Lao Gate", "Guan Du", "Chang Ban",
    "Chi Bi", "He Fei", "Yi Ling", "Wu Zhang Plains"
]

# Format: Stage Name: { Side_ID: (File_Offset, Count_of_Chunks) }
STAGE_MORALE_DATA = {
    "Yellow Turban Rebellion": {
        1: (0x160D5F8A, 11), 
        2: (0x160D5FA2, 11)
    },
    "Hu Lao Gate": {
        1: (0x160D609A, 11), 
        2: (0x160D60B2, 11)
    },
    "Guan Du": {
        1: (0x160D61AA, 11), 
        2: (0x160D61C2, 11)
    },
    "Chang Ban": {
        1: (0x160D62BA, 11), 
        2: (0x160D62D2, 11)
    },
    "Chi Bi": {
        1: (0x160D63CA, 11), 
        2: (0x160D63E2, 11)
    },
    "He Fei": {
        1: (0x160D660A, 11), 
        2: (0x160D6622, 11)
    },
    "Yi Ling": {
        1: (0x160D671A, 11), 
        2: (0x160D6732, 11)
    },
    "Wu Zhang Plains": {
        1: (0x160D682A, 11), 
        2: (0x160D6842, 11)
    }
}

# Zone Schemas for procedural generation
STAGES_ZONES = {
    "Yellow Turban Rebellion": {
        "Side 1": [
            {"name": "Top Left", "rect": (51, 551, 157, 631)},
            {"name": "Top Left Mid", "rect": (79, 487, 201, 558)},
            {"name": "Top Left Mid Right", "rect": (151, 429, 286, 534)},
            {"name": "Center", "rect": (307, 209, 521, 529)},
            {"name": "Bottom Left 1", "rect": (56, 120, 229, 192)},
            {"name": "Bottom Left 2", "rect": (187, 199, 286, 342)},
            {"name": "Bottom Right", "rect": (318, 100, 528, 187)}
        ],
        "Side 2": [
            {"name": "Top Left", "rect": (51, 551, 157, 631)},
            {"name": "Top Left Mid", "rect": (79, 487, 201, 558)},
            {"name": "Top Left Mid Right", "rect": (151, 429, 286, 534)},
            {"name": "Center", "rect": (307, 209, 521, 529)},
            {"name": "Top Right 1", "rect": (466, 666, 540, 689)},
            {"name": "Top Right 2", "rect": (633, 635, 743, 733)},
            {"name": "Top Right 3", "rect": (713, 561, 740, 594)},
            {"name": "Top Right 4", "rect": (646, 558, 690, 571)}
        ]
},
	"Hu Lao Gate": {
        "Side 1": [
            {"name": "Top Gate 1", "rect": (557, 731, 575, 750)},
            {"name": "Top Gate 2", "rect": (610, 722, 638, 750)},
            {"name": "Top Near Gate 1", "rect": (498, 720, 541, 734)},
            {"name": "Top Near Gate 2", "rect": (545, 693, 594, 729)},
            {"name": "Top Near Gate 3", "rect": (625, 707, 658, 737)},
            {"name": "Top Right 1", "rect": (667, 629, 721, 669)},
            {"name": "Orig Shu Area 1", "rect": (631, 595, 678, 642)},
	    {"name": "Orig Shu Area 2", "rect": (588, 520, 657, 584)},
            {"name": "Orig Wei Area 1", "rect": (715, 466, 730, 524)},
            {"name": "Orig Wei Area 2", "rect": (696, 378, 731, 412)},
            {"name": "Orig Wei Area Near Gate", "rect": (669, 339, 715, 375)},
            {"name": "Orig Wu Gate", "rect": (259, 732, 284, 749)},
            {"name": "Orig Wu Area 1", "rect": (242, 715, 328, 734)},
            {"name": "Orig Wu Area 2", "rect": (254, 669, 274, 710)},
	    {"name": "Contested 1", "rect": (366, 602, 416, 640)},
            {"name": "Contested 2", "rect": (417, 583, 435, 619)},
            {"name": "Contested 3", "rect": (159, 612, 216, 630)}
        ],
        "Side 2": [
            {"name": "Bottom Castle", "rect": (135, 66, 230, 99)},
            {"name": "Bottom Castle Gates", "rect": (166, 50, 237, 68)},
            {"name": "Bottom Castle Walls", "rect": (143, 105, 223, 116)},
            {"name": "front of Castle 1", "rect": (125, 120, 220, 157)},
            {"name": "Orig Lu Bu Area", "rect": (141, 193, 226, 216)},
            {"name": "Lu Bu Gate Area", "rect": (110, 215, 145, 235)},
            {"name": "Zhang Liao Area 1", "rect": (131, 228, 165, 286)},
	    {"name": "Zhang Liao Area 2", "rect": (135, 266, 207, 334)},
            {"name": "Behind Mid Castle", "rect": (240, 292, 301, 314)},
            {"name": "Mid Castle Gate 1", "rect": (356, 368, 398, 380)},
            {"name": "Mid Castle Tent Area", "rect": (286, 373, 358, 393)},
            {"name": "Mid Castle Walls", "rect": (284, 419, 359, 435)},
            {"name": "Center Area", "rect": (312, 489, 357, 507)},
            {"name": "Shu Gate", "rect": (565, 422, 589, 483)},
	    {"name": "Wu Gate", "rect": (129, 559, 187, 588)},
            {"name": "Wei Gate 1", "rect": (506, 119, 538, 170)},
            {"name": "Wei Gate 2", "rect": (361, 238, 394, 284)},
            {"name": "Contested 1", "rect": (366, 602, 416, 640)},
            {"name": "Contested 2", "rect": (417, 583, 435, 619)},
            {"name": "Contested 3", "rect": (159, 612, 216, 630)},
            {"name": "Contested 4", "rect": (617, 304, 671, 349)}
        ]
    },
    "Guan Du": {
        "Side 1": [
            {"name": "Cao Castle", "rect": (550, 108, 687, 242)},
            {"name": "Cao Castle Behind", "rect": (706, 124, 737, 258)},
            {"name": "Cao Castle Top", "rect": (621, 263, 740, 282)},
            {"name": "Bottom Center 1", "rect": (306, 204, 535, 239)},
            {"name": "Bottom Center 2", "rect": (307, 149, 539, 186)},
            {"name": "Bottom Center 3", "rect": (510, 72, 629, 92)},
            {"name": "Bottom Right", "rect": (318, 100, 528, 187)},
	    {"name": "Cao Mid 1", "rect": (437, 409, 679, 437)},
            {"name": "Cao Mid 2", "rect": (622, 457, 675, 517)},
            {"name": "Wei Top Castle", "rect": (600, 601, 695, 695)},
            {"name": "Wei Top Mid", "rect": (357, 614, 451, 691)},
            {"name": "Contested 1", "rect": (532, 626, 586, 739)},
            {"name": "Contested 2", "rect": (411, 503, 480, 541)},
            {"name": "Contested 3", "rect": (402, 466, 485, 488)}
],
        "Side 2": [
            {"name": "Yuan Castle", "rect": (105, 107, 301, 252)},
            {"name": "Yuan Castle Left", "rect": (67, 66, 97, 183)},
            {"name": "Yuan Castle Below", "rect": (98, 70, 304, 97)},
            {"name": "Yuan Castle Right", "rect": (306, 67, 341, 240)},
            {"name": "Yuan Castle Top", "rect": (170, 261, 287, 342)},
            {"name": "Yuan Mid", "rect": (339, 444, 383, 520)},
            {"name": "Yuan Mid Left", "rect": (62, 366, 223, 475)},
            {"name": "Yuan Top Left", "rect": (172, 693, 280, 740)},
	    {"name": "Yuan Top Under", "rect": (105, 603, 279, 632)},
            {"name": "Yuan Top Over", "rect": (255, 688, 344, 740)},
	    {"name": "Contested 1", "rect": (532, 626, 586, 739)},
            {"name": "Contested 2", "rect": (411, 503, 480, 541)},
            {"name": "Contested 3", "rect": (402, 466, 485, 488)}
        ]
    },
    "Chang Ban": {
        "Side 1": [
            {"name": "Top Right 1", "rect": (636, 623, 746, 711)},
            {"name": "Top Right 2", "rect": (564, 686, 652, 747)},
            {"name": "Contested 1", "rect": (454, 656, 570, 730)},
            {"name": "Bottom Right 1", "rect": (431, 233, 541, 337)},
            {"name": "Bottom Right 2", "rect": (449, 271, 547, 377)},
            {"name": "Bottom Left 1", "rect": (212, 217, 381, 345)},
            {"name": "Mid Left", "rect": (157, 411, 195, 516)},
	    {"name": "Contested 2", "rect": (160, 565, 220, 621)},
	    {"name": "Contested Right", "rect": (513, 582, 533, 648)},
            {"name": "Contested Left 1", "rect": (70, 52, 88, 199)},
	    {"name": "Contested Left 2", "rect": (70, 52, 88, 199)}
],
        "Side 2": [
            {"name": "Top Left", "rect": (165, 666, 187, 729)},
            {"name": "Top Left Mid", "rect": (60, 462, 145, 494)},
            {"name": "Mid", "rect": (313, 357, 364, 430)},
            {"name": "Bottom Right", "rect": (608, 210, 643, 264)},
            {"name": "Right 1", "rect": (611, 281, 639, 315)},
            {"name": "Right 2", "rect": (672, 339, 689, 389)},
            {"name": "Right 3", "rect": (610, 378, 688, 389)},
            {"name": "Right 4", "rect": (601, 413, 692, 439)},
	    {"name": "Right 5", "rect": (625, 500, 682, 523)},
            {"name": "Right 6", "rect": (527, 561, 678, 586)},
            {"name": "Contested Right", "rect": (513, 582, 533, 648)},
            {"name": "Right 4", "rect": (601, 413, 692, 439)},
            {"name": "Contested Left 1", "rect": (70, 52, 88, 199)},
	    {"name": "Contested Left 2", "rect": (70, 52, 88, 199)}
        ]
    },
    "Chi Bi": {
        "Side 1": [
            {"name": "South left", "rect": (65, 115, 171, 167)},
            {"name": "South Half", "rect": (66, 164, 585, 193)},
            {"name": "South Camp", "rect": (266, 113, 367, 153)},
            {"name": "South Right", "rect": (577, 110, 725, 138)},
            {"name": "South Ships", "rect": (207, 177, 700, 293)},
            {"name": "Contested 1", "rect": (594, 355, 735, 631)}
],
        "Side 2": [
            {"name": "Cao Zone", "rect": (255, 407, 408, 685)},
            {"name": "Cao L1 Fleet", "rect": (107, 258, 143, 642)},
            {"name": "Cao L2 Fleet", "rect": (156, 408, 243, 588)},
            {"name": "Cao B1 Fleet", "rect": (256, 408, 394, 442)},
            {"name": "Cao R1 Fleet", "rect": (406, 358, 493, 588)},
            {"name": "Cao R2 Fleet", "rect": (558, 458, 642, 540)},
	    {"name": "Cao TR Def", "rect": (584, 552, 704, 630)}
        ]
    },
    	"He Fei": {
        "Side 1": [
            {"name": "B Left", "rect": (57, 66, 270, 395)},
            {"name": "T Left 1", "rect": (121, 653, 166, 694)},
            {"name": "T Left 2", "rect": (114, 414, 172, 476)},
            {"name": "T Left 3", "rect": (257, 367, 341, 505)},
            {"name": "B Right 1", "rect": (396, 127, 636, 175)},
            {"name": "B Right 2", "rect": (673, 168, 750, 191)},
            {"name": "Contested 1", "rect": (301, 84, 393, 239)},
	    {"name": "Contested 2", "rect": (552, 377, 694, 480)},
	    {"name": "Contested 3", "rect": (269, 655, 476, 714)},
            {"name": "Contested 4", "rect": (361, 314, 441, 448)}
],
        "Side 2": [
            {"name": "T Right", "rect": (501, 503, 750, 749)},
            {"name": "T R2", "rect": (367, 563, 477, 640)},
            {"name": "T R3", "rect": (462, 376, 543, 476)},
            {"name": "T R4", "rect": (527, 211, 581, 321)},
            {"name": "Contested 1", "rect": (301, 84, 393, 239)},
	    {"name": "Contested 2", "rect": (552, 377, 694, 480)},
	    {"name": "Contested 3", "rect": (269, 655, 476, 714)},
            {"name": "Contested 4", "rect": (361, 314, 441, 448)}
        ]
    },
    "Yi Ling": {
        "Side 1": [
	    {"name": "Base", "rect": (568, 43, 733, 187)},
            {"name": "C1", "rect": (392, 360, 644, 558)},
            {"name": "C2", "rect": (350, 102, 445, 354)},
            {"name": "FR1", "rect": (504, 297, 800, 548)},
            {"name": "Boats", "rect": (618, 590, 784, 698)},
            {"name": "Contested 1", "rect": (220, 640, 456, 754)},
            {"name": "Contested 2", "rect": (648, 473, 762, 603)},
            {"name": "Contested 3", "rect": (414, 85, 592, 280)}
],
        "Side 2": [
            {"name": "Top Left", "rect": (67, 629, 229, 733)},
            {"name": "Top Left Mid", "rect": (42, 402, 247, 617)},
            {"name": "Top Left Mid Right", "rect": (226, 492, 409, 629)},
            {"name": "B Left", "rect": (185, 100, 342, 402)},
            {"name": "Contested 1", "rect": (220, 640, 456, 754)},
            {"name": "Contested 2", "rect": (648, 473, 762, 603)},
            {"name": "Contested 3", "rect": (414, 85, 592, 280)}
        ]
    },
    	"Wu Zhang Plains": {
        "Side 1": [
            {"name": "BL", "rect": (126, 157, 196, 353)},
            {"name": "Base Area", "rect": (208, 62, 629, 395)},
            {"name": "BR 1", "rect": (555, 274, 725, 360)},
            {"name": "BR 2", "rect": (604, 157, 684, 266)},
            {"name": "Contested 1", "rect": (576, 417, 746, 538)},
            {"name": "Contested 2", "rect": (592, 659, 691, 734)}
],
        "Side 2": [
            {"name": "Base", "rect": (314, 677, 438, 738)},
            {"name": "Top Left", "rect": (45, 506, 195, 690)},
            {"name": "Top Left Mid", "rect": (334, 517, 417, 538)},
            {"name": "Top Left Mid Right", "rect": (458, 511, 531, 532)},
            {"name": "Center", "rect": (353, 477, 400, 494)},
            {"name": "M Right 1", "rect": (466, 666, 540, 689)}
        ]
    }
}

# Offsets in bin file where stage data is held, each stage has 8 offsets due to sector data
STAGE_OFFSETS = [
    [0x24DD6DD8, 0x24DD7708, 0x24DD8038, 0x24DD8968, 0x24DD9298, 0x24DD9BC8, 0x24DDA4F8, 0x24DDAE28], 
    [0x24DDF7A8, 0x24DE00D8, 0x24DE0A08, 0x24DE1338, 0x24DE1C68, 0x24DE2598, 0x24DE2EC8, 0x24DE37F8], 
    [0x24DE8178, 0x24DE8AA8, 0x24DE93D8, 0x24DE9D08, 0x24DEA638, 0x24DEAF68, 0x24DEB898, 0x24DEC1C8], 
    [0x24DF0B48, 0x24DF1478, 0x24DF1DA8, 0x24DF26D8, 0x24DF3008, 0x24DF3938, 0x24DF4268, 0x24DF4B98], 
    [0x24DF9518, 0x24DF9E48, 0x24DFA778, 0x24DFB0A8, 0x24DFB9D8, 0x24DFC308, 0x24DFCC38, 0x24DFD568], 
    [0x24E01EE8, 0x24E02818, 0x24E03148, 0x24E03A78, 0x24E043A8, 0x24E04CD8, 0x24E05608, 0x24E05F38], 
    [0x24E0A8B8, 0x24E0B1E8, 0x24E0BB18, 0x24E0C448, 0x24E0CD78, 0x24E0D6A8, 0x24E0DFD8, 0x24E0E908], 
    [0x24E13288, 0x24E13BB8, 0x24E144E8, 0x24E14E18, 0x24E15748, 0x24E16078, 0x24E169A8, 0x24E172D8]
]

# String Name for user in Squad Editor + Integer Value of Direction
UNIT_DIR = [
    ("North", 0), ("North East", 1), ("East", 2), ("South East", 3),
    ("South", 4), ("South West", 5), ("West", 6), ("North West", 7)
]

# String Name for user in Squad Editor + Integer Value of Unit Types
UNIT_TYPES = [
    ("Player", 0), ("Commander", 1), ("General", 2), ("Playable Officer", 3),
    ("NPC Officer", 4), ("Gate C./Troops", 5), ("Troops (respawns)", 6)
]

# String Name for user in Squad Editor + Integer Value of AI Types
AI_TYPES = [
    ("Ranged", 2), ("Cavalry", 4)
]

# String Name for user in Squad Editor + Integer Value of Orders
ORDER_TYPES = [
    ("Attack Enemy", 1), ("Follow Ally", 3), ("Hold Position", 4)
]

UNIT_DATA_FIELDS = [
    ("Pos X", "x", 0, 2), ("Pos Y", "y", 2, 2), ("Direction", "dir", 4, 1),
    ("Pathing", "path", 5, 1), ("Gate Mode", "gate_mode", 6, 1), ("Life", "life", 8, 2),
    ("Leader ID", "leader", 10, 1), ("Guard ID", "guard_id", 11, 1), ("Attack", "atk", 12, 1),
    ("Defense", "def", 13, 1), ("Guard Count(9 is max)", "guard_cnt", 14, 1), ("Serves Slot", "own_slot", 15, 1),
    ("Unit Type", "type", 16, 1), ("AI Type", "ai_type", 17, 1), ("Orders", "orders", 18, 1),
    ("Hidden", "hidden", 19, 1), ("Order Tgt", "target", 21, 1), ("Item Drop", "drop", 22, 1),
    ("AI Level", "ai_lvl", 23, 1), ("Delay", "delay", 24, 2), ("Kill Pts", "points", 26, 2),
]

UNIT_LIMITS = {
    "x": 800, "y": 800, "dir": 255, "path": 255, "gate_mode": 255, "life": 3000,
    "leader": 255, "guard_id": 255, "atk": 255, "def": 255, "guard_cnt": 9, "own_slot": 511,
    "type": 255, "ai_type": 255, "orders": 255, "hidden": 255, "target": 511, "drop": 255,
    "ai_lvl": 255, "delay": 65535, "points": 65535,
}

UNIT_NAMES = {
    0: "Zhao Yun", 1: "Guan Yu", 2: "Zhang Fei", 3: "Xiahou Dun", 4: "Dian Wei", 5: "Xu Zhu",
    6: "Zhou Yu", 7: "Lu Xun", 8: "Taishi Ci", 9: "Diao Chan", 10: "Zhuge Liang", 11: "Cao Cao",
    12: "Lu Bu", 13: "Sun Shang Xiang", 14: "Liu Bei", 15: "Sun Jian", 16: "Sun Quan", 17: "Dong Zhuo",
    18: "Yuan Shao", 19: "Ma Chao", 20: "Huang Zhong", 21: "Xiahou Yuan", 22: "Zhang Liao", 23: "Sima Yi",
    24: "Lu Meng", 25: "Gan Ning", 26: "Jiang Wei", 27: "Zhang Jiao", 28: "Cao Ren", 29: "Cheng Pu",
    30: "Huang Gai", 31: "Han Dang", 32: "Zhang Bao", 33: "Zhang Liang", 34: "Zhang Man Cheng", 35: "Bo Zhang",
    36: "Cao Hong", 37: "Yan Liang", 38: "Wen Chou", 39: "Zhang He", 40: "Gongsun Zan", 41: "Hua Xiong",
    42: "Xu Rong", 43: "Gao Shun", 44: "Li Ru", 45: "Li Jue", 46: "Jia Xu", 47: "Guo Si", 48: "Hu Zhen",
    49: "Xu Huang", 50: "Yu Jin", 51: "Chun Yuqiong", 52: "Yue Jin", 53: "Li Dian", 54: "Xiahou En",
    55: "Cheng Yu", 56: "Xun You", 57: "Zhou Tai", 58: "Ling Tong", 59: "Xu Sheng", 60: "Ding Feng",
    61: "Pang De", 62: "Huang Quan", 63: "Guan Xing", 64: "Zhang Bao", 65: "Shamoke", 66: "Deng Ai",
    67: "Zhong Hui", 68: "Wei Yan", 69: "Ma Dai", 70: "Guan Suo", 71: "Yuan Tan", 72: "Yuan Xi",
    73: "Yuan Shang", 74: "Ju Shou", 75: "Gao Lan", 76: "Zhao Cen", 77: "Niou Fu", 78: "Fan Chou",
    79: "Wang Fang", 80: "Li Meng", 81: "He Jin", 82: "Zhu Jun", 83: "Lu Zhi", 84: "Huangfu Song",
    85: "Zhang Chao", 86: "Liu Yan", 87: "Zou Ying", 88: "Cheng Yuanzhi", 89: "Deng Mao", 90: "Guan Hai",
    91: "Pei Yuan Shao", 92: "He Yi", 93: "Yan Zheng", 94: "Gao Sheng", 95: "Liu Yan", 96: "Song Xian",
    97: "Wei Xu", 98: "Dong Xi", 99: "Lu Wei Kuang", 100: "Xun Chen", 101: "Han Meng", 102: "Han Xun",
    103: "Zhou Cang", 104: "Guan Ping", 105: "Sun Qian", 106: "Mi Zhu", 107: "Mi Fang", 108: "Liu Feng",
    109: "Chen Dao", 110: "Liao Hua", 111: "Liu Qi", 112: "Cao Pi", 113: "Cao Zhang", 114: "Zhu Huan",
    115: "Zhu Ran", 116: "Jiang Qin", 117: "Dong Xi", 118: "Pan Zhang", 119: "Yan Yan", 120: "Wu Lan",
    121: "Lei Tong", 122: "Zhang Ji", 123: "Zhu Ran", 124: "Jiang Qin", 125: "Dong Xi", 126: "Pan Zhang",
    127: "Yan Yan", 128: "Private (Wei - sword)", 129: "Corporal(Sergeant) (Wei - sword)", 130: "Sergeant(Major) (Wei - sword)",
    131: "Private (Wei - spear)", 132: "Sergeant (Wei - spear)", 133: "Major (Wei - spear)", 134: "Corporal(Private) (Wei - pike)",
    135: "Sergeant (Wei - pike)", 136: "Major (Wei - pike)", 137: "Guard (Wei - sword)", 138: "Guard Captain (Wei - sword)",
    139: "Guard (Wei - spear)", 140: "Guard Captain (Wei - spear)", 141: "Guard (Wei - pike)", 142: "Guard Captain (Wei - pike)",
    143: "Bowman (Wei)", 144: "First bow (Wei)", 145: "Crossbow (Wei)", 146: "First Crossbow (Wei)", 147: "Gate Guard (Wei)",
    148: "Gate Captain (Wei)", 149: "Private (Wu - sword)", 150: "Sergeant (Wu - sword)", 151: "Major (Wu - sword)",
    152: "Private (Wu - spear)", 153: "Sergeant (Wu - spear)", 154: "Major (Wu - spear)", 155: "Private (Wu - pike)",
    156: "Sergeant (Wu - pike)", 157: "Major (Wu - pike)", 158: "Guard (Wu - sword)", 159: "Guard Captain (Wu - sword)",
    160: "Guard (Wu - spear)", 161: "Guard Captain (Wu - spear)", 162: "Guard (Wu - pike)", 163: "Guard Captain (Wu - pike)",
    164: "Bowman (Wu)", 165: "First Bow (Wu)", 166: "Crossbow (Wu)", 167: "F.Crossbow (Wu)", 168: "Gate guard (Wu)",
    169: "Gate Captain (Wu)", 170: "Private (Shu - sword)", 171: "Sergeant (Shu - sword)", 172: "Major (Shu - sword)",
    173: "Private (Shu - spear)", 174: "Sergeant (Shu - spear)", 175: "Major (Shu - spear)", 176: "Private (Shu - pike)",
    177: "Sergeant (Shu - pike)", 178: "Major (Shu - pike)", 179: "Guard (Shu - sword)", 180: "Guard Captain (Shu - sword)",
    181: "Guard (Shu - spear)", 182: "G.Captain (Shu - spear)", 183: "Guard (Shu - pike)", 184: "G.Captain (Shu - pike)",
    185: "Bowman (Shu)", 186: "First Bow (Shu)", 187: "Crossbow (Shu)", 188: "First Crossbow (Shu)", 189: "G.guard (Shu)",
    190: "Gate Captain (Shu)", 191: "Private (YS - sword)", 192: "Sergeant (YS - sword)", 193: "Major (YS - sword)",
    194: "Private (YS - spear)", 195: "Sergeant (YS - spear)", 196: "Major (YS - spear)?", 197: "Private (YS - pike)?",
    198: "Sergeant (YS - pike)?", 199: "Major (YS - pike)?", 200: "Guard (YS - sword)", 201: "G.Captain (YS - sword)",
    202: "Guard (YS - spear)", 203: "G.Captain (YS - spear)", 204: "Guard (YS - pike)", 205: "G.Captain (YS - pike)",
    206: "Bowman (YS)", 207: "First Bow (YS)", 208: "Crossbow (YS)", 209: "Catapult Chief (YS)", 210: "Gate Guard (YS)",
    211: "G.Captain (YS)", 212: "Private (Purple - sword)", 213: "Sergeant (Purple - sword)?", 214: "Major (Purple - sword)?",
    215: "Private (Purple - spear)?", 216: "Sergeant (Purple - spear)?", 217: "Major (Purple - spear)?", 218: "Private (Purple - pike)?",
    219: "Sergeant (Purple - pike)?", 220: "Major (Purple - pike)", 221: "Guard (Purple - sword)", 222: "G.captain (Purple - sword)",
    223: "Guard (Purple - spear)?", 224: "G.Captain (Purple - spear)?", 225: "Guard (Purple - pike)?", 226: "G.Captain (Purple - pike)",
    227: "Bowman (Purple)", 228: "First Bow (Purple)?", 229: "Crossbow (Purple)?", 230: "First Crossbow (Purple)",
    231: "Gate Guard (Purple)", 232: "G.Captain (Purple)", 233: "Trooper (YT - sword)", 234: "Trooper (YT - spear)",
    235: "Trooper (YT - pike)", 236: "Captain (YT - sword)", 237: "Captain (YT - spear)", 238: "Captain (YT - pike)",
    239: "General (YT - sword)", 240: "General (YT - spear)", 241: "General (YT - pike)", 242: "Bowman (YT)",
    243: "First bow (YT)", 244: "Bowman (YT)", 245: "First Bow (YT)", 246: "Gate guard (YT)", 247: "Gate Captain (YT)",
    248: "Lady Guard", 249: "Lady Guard", 250: "Lady Guard", 251: "Lady Captain", 252: "Lady Bowman",
    253: "First Lady Bow", 254: "Bodyguard"
}

def get_unit_name(idx):
    return UNIT_NAMES.get(idx, f"Unit ID {idx}")

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        self.tw = None

    def enter(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

# Stage Mod Creator

class StageModCreator(tk.Toplevel):
    def __init__(self, parent, slots, stage_idx):
        super().__init__(parent)
        self.slots = slots
        self.stage_idx = stage_idx
        self.title("Stage Mod Creator")
        self.geometry("600x550")
        self.configure(bg=LILAC)
        self.resizable(False, False)

        self.image_paths = []
        self._setup_ui()

    def _setup_ui(self):
        # Labels
        self._lbl("Author of Mod:", 20, 20)
        self._lbl("Mod Name (No extension):", 20, 60)
        self._lbl("Version Number:", 20, 100)
        self._lbl("Mod Description:", 20, 140)

        # Entries
        self.var_author = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_version = tk.StringVar()
        
        tk.Entry(self, textvariable=self.var_author, width=30).place(x=200, y=20)
        tk.Entry(self, textvariable=self.var_name, width=30).place(x=200, y=60)
        tk.Entry(self, textvariable=self.var_version, width=30).place(x=200, y=100)

        self.txt_desc = tk.Text(self, wrap=tk.WORD, height=8, width=50)
        self.txt_desc.place(x=20, y=170)

        # Image Selection
        tk.Button(self, text="Select Images (Max 3)", command=self.select_images, 
                  bg="white", height=2).place(x=20, y=320)
        self.lbl_images = tk.Label(self, text="0 images selected", bg=LILAC)
        self.lbl_images.place(x=160, y=330)

        # Create Button
        tk.Button(self, text="Create Mod", command=self.create_mod, 
                  bg="white", font=("Arial", 12, "bold"), width=20, height=2).place(x=180, y=400)

    def _lbl(self, text, x, y):
        tk.Label(self, text=text, bg=LILAC, font=("Arial", 10)).place(x=x, y=y)

    def select_images(self):
        paths = filedialog.askopenfilenames(
            title="Select Preview Images",
            filetypes=[("Images", "*.png *.jpg *.gif")]
        )
        if paths:
            self.image_paths = list(paths[:3])
            self.lbl_images.config(text=f"{len(self.image_paths)} images selected")

    def create_mod(self):
        name = self.var_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Mod Name is required.")
            return

        ext = STAGE_EXTENSIONS[self.stage_idx]
        filename = os.path.join(DW2_MODS_DIR, name + ext)
        
        if not os.path.exists(DW2_MODS_DIR):
            os.makedirs(DW2_MODS_DIR)

        try:
            with open(filename, "wb") as f:
                # Write 512 slots
                for slot in self.slots:
                    b = bytearray(slot["raw"]) # base 32 bytes
                    for _, key, offset, size in UNIT_DATA_FIELDS:
                        val = slot[key]
                        max_val = (2**(8*size)) - 1
                        val = max(0, min(val, max_val))
                        b[offset:offset+size] = val.to_bytes(size, "little")
                    f.write(b)
                
                # Write Offsets
                for off in STAGE_OFFSETS[self.stage_idx]:
                    f.write(off.to_bytes(4, "little"))

                # append metadata
                self._write_metadata(f)
            
            messagebox.showinfo("Success", f"Mod created successfully in {DW2_MODS_DIR}!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create mod:\n{e}")

    def _write_metadata(self, f):
        # Metadata Header
        f.write(b"DW2MOD")
        
        # Write Stage ID (1 byte)
        f.write(self.stage_idx.to_bytes(1, "little"))

        # Helper to write string with 2 byte length
        def write_str(s):
            b_s = s.encode("utf-8")
            f.write(len(b_s).to_bytes(2, "little"))
            f.write(b_s)

        write_str(self.var_author.get())
        write_str(self.var_version.get())
        write_str(self.txt_desc.get("1.0", tk.END).strip())

        # Images
        f.write(len(self.image_paths).to_bytes(1, "little"))
        for p in self.image_paths:
            try:
                with open(p, "rb") as img_f:
                    data = img_f.read()
                    f.write(len(data).to_bytes(4, "little"))
                    f.write(data)
            except:
                f.write((0).to_bytes(4, "little")) # Failed image

        # Write Morale Data (Split Payload)
        stg_name = STAGE_NAMES[self.stage_idx]
        if stg_name in STAGE_MORALE_DATA:
            f.write(b"MORALE") # Marker
            
            for side_id in [1, 2]:
                # Reconstruct the list of morale values from the slots
                morale_values = []
                start_slot = 0 if side_id == 1 else 256
                end_slot = 256 if side_id == 1 else 512
                
                for i in range(start_slot, end_slot):
                    # Check if this slot is a Force Leader
                    target_val = i if side_id == 1 else (i - 256)
                    if self.slots[i]["own_slot"] == target_val and self.slots[i]["leader"] != 255:
                        m_val = self.slots[i].get("morale", 0)
                        morale_values.append(m_val)
                
                # Write Count (2 bytes) + Values (2 bytes each)
                f.write(len(morale_values).to_bytes(2, "little"))
                for val in morale_values:
                    f.write(val.to_bytes(2, "little"))
        else:
            f.write(b"NOMORALE") # Marker for no data

# Mod Manager

class HighEndModManager(tk.Toplevel):
    def __init__(self, parent, bin_path):
        super().__init__(parent)
        self.bin_path = bin_path
        self.title("DW2 Stage Mod Manager")
        self.geometry("900x500")
        self.configure(bg=LILAC)
        self.resizable(False, False)
        
        # Data
        self.mod_list = []
        self.current_preview_images = []
        self.preview_idx = 0
        
        # Automatic Backup Check on Startup
        self._ensure_all_backups()
        
        # Load Mod State
        self.mod_state = self._load_state()

        self._build_gui()
        self._scan_mods()

    def _ensure_all_backups(self):
        """Checks if backups exist, if not creates them (Stage Data + Morale)"""
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            
        missing_backups = []
        for idx, name in enumerate(STAGE_NAMES):
            safe_name = name.replace(' ', '')
            bk_path = os.path.join(BACKUP_DIR, f"Original_{safe_name}.stage")
            if not os.path.exists(bk_path):
                missing_backups.append((idx, bk_path))
        
        if missing_backups:
            try:
                with open(self.bin_path, "rb") as f_bin:
                    for idx, bk_path in missing_backups:
                        with open(bk_path, "wb") as f_bk:
                            # Backup Stage Data (Standard)
                            target_offsets = STAGE_OFFSETS[idx]
                            for off in target_offsets:
                                f_bin.seek(off)
                                f_bk.write(f_bin.read(64*32))
                            # Write offsets
                            for off in target_offsets:
                                f_bk.write(off.to_bytes(4, "little"))
                                
                            # Backup Morale Data (New)
                            stg_name = STAGE_NAMES[idx]
                            if stg_name in STAGE_MORALE_DATA:
                                f_bk.write(b"MORALE")
                                for side_id in [1, 2]:
                                    m_off, m_count = STAGE_MORALE_DATA[stg_name][side_id]
                                    f_bin.seek(m_off)
                                    data = f_bin.read(m_count * 2)
                                    f_bk.write(data)
                            else:
                                f_bk.write(b"NOMORALE")

                messagebox.showinfo("Backup", f"Automatically created {len(missing_backups)} missing backups.")
            except Exception as e:
                messagebox.showerror("Backup Error", f"Failed to auto-create backups:\n{e}")

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        # Default state: all slots empty
        return {str(i): None for i in range(8)}

    def _save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.mod_state, f, indent=4)

    def _build_gui(self):
        # Left Panel (List)
        left_frame = tk.Frame(self, bg=LILAC, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        left_frame.pack_propagate(False)

        # Search/Filter
        self.var_filter = tk.StringVar()
        self.var_filter.trace("w", self._filter_list)
        tk.Label(left_frame, text="Filter:", bg=LILAC).pack(anchor="w")
        tk.Entry(left_frame, textvariable=self.var_filter).pack(fill=tk.X, pady=(0, 5))

        # Treeview
        columns = ("Name", "Ver", "Author", "Status")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("Name", text="Mod Name")
        self.tree.heading("Ver", text="Ver")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Status", text="Status")
        self.tree.column("Name", width=140)
        self.tree.column("Ver", width=40)
        self.tree.column("Author", width=80)
        self.tree.column("Status", width=60)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_mod_select)

        # Buttons
        btn_frame = tk.Frame(left_frame, bg=LILAC)
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="Enable Mod", command=self._enable_mod, bg="white", height=2).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Restore/Disable", command=self._disable_mod, bg="#ffdddd").pack(fill=tk.X, pady=2)

        # Right Panel (Preview)
        right_frame = tk.Frame(self, bg=LILAC_LIGHT, bd=2, relief="sunken")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Image Preview Area
        self.canvas = tk.Canvas(right_frame, bg="black", height=300)
        self.canvas.pack(fill=tk.X)
        
        # Image Nav
        nav_frame = tk.Frame(right_frame, bg=LILAC_LIGHT)
        nav_frame.pack(fill=tk.X)
        tk.Button(nav_frame, text="<", command=self._prev_img).pack(side=tk.LEFT)
        tk.Button(nav_frame, text=">", command=self._next_img).pack(side=tk.RIGHT)

        # Description
        tk.Label(right_frame, text="Description:", bg=LILAC_LIGHT, anchor="w").pack(fill=tk.X, pady=(5,0))
        
        self.txt_desc_preview = tk.Text(right_frame, wrap=tk.WORD, bg="white", height=8, width=40, state="disabled") 
        self.txt_desc_preview.pack(fill=tk.BOTH, expand=True)

    def _scan_mods(self):
        self.mod_list = []
        if not os.path.exists(DW2_MODS_DIR):
            os.makedirs(DW2_MODS_DIR)

        for f in os.listdir(DW2_MODS_DIR):
            if any(f.endswith(ext) for ext in STAGE_EXTENSIONS):
                full_path = os.path.join(DW2_MODS_DIR, f)
                info = self._parse_mod_file(full_path)
                self.mod_list.append(info)
        
        self._refresh_tree()

    def _parse_mod_file(self, path):
        # Default info
        info = {
            "path": path,
            "filename": os.path.basename(path),
            "name": os.path.splitext(os.path.basename(path))[0],
            "author": "Unknown",
            "version": "1.0",
            "desc": "No description available.",
            "has_meta": False,
            "stage_id": None,
            "img_offsets": [] # (offset, size)
        }
        
        fsize = os.path.getsize(path)
        PAYLOAD_SIZE = 16416

        if fsize > PAYLOAD_SIZE:
            try:
                with open(path, "rb") as f:
                    f.seek(PAYLOAD_SIZE)
                    marker = f.read(6)
                    if marker == b"DW2MOD":
                        info["has_meta"] = True
                        
                        # Read Stage ID (1 byte)
                        stage_id_bytes = f.read(1)
                        if len(stage_id_bytes) == 1:
                            info["stage_id"] = int.from_bytes(stage_id_bytes, "little")
                        
                        def read_str():
                            l = int.from_bytes(f.read(2), "little")
                            return f.read(l).decode("utf-8")

                        info["author"] = read_str()
                        info["version"] = read_str()
                        info["desc"] = read_str()

                        # Images
                        img_count = int.from_bytes(f.read(1), "little")
                        for _ in range(img_count):
                            size = int.from_bytes(f.read(4), "little")
                            if size > 0:
                                info["img_offsets"].append((f.tell(), size))
                                f.seek(size, 1) # Skip data
            except:
                pass # Corrupt meta, use defaults
        
        # Fallback for old mods or missing meta: guess stage ID from extension
        if info["stage_id"] is None:
            ext = os.path.splitext(path)[1]
            try:
                info["stage_id"] = STAGE_EXTENSIONS.index(ext)
            except:
                pass

        return info

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        search = self.var_filter.get().lower()
        
        for mod in self.mod_list:
            if search in mod["name"].lower() or search in mod["author"].lower():
                # Check status based on filename match in Ledger
                status = ""
                sid = str(mod["stage_id"])
                if sid in self.mod_state and self.mod_state[sid] == mod["filename"]:
                    status = "Enabled"
                
                self.tree.insert("", "end", iid=mod["path"], 
                                 values=(mod["name"], mod["version"], mod["author"], status))

    def _filter_list(self, *args):
        self._refresh_tree()

    def _on_mod_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        path = sel[0]
        
        mod = next((m for m in self.mod_list if m["path"] == path), None)
        if not mod: return

        # Unlock, Edit, then Lock
        self.txt_desc_preview.config(state="normal")
        self.txt_desc_preview.delete("1.0", tk.END)
        self.txt_desc_preview.insert("1.0", mod["desc"])
        self.txt_desc_preview.config(state="disabled")

        # Load Images
        self.current_preview_images = []
        if mod["img_offsets"]:
            try:
                with open(mod["path"], "rb") as f:
                    for off, size in mod["img_offsets"]:
                        f.seek(off)
                        data = f.read(size)
                        img = Image.open(io.BytesIO(data))
                        # Force resize to exactly 450x300 (ignoring aspect ratio)
                        img = img.resize((450, 300), Image.Resampling.LANCZOS)
                        self.current_preview_images.append(ImageTk.PhotoImage(img))
            except:
                pass
        
        self.preview_idx = 0
        self._show_image()

    def _show_image(self):
        self.canvas.delete("all")
        if self.current_preview_images:
            img = self.current_preview_images[self.preview_idx]
            # Center it
            cw = self.canvas.winfo_width() or 450
            ch = self.canvas.winfo_height() or 300
            self.canvas.create_image(cw//2, ch//2, image=img)
        else:
            self.canvas.create_text(225, 150, text="No Preview", fill="white")

    def _next_img(self):
        if not self.current_preview_images: return
        self.preview_idx = (self.preview_idx + 1) % len(self.current_preview_images)
        self._show_image()

    def _prev_img(self):
        if not self.current_preview_images: return
        self.preview_idx = (self.preview_idx - 1) % len(self.current_preview_images)
        self._show_image()

    def _enable_mod(self):
        sel = self.tree.selection()
        if not sel: return
        path = sel[0]
        mod = next((m for m in self.mod_list if m["path"] == path), None)
        
        stage_id = mod["stage_id"]
        if stage_id is None:
            messagebox.showerror("Error", "Could not identify target stage.")
            return

        # Collision detection
        sid_str = str(stage_id)
        current_active = self.mod_state.get(sid_str)
        
        if current_active and current_active != mod["filename"]:
            messagebox.showwarning("Collision", f"Please disable '{current_active}' first.")
            return
        
        if current_active == mod["filename"]:
            messagebox.showinfo("Info", "Mod already enabled.")
            return

        # Apply Mod
        try:
            PAYLOAD_SIZE = 16416
            target_offsets = STAGE_OFFSETS[stage_id]

            with open(path, "rb") as f_mod, open(self.bin_path, "r+b") as f_bin:
                # Write Stage Data
                payload = f_mod.read(PAYLOAD_SIZE)
                chunk_size = 64 * 32
                for i, target_off in enumerate(target_offsets):
                    chunk_data = payload[i*chunk_size : (i+1)*chunk_size]
                    f_bin.seek(target_off)
                    f_bin.write(chunk_data)
                
                # Parse Metadata to find Morale
                # We need to skip the header info to get to the data
                marker = f_mod.read(6) # DW2MOD
                if marker == b"DW2MOD":
                    # Skip Stage ID
                    f_mod.read(1)
                    # Skip Strings (Author, Ver, Desc)
                    for _ in range(3):
                        l = int.from_bytes(f_mod.read(2), "little")
                        f_mod.read(l)
                    # Skip Images
                    img_cnt = int.from_bytes(f_mod.read(1), "little")
                    for _ in range(img_cnt):
                        l = int.from_bytes(f_mod.read(4), "little")
                        f_mod.read(l)
                    
                    # Check for Morale Block
                    m_marker = f_mod.read(6)
                    if m_marker == b"MORALE":
                        stg_name = STAGE_NAMES[stage_id]
                        if stg_name in STAGE_MORALE_DATA:
                            for side_id in [1, 2]:
                                # Read from Mod
                                count = int.from_bytes(f_mod.read(2), "little")
                                data = f_mod.read(count * 2)
                                
                                # Write to Bin
                                bin_off, bin_count = STAGE_MORALE_DATA[stg_name][side_id]
                                # Safety: don't write more than the bin expects
                                write_len = min(len(data), bin_count * 2)
                                
                                f_bin.seek(bin_off)
                                f_bin.write(data[:write_len])

            # Update State
            self.mod_state[sid_str] = mod["filename"]
            self._save_state()
            self._refresh_tree()
            messagebox.showinfo("Success", f"Mod '{mod['name']}' enabled.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable mod:\n{e}")

    def _disable_mod(self):
        sel = self.tree.selection()
        if not sel: return
        
        path = sel[0]
        mod = next((m for m in self.mod_list if m["path"] == path), None)
        stage_id = mod["stage_id"]
        sid_str = str(stage_id)
        
        if self.mod_state.get(sid_str) != mod["filename"]:
            messagebox.showinfo("Info", "This mod is not enabled.")
            return

        # Restore from Backup
        bk_name = f"Original_{STAGE_NAMES[stage_id].replace(' ', '')}.stage"
        bk_path = os.path.join(BACKUP_DIR, bk_name)
        
        if not os.path.exists(bk_path):
            messagebox.showerror("Error", "Backup not found.")
            return

        try:
            with open(bk_path, "rb") as f_bk, open(self.bin_path, "r+b") as f_bin:
                # Restore Stage Data
                payload = f_bk.read(16416)
                target_offsets = STAGE_OFFSETS[stage_id]
                chunk_size = 64 * 32
                for i, target_off in enumerate(target_offsets):
                    chunk_data = payload[i*chunk_size : (i+1)*chunk_size]
                    f_bin.seek(target_off)
                    f_bin.write(chunk_data)
                
                # Restore Morale (If present)
                m_marker = f_bk.read(6)
                if m_marker == b"MORALE":
                    stg_name = STAGE_NAMES[stage_id]
                    if stg_name in STAGE_MORALE_DATA:
                        for side_id in [1, 2]:
                            bin_off, bin_count = STAGE_MORALE_DATA[stg_name][side_id]
                            data = f_bk.read(bin_count * 2)
                            f_bin.seek(bin_off)
                            f_bin.write(data)
            
            self.mod_state[sid_str] = None
            self._save_state()
            self._refresh_tree()
            messagebox.showinfo("Success", f"Restored {STAGE_NAMES[stage_id]} to original.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")

# Main App

class DW2CoordinateGuider:
    def __init__(self, root):
        self.root = root
        self.root.title("DW2 Visual Guider")
        self.root.geometry("1840x900") 

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.maps_dir = os.path.join(self.base_dir, "maps")
        os.makedirs(self.maps_dir, exist_ok=True)
        
        # Binary File Auto-detect
        self.bin_path = None
        possible_path = os.path.join(self.base_dir, "DW2.bin")
        if os.path.exists(possible_path):
            self.bin_path = possible_path
        else:
            possible_path = os.path.join(os.path.dirname(self.base_dir), "DW2.bin")
            if os.path.exists(possible_path):
                self.bin_path = possible_path

        # Canvas Variables
        self.original_width = 800
        self.original_height = 800
        self.scale = 1.0
        self.zoom_level = 1.0
        
        self.base_image = None
        self.current_pil_image = None # For Pixel Analysis
        self.display_image = None
        self.image_id = None

        self.current_stage_index = 0
        self.slots = [] 
        self.markers = [] 
        
        self.selected_indices = set() # Set of integers
        self.drag_start_x = None
        self.drag_start_y = None
        self.drag_rect_id = None
        self.dragging_unit_idx = None # If dragging units
        
        # Visual Options
        self.show_guards_var = tk.BooleanVar(value=True) # Default ON
        
        self.entry_vars = {} 
        self.list_map = []
        
        self._setup_ui()
        self.load_stage_data(0)

    def _setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Wide Right Panel for Editor
        right_frame = tk.Frame(main_frame, width=650) # Changed from 500 to 650
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Top Bar
        top_bar = tk.Frame(left_frame)
        top_bar.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(top_bar, text="Load DW2.bin", command=self.browse_bin_file).pack(side=tk.LEFT, padx=5)
        tk.Label(top_bar, text="Stage:").pack(side=tk.LEFT)
        self.stage_combo = ttk.Combobox(top_bar, values=STAGE_NAMES, state="readonly", width=25)
        self.stage_combo.current(0)
        self.stage_combo.pack(side=tk.LEFT, padx=5)
        self.stage_combo.bind("<<ComboboxSelected>>", self.on_stage_changed)
        
        # Guards Checkbox
        tk.Checkbutton(top_bar, text="Show Guards", variable=self.show_guards_var, command=self.refresh_markers).pack(side=tk.LEFT, padx=10)

        self.show_morale_var = tk.BooleanVar(value=False)
        tk.Checkbutton(top_bar, text="Show Morale", variable=self.show_morale_var, command=self.refresh_markers).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        tk.Button(top_bar, text="Mod Manager", command=self.open_mod_manager, 
                  bg=LILAC, fg="white", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)
        tk.Button(top_bar, text="Save Mod File", command=self.save_mod_file, bg="#ddffdd").pack(side=tk.RIGHT, padx=5)

        tk.Button(top_bar, text="Gen PNACH", command=self.generate_pnach, 
                  bg="#8A2BE2", fg="white", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(top_bar, text="Predict", command=self.calculate_likely_outcome, 
                  bg=GOLD_BTN, fg="black", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)

        tk.Button(top_bar, text="Generate Stage", command=self.generate_procedural_stage,
                  bg=ORANGE_BTN, fg="black", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)

        tk.Button(top_bar, text="Randomize Stats", command=self.open_stat_randomizer, 
                  bg="#FF69B4", fg="black", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(top_bar, text="Auto-Balance", command=self.run_auto_balance, 
                  bg=CYAN_BTN, fg="black", font=("Arial", 9, "bold")).pack(side=tk.RIGHT, padx=20)
        
        # Canvas Container
        canvas_container = tk.Frame(left_frame, bd=2, relief=tk.SUNKEN)
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        vbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        hbar = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(canvas_container, bg="#333333", 
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        vbar.config(command=self.canvas.yview)
        hbar.config(command=self.canvas.xview)
        
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # bindings
        self.canvas.bind("<ButtonPress-1>", self.on_left_press)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<ButtonPress-2>", self.start_pan) 
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<ButtonPress-3>", self.start_pan) 
        self.canvas.bind("<B3-Motion>", self.do_pan)

        # right panel
        
        # Squad Editor
        edit_frame = tk.LabelFrame(right_frame, text="Squad Editor")
        edit_frame.pack(fill=tk.X, pady=5)
        
        # Global Morale Bar Area
        # A small canvas to draw the Blue vs Red balance
        self.morale_canvas = tk.Canvas(edit_frame, width=300, height=30, bg="#333333", highlightthickness=0)
        self.morale_canvas.grid(row=0, column=0, columnspan=4, pady=(5, 10))
        
        self.lbl_selected = tk.Label(edit_frame, text="No Selection", fg="gray", font=("Arial", 10, "bold"))
        self.lbl_selected.grid(row=1, column=0, columnspan=4, pady=5)

        # Define Tooltip Dictionary
        TOOLTIPS = {
            "x": "Horizontal coordinate on the map (0-800)",
            "y": "Vertical coordinate on the map (0-800)",
            "dir": "Facing direction (0-7). 0 is North/Up.",
            "path": "Pathing, relates to what the squad prioritizes.",
            "gate_mode": "Behavior state of the Gate",
            "life": "Life of the squad leader, guards get 33.3% less of it.",
            "leader": "The ID of this squad's Officer/Commander.",
            "guard_id": "The ID of the squad leader's guards.",
            "atk": "Attack of the squad leader, guards get 33.3% less of it.",
            "def": "Defense of the squad leader, guards get 33.3% less of it.",
            "guard_cnt": "Number of bodyguards (Total unit size including leader), max value DW2 supports is 9.",
            "own_slot": "Determines who the squad serves, \n if the value is the same as the slot number \n then the squad becomes its own force. \n DW2 has issues if there are more than 22 forces on a stage.",
            "type": "Unit Class (0=Player, 1=Commander, 2=General, 3=Playable Officer, \n 4=NPC Officer, 5= Gate Captain/Guards/Troops that don't respawn, 6=Troops which do respawn).",
            "ai_type": "This determines the type of unit the squad is, 2 specifies \n they're ranged units while 4 has the squad squad \n spawn on a horse.",
            "orders": "This determines the orders of the squad. 1 = attack enemy slot, 3 = follow ally slot, \n 4 = hold position. There are other types but not all are documented.",
            "hidden": "This sets the squad to be hidden, values 1 and higher have the \n squad not appear on the map until the event related to \n them is triggered. Setting to 0 forces the squad \n to appear regardless of event.",
            "target": "This determines who is targeted by the squad. If orders is set to 1, they target \n the enemy slot number set for Order Tgt. If orders is set to 3, they follow the ally slot \n set by Order Tgt.",
            "drop": "Item ID dropped upon defeat.",
            "ai_lvl": "Aggression/Intelligence.",
            "delay": "This determines how long the squad waits before advancing. \n Setting to 0 makes them advance sooner if their orders \n are attack enemy slot.",
            "points": "Points awarded to player for KO of this squad."
        }

        row = 2
        col = 0
        for label_text, key, _, _ in UNIT_DATA_FIELDS:
            # Create Label
            lbl = tk.Label(edit_frame, text=label_text + ":")
            lbl.grid(row=row, column=col*2, sticky="e", padx=2, pady=2)
            
            # Attach Tooltip if one exists for this key
            if key in TOOLTIPS:
                ToolTip(lbl, TOOLTIPS[key])

            var = tk.StringVar()
            self.entry_vars[key] = var
            entry = tk.Entry(edit_frame, textvariable=var, width=22)
            entry.grid(row=row, column=col*2+1, sticky="w", padx=2, pady=2)
            
            col += 1
            if col > 1:
                col = 0
                row += 1

       # Morale Field
        # Create Label as a variable so we can attach a tooltip
        lbl_morale = tk.Label(edit_frame, text="Morale:")
        lbl_morale.grid(row=row, column=0, sticky="e", padx=2, pady=2)
        ToolTip(lbl_morale, "Force Morale (0-899). Only editable for Force Leaders. \n Morale affects how well the squads fight offscreen \n when the player isn't around.")

        # Create Entry
        self.var_morale = tk.StringVar()
        self.entry_morale = tk.Entry(edit_frame, textvariable=self.var_morale, width=22)
        self.entry_morale.grid(row=row, column=1, sticky="w", padx=2, pady=2)

        btn_frame = tk.Frame(edit_frame)
        btn_frame.grid(row=row+1, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Update Squad Data", command=self.update_selected_unit_data, bg="#ccffcc", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Squad", command=self.delete_selected_unit, bg="#ffdddd").pack(side=tk.LEFT, padx=5)

        # Master Unit ID Reference (Searchable)
        tk.Label(btn_frame, text="ID Lookup:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(15, 2))
        
        # Generate List
        sorted_all_units = sorted(UNIT_NAMES.items(), key=lambda x: x[0])
        # Store in self so the filter function can access the full list later
        self.all_unit_values = [f"{name} ({uid})" for uid, name in sorted_all_units]
        
        cb_unit_ref = ttk.Combobox(btn_frame, values=self.all_unit_values, state="normal", width=35)
        cb_unit_ref.set("Type to Filter")
        cb_unit_ref.pack(side=tk.LEFT, padx=2)
        
        # Bind the KeyRelease event to the filter function
        cb_unit_ref.bind('<KeyRelease>', self._on_combo_keyrelease)
        
        add_frame = tk.LabelFrame(right_frame, text="Add New Unit")
        add_frame.pack(fill=tk.X, pady=10)
        self.lbl_cap_s1 = tk.Label(add_frame, text="Side 1 (Blue): 0/256", fg="blue")
        self.lbl_cap_s1.pack(anchor="w", padx=5)
        self.lbl_cap_s2 = tk.Label(add_frame, text="Side 2 (Red): 0/256", fg="red")
        self.lbl_cap_s2.pack(anchor="w", padx=5)
        
        btn_add_frame = tk.Frame(add_frame)
        btn_add_frame.pack(fill=tk.X)
        tk.Button(btn_add_frame, text="Add to Side 1", command=lambda: self.add_unit(1)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_add_frame, text="Add to Side 2", command=lambda: self.add_unit(2)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Unit List
        list_frame = tk.LabelFrame(right_frame, text="Unit List (Multi-Select)")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Filter:").pack(side=tk.LEFT)
        self.var_search = tk.StringVar()
        self.var_search.trace("w", self.filter_list)
        tk.Entry(search_frame, textvariable=self.var_search).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Listbox now extended mode
        self.listbox = tk.Listbox(list_frame, exportselection=False, width=40, selectmode=tk.EXTENDED)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = tk.Scrollbar(list_frame, command=self.listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        
        # Zoom Controls
        zoom_frame = tk.Frame(right_frame)
        zoom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(zoom_frame, text="-", width=3, command=self.zoom_out).pack(side=tk.LEFT)
        tk.Button(zoom_frame, text="+", width=3, command=self.zoom_in).pack(side=tk.LEFT)
        self.lbl_zoom = tk.Label(zoom_frame, text="100%")
        self.lbl_zoom.pack(side=tk.LEFT, padx=5)

    def _on_combo_keyrelease(self, event):
        # Get the widget that triggered the event
        combo = event.widget
        # If user pressed Up/Down/Return, don't filter (let them navigate)
        if event.keysym in ['Up', 'Down', 'Return', 'Enter']:
            return

        # Get current text
        value = event.widget.get()
        
        # If empty, reset to full list
        if value == '':
            combo['values'] = self.all_unit_values
        else:
            # Filter the list based on case-insensitive match
            data = []
            for item in self.all_unit_values:
                if value.lower() in item.lower():
                    data.append(item)
            combo['values'] = data

    # Genetic algorithm and auto-balance
    
    def calculate_tcp(self, slots):
        """Calculates Total Combat Power for a list of units"""
        total = 0
        for s in slots:
            if s["leader"] == 255 or (s["x"]==0 and s["y"]==0): continue
            
            # Formula: Life * Attack * Defense * AI
            life = max(1, s["life"])
            atk = max(1, s["atk"])
            defence = max(1, s["def"])
            ai = max(1, s["ai_lvl"])
            
            total += life * atk * defence * ai
        return total

    def calculate_likely_outcome(self):
        """Estimates the battle outcome by comparing TCP"""
        if not self.slots: return

        # Find Commanders (Type == 1)
        c1_name = "Unknown Commander"
        c2_name = "Unknown Commander"
        
        for i in range(256):
            if self.slots[i]["leader"] != 255 and self.slots[i]["type"] == 1:
                c1_name = get_unit_name(self.slots[i]["leader"])
                break
        
        for i in range(256, 512):
            if self.slots[i]["leader"] != 255 and self.slots[i]["type"] == 1:
                c2_name = get_unit_name(self.slots[i]["leader"])
                break
                
        # Calculate TCP
        s1 = self.slots[0:256]
        s2 = self.slots[256:512]
        tcp1 = self.calculate_tcp(s1)
        tcp2 = self.calculate_tcp(s2)
        
        if tcp1 == 0 or tcp2 == 0:
            messagebox.showinfo("Outcome", "One side has 0 combat power. Winner is obvious.")
            return

        if tcp1 > tcp2:
            winner = "Side 1 (Blue)"
            w_cmd = c1_name
            l_cmd = c2_name
            ratio = tcp1 / tcp2
        else:
            winner = "Side 2 (Red)"
            w_cmd = c2_name
            l_cmd = c1_name
            ratio = tcp2 / tcp1
        
        if ratio < 1.1:
            outcome = "Stalemate/Phyrric Victory"
            desc = f"The battle will likely be a long, bloody stalemate.\n{l_cmd} may fall but {w_cmd} will suffer heavy losses."
        elif ratio < 1.5:
            outcome = "Decisive Victory"
            desc = f"{w_cmd} has a clear advantage.\n{l_cmd} will likely be defeated after a moderate struggle."
        elif ratio < 2.0:
            outcome = "Crushing Defeat"
            desc = f"{w_cmd} dominates the battlefield.\n{l_cmd} will be routed quickly."
        else:
            outcome = "Instant Wipe"
            desc = f"Total defeat.\n{l_cmd}'s forces will evaporate almost instantly against {w_cmd}."

        adv_pct = int((ratio - 1) * 100)
            
        msg = (f"Battle Prediction \n\n"
               f"Side 1 (Blue): {c1_name}\n"
               f"Side 2 (Red):  {c2_name}\n\n"
               f"TCP Ratio: {tcp1:,} vs {tcp2:,}\n"
               f"Advantage: {winner} (+{adv_pct}%)\n\n"
               f"Likely Outcome: {outcome}\n"
               f"{desc}")
        
        messagebox.showinfo("Likely Outcome", msg)

    def get_deployment_zone(self, side_slots):
        """Finds the centroid of existing units to spawn near friends"""
        xs = [s["x"] for s in side_slots if s["leader"]!=255]
        ys = [s["y"] for s in side_slots if s["leader"]!=255]
        if not xs: return 400, 400
        return sum(xs)//len(xs), sum(ys)//len(ys)

    def get_pixel_variant(self, x, y):
        """Returns (R, G, B, A, Hue) or None if out of bounds"""
        if not self.current_pil_image: return None
        
        w, h = self.current_pil_image.size
        
        # Clamp to h-1 to prevent index out of bounds
        ix = int(x)
        iy = int(h - y) 
        
        if ix < 0 or ix >= w or iy < 0 or iy >= h: return None
        
        try:
            r, g, b, a = self.current_pil_image.getpixel((ix, iy))
            # Get HSV (Hue 0-1, Sat 0-1, Val 0-1)
            h_val, s_val, v_val = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            return (r, g, b, a, h_val, s_val, v_val)
        except:
            return None

    def is_valid_terrain(self, x, y):
        """
        GA Constraint: Check if pixel is valid
        Strict Mode: Rejects semi-transparency and wider blue ranges
        """
        offsets = [(0,0), (0,10), (0,-10), (10,0), (-10,0)]
        
        for ox, oy in offsets:
            data = self.get_pixel_variant(x + ox, y + oy)
            if not data: return False # Out of bounds
            
            r, g, b, a, hue, sat, val = data
            
            # string Transparency Check (The Fix for Alpha 128)
            if a < 250: 
                return False 

            # Check Black/Dark (Void)
            if r < 40 and g < 40 and b < 40: 
                return False

            # Check Water (HSV + RGB)
            blue_dominant = (b > r + 15) and (b > g + 15)
            blue_hue = (0.45 < hue < 0.75)
            has_color = (sat > 0.15)

            if (blue_dominant or blue_hue) and has_color:
                return False 
                
        return True

    def is_crowded(self, x, y, all_units):
        """GA Constraint: Check 5 pixel collision rule"""
        for s in all_units:
            if s["leader"] == 255: continue
            if abs(s["x"] - x) < 5 and abs(s["y"] - y) < 5:
                return True
        return False

    def run_auto_balance(self):
        if not self.slots: return
        
        s1 = self.slots[0:256]
        s2 = self.slots[256:512]
        
        tcp1 = self.calculate_tcp(s1)
        tcp2 = self.calculate_tcp(s2)
        
        if tcp1 == tcp2:
            messagebox.showinfo("Balance", "Combat Power is exactly equal!")
            return
            
        weak_side_idx = 1 if tcp1 > tcp2 else 0
        target_gap = abs(tcp1 - tcp2)
        
        # Define Weaker Side
        weak_slots = s2 if weak_side_idx == 1 else s1
        weak_start_idx = 256 if weak_side_idx == 1 else 0
        
        # Identify Empty Slots
        empty_indices = [i for i, s in enumerate(weak_slots) if s["leader"] == 255]
        if not empty_indices:
            messagebox.showwarning("Full", "Weaker side has no empty slots!")
            return

        # Find Deployment Zone
        center_x, center_y = self.get_deployment_zone(weak_slots)
        
        # GA
        POPULATION_SIZE = 20
        GENERATIONS = 15
        
        def create_random_unit():
            # Standard Random Search (Preferred)
            for _ in range(40): 
                nx = center_x + random.randint(-150, 150)
                ny = center_y + random.randint(-150, 150)
                nx = max(10, min(790, nx))
                ny = max(10, min(790, ny))
                
                if self.is_valid_terrain(nx, ny) and not self.is_crowded(nx, ny, weak_slots):
                    return {
                        "leader": 128, 
                        "x": nx, "y": ny,
                        "life": random.randint(100, 300),
                        "atk": random.randint(5, 20),
                        "def": random.randint(5, 20),
                        "ai_lvl": random.randint(1, 8),
                        "dir": 0, "path": 0, "gate_mode": 0, "guard_id": 0,
                        "guard_cnt": 0, "own_slot": 0, "ai_type": 0, "orders": 0,
                        "hidden": 0, "target": 255, "drop": 0, "delay": 0, "points": 0
                    }
            
            # Smart Buddy Spawning
            valid_friends = [s for s in weak_slots if s["leader"] != 255]
            
            if valid_friends:
                for attempt in range(30):
                    buddy = random.choice(valid_friends)
                    
                    if attempt < 10:
                        offsets = [-12, -8, -6, 6, 8, 12] # Safe Spacing
                    else:
                        offsets = [-2, -1, 1, 2] # Tight Squeeze
                        
                    fx = buddy["x"] + random.choice(offsets)
                    fy = buddy["y"] + random.choice(offsets)
                    fx = max(10, min(790, fx))
                    fy = max(10, min(790, fy))
                    
                    if self.is_valid_terrain(fx, fy):
                        return {
                            "leader": 128, "x": fx, "y": fy,
                            "life": 100, "atk": 5, "def": 5, "ai_lvl": 1,
                            "dir": 0, "path": 0, "gate_mode": 0, "guard_id": 0,
                            "guard_cnt": 0, "own_slot": 0, "ai_type": 0, "orders": 0,
                            "hidden": 0, "target": 255, "drop": 0, "delay": 0, "points": 0
                        }

                # desperate spawn (Ignore Terrain)
                buddy = random.choice(valid_friends)
                fx = buddy["x"] + random.choice([-2, -1, 1, 2])
                fy = buddy["y"] + random.choice([-2, -1, 1, 2])
                fx = max(10, min(790, fx))
                fy = max(10, min(790, fy))
                
                return {
                    "leader": 128, "x": fx, "y": fy,
                    "life": 100, "atk": 5, "def": 5, "ai_lvl": 1,
                    "dir": 0, "path": 0, "gate_mode": 0, "guard_id": 0,
                    "guard_cnt": 0, "own_slot": 0, "ai_type": 0, "orders": 0,
                    "hidden": 0, "target": 255, "drop": 0, "delay": 0, "points": 0
                }

            # Absolute Last Resort
            rx = center_x + random.randint(-50, 50)
            ry = center_y + random.randint(-50, 50)
            return {
                "leader": 128, "x": rx, "y": ry,
                "life": 100, "atk": 5, "def": 5, "ai_lvl": 1,
                "dir": 0, "path": 0, "gate_mode": 0, "guard_id": 0,
                "guard_cnt": 0, "own_slot": 0, "ai_type": 0, "orders": 0,
                "hidden": 0, "target": 255, "drop": 0, "delay": 0, "points": 0
            }

        # Initial Population
        population = []
        for _ in range(POPULATION_SIZE):
            count = random.randint(1, min(10, len(empty_indices)))
            ind = [create_random_unit() for _ in range(count)]
            population.append(ind)

        best_solution = None
        best_diff = float('inf')

        # Evolution Loop
        for gen in range(GENERATIONS):
            scored_pop = []
            for ind in population:
                added_tcp = self.calculate_tcp(ind)
                diff = abs(target_gap - added_tcp)
                scored_pop.append((diff, ind))
                if diff < best_diff:
                    best_diff = diff
                    best_solution = ind
            
            scored_pop.sort(key=lambda x: x[0])
            survivors = [x[1] for x in scored_pop[:POPULATION_SIZE//2]]
            
            new_pop = survivors[:]
            while len(new_pop) < POPULATION_SIZE:
                parent = random.choice(survivors)
                child = copy.deepcopy(parent)
                
                if random.random() < 0.3:
                    if random.random() < 0.5 and len(child) < len(empty_indices):
                        child.append(create_random_unit())
                    elif len(child) > 1:
                        child.pop()
                if random.random() < 0.3:
                    u = random.choice(child)
                    u["life"] = max(1, u["life"] + random.randint(-50, 50))
                
                new_pop.append(child)
            population = new_pop

        # apply best solution
        self.selected_indices.clear()
        
        final_units = []
        for u in best_solution:
            if not self.is_crowded(u["x"], u["y"], final_units):
                final_units.append(u)

        count_added = 0
        for unit_data in final_units:
            if not empty_indices: break
            slot_idx = empty_indices.pop(0) + weak_start_idx
            unit_data["own_slot"] = slot_idx
            self.slots[slot_idx].update(unit_data)
            self.selected_indices.add(slot_idx) 
            count_added += 1

        self._update_editor_panel()
        self.refresh_markers()
        self.refresh_listbox()
        self.update_caps()
        self._update_global_morale()
        
        side_name = "Side 1 (Blue)" if weak_side_idx == 0 else "Side 2 (Red)"
        msg = (f"Analysis Complete.\n"
               f"{side_name} was weaker by {target_gap:,} TCP.\n"
               f"GA generated {count_added} reinforcements to balance power.\n"
               f"Units placed near deployment zone ({center_x}, {center_y}).")
        messagebox.showinfo("Auto-Balance Complete", msg)

    # Scenario generator

    def generate_procedural_stage(self):
        stage_name = STAGE_NAMES[self.current_stage_index]
        if stage_name not in STAGES_ZONES:
            messagebox.showerror("Error", f"No Zone Data defined for {stage_name} yet.\nPlease contact the developer.")
            return
        
        if not messagebox.askyesno("Confirm", "This will wipe all current units and generate a new battle.\nContinue?"):
            return

        # wipe map
        for i in range(512):
            self.slots[i].update({
                "leader": 255, "x": 0, "y": 0, "guard_cnt": 0,
                "life": 0, "atk": 0, "def": 0, "ai_lvl": 0
            })

        zones = STAGES_ZONES[stage_name]
        
        # generate commanders (Type 1)
        # Side 1 Commander (Blue) - Slot 0
        s1_zone = random.choice(zones["Side 1"])
        self._spawn_unit_in_zone(0, s1_zone, is_commander=True, side=1)
        
        # Side 2 Commander (Red) - Slot 256
        s2_zone = random.choice(zones["Side 2"])
        self._spawn_unit_in_zone(256, s2_zone, is_commander=True, side=2)

        # generate armies
        # Side 1 Troops (Slots 1-50)
        for i in range(1, 101):
            z = random.choice(zones["Side 1"])
            self._spawn_unit_in_zone(i, z, is_commander=False, side=1)
            
        # Side 2 Troops (Slots 257-307)
        for i in range(257, 357):
            z = random.choice(zones["Side 2"])
            self._spawn_unit_in_zone(i, z, is_commander=False, side=2)

        self.selected_indices.clear()
        self._update_editor_panel()
        self.refresh_markers()
        self.refresh_listbox()
        self.update_caps()
        self._update_global_morale()
        messagebox.showinfo("Success", f"Generated new scenario for {stage_name}.")

    def _spawn_unit_in_zone(self, slot_idx, zone, is_commander, side):
        rect = zone["rect"] # (minx, miny, maxx, maxy)
        
        # Helper to clamp coords to map bounds (0-799)
        # prevents 800 error which is technically out of index
        def get_rand_spot():
            rx = random.randint(rect[0], rect[2])
            ry = random.randint(rect[1], rect[3])
            return max(0, min(790, rx)), max(0, min(790, ry))

        # Check existing units to prevent crowding
        # We only care about leaders for crowding checks to save perf
        all_units = [s for s in self.slots if s["leader"] != 255]

        # Perfect spawn (Valid Terrain + Space)
        # Try hard (1000 times) to find a good empty spot
        for _ in range(1000):
            rx, ry = get_rand_spot()
            if self.is_valid_terrain(rx, ry) and not self.is_crowded(rx, ry, all_units):
                self._apply_spawn_data(slot_idx, rx, ry, is_commander, side)
                return

        # Crowded spawn (Valid Terrain, Ignore Buddies)
        # If the zone is full, just stack them on top of each other
        # Better to have stacked units on land than spread out units in water
        for _ in range(1000):
            rx, ry = get_rand_spot()
            if self.is_valid_terrain(rx, ry):
                self._apply_spawn_data(slot_idx, rx, ry, is_commander, side)
                return

        # Desperate (Force Rect)
        # If we get here the zone is likely invalid (all water/wall)
        # Just spawn randomly in the box so the unit exists
        rx, ry = get_rand_spot()
        self._apply_spawn_data(slot_idx, rx, ry, is_commander, side)

    def _apply_spawn_data(self, slot_idx, x, y, is_commander, side):
        # Helper to apply stats
        leader_id = random.choice([0, 1, 5, 10]) if is_commander else 128
        unit_type = 1 if is_commander else 6
        
        self.slots[slot_idx].update({
            "leader": leader_id,
            "x": x, "y": y,
            "type": unit_type,
            "life": 300 if is_commander else 150,
            "atk": 20 if is_commander else 10,
            "def": 20 if is_commander else 10,
            "guard_cnt": 5 if is_commander else 0, # Visuals use Count-1
            "ai_lvl": 8 if is_commander else 2,
            "dir": random.randint(0, 7),
            "own_slot": slot_idx
        })

    # File I/O
    
    def browse_bin_file(self):
        filename = filedialog.askopenfilename(title="Select DW2.bin", filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")])
        if filename:
            self.bin_path = filename
            self.load_stage_data(self.stage_combo.current())

    def load_stage_data(self, stage_idx):
        self.current_stage_index = stage_idx
        self.slots = [] 
        self.load_image(MAP_FILES[stage_idx])
        
        if not self.bin_path or not os.path.exists(self.bin_path):
            self.lbl_selected.config(text="DW2.bin not loaded", fg="red")
            self.refresh_markers(); self.refresh_listbox(); return

        try:
            with open(self.bin_path, "rb") as f:
                # read unit slots
                for block_offset in STAGE_OFFSETS[stage_idx]:
                    f.seek(block_offset)
                    for _ in range(64):
                        chunk = f.read(32)
                        if len(chunk) != 32: break
                        slot_data = {"raw": bytearray(chunk), "morale": 0} # Init morale
                        for _, key, offset, size in UNIT_DATA_FIELDS:
                            val = int.from_bytes(chunk[offset:offset+size], "little")
                            slot_data[key] = val
                        self.slots.append(slot_data)

                # read morale data (If available for this stage)
                stg_name = STAGE_NAMES[stage_idx]
                if stg_name in STAGE_MORALE_DATA:
                    for side_id in [1, 2]:
                        m_off, m_count = STAGE_MORALE_DATA[stg_name][side_id]
                        f.seek(m_off)
                        
                        # Read all morale values for this side
                        morale_list = []
                        for _ in range(m_count):
                            morale_list.append(int.from_bytes(f.read(2), "little"))
                        
                        start_slot = 0 if side_id == 1 else 256
                        end_slot = 256 if side_id == 1 else 512
                        
                        m_idx = 0
                        for i in range(start_slot, end_slot):
                            # Side 2 uses Relative Index (0-255), not Absolute (256-511)
                            # If I am at absolute slot 300, my own_slot value will be 44 (300-256)
                            target_val = i if side_id == 1 else (i - 256)
                            
                            if self.slots[i]["own_slot"] == target_val and self.slots[i]["leader"] != 255:
                                if m_idx < len(morale_list):
                                    self.slots[i]["morale"] = morale_list[m_idx]
                                    m_idx += 1
        
            self.selected_indices.clear()
            self._update_editor_panel()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read binary:\n{e}")
            return

        self.refresh_markers()
        self.refresh_listbox()
        self.update_caps()
        self._update_global_morale()

    def save_mod_file(self):
        """Opens the Stage Mod Creator instead of direct save"""
        if not self.slots: return
        # Open Creator Window
        StageModCreator(self.root, self.slots, self.current_stage_index)

    def generate_pnach(self):
        if not self.slots: return
        
        # Constants
        # Unit Data Base Addresses (US Version)
        # Side 1 (Slots 0-255) ram Base
        UNIT_RAM_BASE_S1 = 0x203E4980 
        
        # Side 2 (Slots 256-511) ram Base
        UNIT_RAM_BASE_S2 = 0x203E6960
        
        # Morale Data Base Addresses (US Version)
        MORALE_RAM_MAP = {
            "Yellow Turban Rebellion": 0x2036EB52,
            "Hu Lao Gate": 0x2036EC62,
            "Guan Du": 0x2036ED72,
            "Chang Ban": 0x2036EE82,
            "Chi Bi": 0x2036EF92,
            "He Fei": 0x2036F0A2,
            "Yi Ling": 0x2036F1B2,
            "Wu Zhang Plains": 0x2036F2C2
        }

        filename = filedialog.asksaveasfilename(
            defaultextension=".pnach",
            initialfile="5B665C0B.pnach",
            title="Save PNACH File",
            filetypes=[("PNACH Files", "*.pnach")]
        )
        if not filename: return

        try:
            with open(filename, "w") as f:
                f.write(f"// Generated by DW2 Visual Guider\n")
                f.write(f"// Stage: {STAGE_NAMES[self.current_stage_index]}\n\n")

                # Write squad data (Active Slots Only)

                f.write(f"\n// Side 1\n")
                
                # Side 1 (0 - 255)
                base_phys_s1 = UNIT_RAM_BASE_S1 & 0x0FFFFFFF
                count_s1 = 0
                for i in range(256):
                    slot = self.slots[i]
                    
                    # Filter: Skip Empty (255) and Zeroed Slots (0/0/0)
                    # This prevents writing null data for empty bin slots
                    is_active = slot["leader"] != 255
                    is_not_zero = not (slot["leader"] == 0 and slot["x"] == 0 and slot["y"] == 0)
                    
                    if is_active and is_not_zero:
                        # Addr = Base S1 + (Index * 32)
                        current_addr = base_phys_s1 + (i * 32)
                        self._write_slot_pnach(f, slot, current_addr)
                        count_s1 += 1

                f.write(f"\n// Side 2\n")

                # Side 2 (256 - 511)
                base_phys_s2 = UNIT_RAM_BASE_S2 & 0x0FFFFFFF
                count_s2 = 0
                for i in range(256, 512):
                    slot = self.slots[i]
                    
                    # Filter: Skip Empty (255) and Zeroed Slots (0/0/0)
                    is_active = slot["leader"] != 255
                    is_not_zero = not (slot["leader"] == 0 and slot["x"] == 0 and slot["y"] == 0)
                    
                    if is_active and is_not_zero:
                        # Relative Index = i - 256
                        # Addr = Base S2 + (Relative Index * 32)
                        current_addr = base_phys_s2 + ((i - 256) * 32)
                        self._write_slot_pnach(f, slot, current_addr)
                        count_s2 += 1

                # Write Morale Data
                
                stg_name = STAGE_NAMES[self.current_stage_index]
                if stg_name in MORALE_RAM_MAP:
                    f.write(f"\n// Morale Data\n")
                    
                    morale_base_virt = MORALE_RAM_MAP[stg_name]
                    morale_base_phys = morale_base_virt & 0x0FFFFFFF
                    
                    # Side 1
                    s1_values = []
                    for i in range(256):
                         if self.slots[i]["leader"] != 255 and self.slots[i]["own_slot"] == i:
                             s1_values.append(self.slots[i].get("morale", 0))
                    
                    for m_idx, val in enumerate(s1_values):
                        addr = morale_base_phys + (m_idx * 2)
                        f.write(f"patch=1,EE,{addr:08X},short,{val:04X}\n")
                        
                    # Side 2
                    # Starts 0x18 (24 bytes) after Side 1
                    s2_base_phys = morale_base_phys + 0x18
                    
                    s2_values = []
                    for i in range(256, 512):
                        if self.slots[i]["leader"] != 255 and self.slots[i]["own_slot"] == (i - 256):
                            s2_values.append(self.slots[i].get("morale", 0))
                            
                    for m_idx, val in enumerate(s2_values):
                        addr = s2_base_phys + (m_idx * 2)
                        f.write(f"patch=1,EE,{addr:08X},short,{val:04X}\n")

            messagebox.showinfo("Success", f"PNACH generated successfully!\nActive Units: {count_s1} (S1) + {count_s2} (S2)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PNACH:\n{e}")

    def _write_slot_pnach(self, f, slot, addr):
        """Helper to write 32 bytes of a slot to PNACH"""
        b = bytearray(32) 
        for _, key, offset, size in UNIT_DATA_FIELDS:
            val = slot[key]
            max_val = (2**(8*size)) - 1
            val = max(0, min(val, max_val))
            b[offset:offset+size] = val.to_bytes(size, "little")

        for x in range(0, 32, 4):
            chunk_val = int.from_bytes(b[x:x+4], "little")
            chunk_addr = addr + x
            f.write(f"patch=1,EE,{chunk_addr:08X},word,{chunk_val:08X}\n")

    def open_mod_manager(self):
        """Opens the High End Mod Manager"""
        if not self.bin_path:
            messagebox.showwarning("Warning", "Please load DW2.bin first.")
            return
        HighEndModManager(self.root, self.bin_path)

    # Logic for coords and render

    def map_to_canvas(self, mx, my):
        cy = (self.original_height - my) * self.scale
        cx = mx * self.scale
        return cx, cy

    def canvas_to_map(self, cx, cy):
        my = self.original_height - (cy / self.scale)
        mx = cx / self.scale
        return int(mx), int(my)

    def load_image(self, filename):
        path = os.path.join(self.maps_dir, filename)
        if not os.path.exists(path):
            self.base_image = None
            self.canvas.delete("all")
            return
        try:
            pil_img = Image.open(path).convert("RGBA") # Force RGBA for consistent analysis
            
            # Store original image for Pixel Analysis (GA)
            self.current_pil_image = pil_img
            
            self.base_image = ImageTk.PhotoImage(pil_img)
            self.original_width = pil_img.width
            self.original_height = pil_img.height
            self.zoom_level = 1.0
            self.apply_zoom()
        except Exception as e:
            print(f"Failed to load image: {e}")

    def apply_zoom(self):
        if not self.base_image: return
        try:
            path = os.path.join(self.maps_dir, MAP_FILES[self.current_stage_index])
            pil_img = Image.open(path)
            
            new_w = int(self.original_width * self.zoom_level)
            new_h = int(self.original_height * self.zoom_level)
            
            resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.display_image = ImageTk.PhotoImage(resized)
            
            self.scale = self.zoom_level
            
            self.canvas.delete("all")
            self.canvas.config(scrollregion=(0, 0, new_w, new_h))
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
            self.lbl_zoom.config(text=f"{int(self.scale*100)}%")
            self.refresh_markers()
        except:
            pass

    def refresh_markers(self):
        self.canvas.delete("marker")
        self.canvas.delete("guard_vis") # Clear old guards
        
        if not self.slots: return

        # Base "V" Offsets (Relative to North/Up)
        # Left/Right, then wider/further back
        # Y is negative for Up
        BASE_OFFSETS = [
            (-10, 0), (10, 0),      # Flank
            (-15, -10), (15, -10),  # Row 2
            (-20, -20), (20, -20),  # Row 3
            (-25, -30), (25, -30)   # Row 4
        ]

        # Draw markers
        for i, slot in enumerate(self.slots):
            if slot["leader"] == 255 or (slot["x"] == 0 and slot["y"] == 0):
                continue

            cx, cy = self.map_to_canvas(slot["x"], slot["y"])
            
            # Determine Color
            if i in self.selected_indices:
                color = "cyan"
                g_color = "#E0FFFF" # Light Cyan
            else:
                color = "blue" if i < 256 else "red"
                g_color = "#ADD8E6" if i < 256 else "#F08080" # Light Blue/Light Coral

            # Draw Guards (If enabled)
            if self.show_guards_var.get() and slot["guard_cnt"] > 1:
                # Actual guards = count - 1 (Leader included in count)
                actual_guards = max(0, slot["guard_cnt"] - 1)
                count = min(8, actual_guards) 
                
                # Calculate Rotation Angle
                # 0 = North (Up), 2 = East (Right), 4 = South (Down)
                # Angle in Radians = dir * 45 degrees
                # Clockwise rotation formula for screen coords (Y Down)
                direction = slot["dir"]
                rad = math.radians(direction * 45)
                cos_a = math.cos(rad)
                sin_a = math.sin(rad)

                for g_idx in range(count):
                    ox, oy = BASE_OFFSETS[g_idx]
                    
                    # Apply Rotation Matrix
                    # x' = x*cos - y*sin
                    # y' = x*sin + y*cos
                    rx = ox * cos_a - oy * sin_a
                    ry = ox * sin_a + oy * cos_a
                    
                    gx, gy = cx + rx, cy + ry
                    self.canvas.create_oval(gx-2, gy-2, gx+2, gy+2, fill=g_color, outline="", tags="guard_vis")

            # Draw Morale Bar (Chain of Command)
            if self.show_morale_var.get():
                # Use the helper to find the top-level morale
                m_val = self._get_commander_morale(i)

                if m_val > 0:
                    bar_w = 24
                    fill_pct = min(1.0, m_val / 899.0)
                    fill_px = int(bar_w * fill_pct)
                    
                    bar_color = "blue" if i < 256 else "red"
                    
                    by = cy - 18
                    bx_start = cx - (bar_w / 2)
                    bx_end = bx_start + bar_w
                    
                    # Background
                    self.canvas.create_line(bx_start, by, bx_end, by, 
                                            width=6, fill="#444", capstyle=tk.ROUND, tags="marker")
                    # Foreground
                    if fill_px > 0:
                        self.canvas.create_line(bx_start, by, bx_start + fill_px, by, 
                                                width=4, fill=bar_color, capstyle=tk.ROUND, tags="marker")

            # Draw Leader
            tags = ("marker", f"slot_{i}")
            self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=color, outline="white", width=2, tags=tags)
            self.canvas.create_text(cx, cy-10, text=str(slot["leader"]), fill="white", font=("Arial", 8, "bold"), tags=tags)

    def _update_global_morale(self):
        """Calculates total morale for both sides and draws the balance bar"""
        if not self.slots: return

        # Calculate Totals (Only count Force Leaders)
        total_s1 = 0
        total_s2 = 0
        
        # Side 1 (0-255)
        for i in range(256):
            s = self.slots[i]
            if s["leader"] != 255 and s["own_slot"] == i:
                total_s1 += s.get("morale", 0)
                
        # Side 2 (256-511), relative indexing
        for i in range(256, 512):
            s = self.slots[i]
            if s["leader"] != 255:
                # If I am slot 300, my own_slot is 44 (300-256)
                target_self = i - 256
                if s["own_slot"] == target_self:
                    total_s2 += s.get("morale", 0)

        # Draw Bar
        self.morale_canvas.delete("all")
        w = 300
        h = 30
        
        total = total_s1 + total_s2
        if total == 0:
            # Draw Gray Neutral Bar
            self.morale_canvas.create_rectangle(0, 0, w, h, fill="#555555", width=0)
            self.morale_canvas.create_text(w/2, h/2, text="No Morale Data", fill="white", font=("Arial", 8))
            return

        # Calculate Split
        # If S1 has 1000 and S2 has 1000, ratio is 0.5 -> Midpoint at w/2
        ratio = total_s1 / total
        mid_x = int(w * ratio)
        
        # Draw Blue Side (Left)
        if mid_x > 0:
            self.morale_canvas.create_rectangle(0, 0, mid_x, h, fill="blue", width=0)
            # Text S1
            if mid_x > 40:
                self.morale_canvas.create_text(10, h/2, text=f"{total_s1}", anchor="w", fill="white", font=("Arial", 9, "bold"))

        # Draw Red Side (Right)
        if mid_x < w:
            self.morale_canvas.create_rectangle(mid_x, 0, w, h, fill="red", width=0)
            # Text S2
            if (w - mid_x) > 40:
                self.morale_canvas.create_text(w-10, h/2, text=f"{total_s2}", anchor="e", fill="white", font=("Arial", 9, "bold"))
        
        # Draw Divider Line
        self.morale_canvas.create_line(mid_x, 0, mid_x, h, fill="white", width=2)
        
    def update_caps(self):
        s1 = sum(1 for i in range(0, 256) if self.slots[i]["leader"] != 255 and not (self.slots[i]["x"] == 0 and self.slots[i]["y"] == 0))
        s2 = sum(1 for i in range(256, 512) if self.slots[i]["leader"] != 255 and not (self.slots[i]["x"] == 0 and self.slots[i]["y"] == 0))
        self.lbl_cap_s1.config(text=f"Side 1 (Blue): {s1}/256")
        self.lbl_cap_s2.config(text=f"Side 2 (Red): {s2}/256")
    
    # Zoom and Panning

    def get_view_center_in_map_coords(self):
        if not self.base_image: return 400, 400
        x0 = self.canvas.canvasx(0)
        y0 = self.canvas.canvasy(0)
        vw = self.canvas.winfo_width()
        vh = self.canvas.winfo_height()
        cx = x0 + vw / 2
        cy = y0 + vh / 2
        return self.canvas_to_map(cx, cy)

    def center_on_map_coord(self, mx, my):
        if not self.base_image: return
        cx, cy = self.map_to_canvas(mx, my)
        full_w = self.original_width * self.scale
        full_h = self.original_height * self.scale
        vw = self.canvas.winfo_width()
        vh = self.canvas.winfo_height()
        target_x = cx - vw / 2
        target_y = cy - vh / 2
        if full_w > 0: self.canvas.xview_moveto(target_x / full_w)
        if full_h > 0: self.canvas.yview_moveto(target_y / full_h)

    def zoom_in(self):
        if not self.base_image: return
        mx, my = self.get_view_center_in_map_coords()
        self.zoom_level += 0.5
        self.apply_zoom()
        self.center_on_map_coord(mx, my)

    def zoom_out(self):
        if not self.base_image or self.zoom_level <= 0.5: return
        mx, my = self.get_view_center_in_map_coords()
        self.zoom_level -= 0.5
        self.apply_zoom()
        self.center_on_map_coord(mx, my)

    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # Interaction: Selection and Drag

    def on_stage_changed(self, event):
        self.load_stage_data(self.stage_combo.current())

    def on_left_press(self, event):

        # Check if clicked on a marker
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(cx-5, cy-5, cx+5, cy+5)
        
        clicked_unit_idx = None
        for item in items:
            for t in self.canvas.gettags(item):
                if t.startswith("slot_"):
                    clicked_unit_idx = int(t.split("_")[1])
                    break
            if clicked_unit_idx is not None: break

        # Logic
        ctrl_pressed = (event.state & 0x4) != 0 # Check ctrl key
        
        if clicked_unit_idx is not None:
            # Clicked a unit
            if ctrl_pressed:
                # Toggle
                if clicked_unit_idx in self.selected_indices:
                    self.selected_indices.remove(clicked_unit_idx)
                else:
                    self.selected_indices.add(clicked_unit_idx)
            else:
                # If unit is already selected don't clear immediately (might drag)
                if clicked_unit_idx not in self.selected_indices:
                    self.selected_indices.clear()
                    self.selected_indices.add(clicked_unit_idx)
            
            self._update_editor_panel()
            self.refresh_markers()
            self.refresh_listbox_selection()
            self.dragging_unit_idx = clicked_unit_idx # Prepare drag
        else:
            # Clicked empty space -> Start Selection Box
            if not ctrl_pressed:
                self.selected_indices.clear()
            self.drag_start_x = cx
            self.drag_start_y = cy
            self.drag_rect_id = self.canvas.create_rectangle(cx, cy, cx, cy, outline="cyan", width=2)

    def on_left_drag(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)

        # Mode A: Dragging Units
        if self.dragging_unit_idx is not None:
            mx, my = self.canvas_to_map(cx, cy)
            mx, my = max(0, min(800, mx)), max(0, min(800, my))
            
            # Calculate delta for the leader of the drag
            main_slot = self.slots[self.dragging_unit_idx]
            dx = mx - main_slot["x"]
            dy = my - main_slot["y"]
            
            # Move all selected units by delta
            for idx in self.selected_indices:
                s = self.slots[idx]
                s["x"] = max(0, min(800, s["x"] + dx))
                s["y"] = max(0, min(800, s["y"] + dy))
            
            self._update_editor_panel()
            self.refresh_markers()
        
        # Mode B: Selection Box
        elif self.drag_rect_id:
            self.canvas.coords(self.drag_rect_id, self.drag_start_x, self.drag_start_y, cx, cy)

    def on_left_release(self, event):
        # Finalize Box Selection
        if self.drag_rect_id:
            x1, y1, x2, y2 = self.canvas.coords(self.drag_rect_id)
            self.canvas.delete(self.drag_rect_id)
            self.drag_rect_id = None
            
            # Normalize coords
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            
            # Find units in box
            items = self.canvas.find_enclosed(x_min, y_min, x_max, y_max)
            # Let's iterate slots and check canvas coords manually for precision
            for i, slot in enumerate(self.slots):
                if slot["leader"] == 255: continue
                cx, cy = self.map_to_canvas(slot["x"], slot["y"])
                if x_min <= cx <= x_max and y_min <= cy <= y_max:
                    self.selected_indices.add(i)
            
            self._update_editor_panel()
            self.refresh_markers()
            self.refresh_listbox_selection()

        self.dragging_unit_idx = None

    def _get_commander_morale(self, unit_idx):
        """
        Recursively climbs the chain of command to find the Force Leader's morale
        Prevents infinite loops with a safety counter
        """
        current_idx = unit_idx
        
        # Max 5 hops to prevent infinite loops (A->B->A)
        for _ in range(5):
            if current_idx < 0 or current_idx >= len(self.slots):
                return 0
                
            slot = self.slots[current_idx]
            serves_rel = slot["own_slot"]
            
            # Convert Relative Serves Index to Absolute Index
            # If I am on Side 2 (index 300), Serves 0 means I serve Slot 256
            base_offset = 0 if current_idx < 256 else 256
            target_abs = base_offset + serves_rel
            
            # Check: Am I serving myself? (I am the Force Leader)
            if target_abs == current_idx:
                return slot.get("morale", 0)
            
            # Climb the ladder: Look at who I serve next
            current_idx = target_abs
            
        return 0 # Failed to find a leader within 5 hops

    # Squad Editor Logic
 
    def _update_editor_panel(self):
        count = len(self.selected_indices)
        if count == 0:
            self.lbl_selected.config(text="No Selection", fg="gray")
            for var in self.entry_vars.values(): var.set("")
            return
        elif count == 1:
            idx = list(self.selected_indices)[0]
            name = get_unit_name(self.slots[idx]["leader"])
            self.lbl_selected.config(text=f"Slot {idx} | {name}", fg="black")
        else:
            self.lbl_selected.config(text=f"Squad Selection: {count} Units", fg="purple")

        first_idx = list(self.selected_indices)[0]
        ref_slot = self.slots[first_idx]

        # Map keys to the lookup lists
        lookup_map = {
            "dir": UNIT_DIR,
            "type": UNIT_TYPES,
            "ai_type": AI_TYPES,
            "orders": ORDER_TYPES
        }

        for _, key, _, _ in UNIT_DATA_FIELDS:
            is_mixed = False
            ref_val = ref_slot[key]
            
            for idx in self.selected_indices:
                if self.slots[idx][key] != ref_val:
                    is_mixed = True
                    break
            
            if is_mixed:
                self.entry_vars[key].set("<Mixed>")
            else:
                # Format string: "Name: Value"
                final_str = str(ref_val)
                if key in lookup_map:
                    for name, val in lookup_map[key]:
                        if val == ref_val:
                            final_str = f"{name}: {val}"
                            break
                self.entry_vars[key].set(final_str)
                
        # Morale Field Logic (Chain of Command)
        idx = list(self.selected_indices)[0]
        s = self.slots[idx]
        serves = s["own_slot"]
        
        # Calculate target_self to see if I am editable
        target_self = idx if idx < 256 else (idx - 256)
        
        if serves == target_self:
            # I am the Force Leader -> Editable
            current_morale = s.get("morale", 0)
            self.entry_morale.config(state="normal")
            self.var_morale.set(str(current_morale))
        else:
            # I serve someone else -> Read-Only look at top Commander
            eff_morale = self._get_commander_morale(idx)
            self.var_morale.set(f"{eff_morale} (Linked)")
            self.entry_morale.config(state="disabled")

    def update_selected_unit_data(self):
        if not self.selected_indices: return
        
        try:
            for _, key, _, size in UNIT_DATA_FIELDS:
                if key in self.entry_vars:
                    val_str = self.entry_vars[key].get()
                    
                    if val_str == "<Mixed>" or val_str == "":
                        continue
                    
                    # Parsing Logic
                    # If format is "String: Value", split by colon and take the last part
                    if ":" in val_str:
                        # "North: 0" -> takes " 0" -> int(0)
                        clean_str = val_str.split(":")[-1].strip()
                        val = int(clean_str)
                    elif "(" in val_str and ")" in val_str:
                        # Fallback for "Name (Value)" if user typed that
                        clean_str = val_str.split("(")[-1].strip(")")
                        val = int(clean_str)
                    else:
                        # Raw integer input
                        val = int(val_str)

                    binary_limit = (2**(8*size)) - 1
                    custom_limit = UNIT_LIMITS.get(key, binary_limit)
                    limit = min(custom_limit, binary_limit)
                    val = max(0, min(val, limit))
                    
                    for idx in self.selected_indices:
                        self.slots[idx][key] = val

            # Save Morale (Only if editable)
            if self.entry_morale["state"] == "normal":
                try:
                    val = int(self.var_morale.get())
                    # Clamp input to 899
                    val = max(0, min(899, val)) 
                    for idx in self.selected_indices:
                        self.slots[idx]["morale"] = val
                except: pass
                    
            self.refresh_markers()
            self.refresh_listbox() 
            self._update_editor_panel() 
            self.update_caps()
            self._update_global_morale()
            messagebox.showinfo("Updated", f"Updated {len(self.selected_indices)} units.")
            
        except ValueError:
            messagebox.showerror("Error", "Could not read value.\nEnsure format is 'Name: Integer' or just 'Integer'.")
    def delete_selected_unit(self):
        if not self.selected_indices: return
        if messagebox.askyesno("Delete", f"Delete {len(self.selected_indices)} units?"):
            for idx in self.selected_indices:
                self.slots[idx]["leader"] = 255
            
            self.selected_indices.clear()
            self._update_editor_panel()
            self.refresh_markers()
            self.refresh_listbox()
            self.update_caps()
            self._update_global_morale()

    def add_unit(self, side):
        if not self.slots: return
        start, end = (0, 256) if side == 1 else (256, 512)
        
        for i in range(start, end):
            if self.slots[i]["leader"] == 255 or (self.slots[i]["x"] == 0 and self.slots[i]["y"] == 0):
                new_data = {
                    "leader": 0, "type": 0, "life": 200, "x": 400, "y": 400,
                    "dir": 0, "path": 0, "gate_mode": 0, "guard_id": 0, "atk": 10, "def": 10,
                    "guard_cnt": 0, "own_slot": i, "ai_type": 0, "orders": 0, "hidden": 0,
                    "target": 255, "drop": 0, "ai_lvl": 0, "delay": 0, "points": 0
                }
                self.slots[i].update(new_data)
                
                self.selected_indices.clear()
                self.selected_indices.add(i)
                self._update_editor_panel()
                self.refresh_markers()
                self.refresh_listbox()
                self.update_caps()
                self.center_on_map_coord(400, 400)
                self._update_global_morale()
                return
        messagebox.showwarning("Full", f"No empty slots available for Side {side}!")

    def filter_list(self, *args):
        self.refresh_listbox()
    
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        self.list_map = [] 
        if not self.slots: return
        filter_txt = self.var_search.get().lower()
        
        indices_to_select = []
        
        row_idx = 0
        for i, slot in enumerate(self.slots):
            if slot["leader"] == 255 or (slot["x"] == 0 and slot["y"] == 0):
                continue
                
            side = "S1" if i < 256 else "S2"
            name = get_unit_name(slot["leader"])
            display_text = f"[{side} | {i}] {name} ({slot['x']}, {slot['y']})"
            
            if filter_txt and filter_txt not in display_text.lower(): continue
            
            self.listbox.insert(tk.END, display_text)
            self.list_map.append(i)
            
            if i in self.selected_indices:
                indices_to_select.append(row_idx)
            row_idx += 1
            
        for r in indices_to_select:
            self.listbox.selection_set(r)

    def refresh_listbox_selection(self):
        self.listbox.selection_clear(0, tk.END)
        if not self.selected_indices: return
        
        first_view = None
        for i, slot_idx in enumerate(self.list_map):
            if slot_idx in self.selected_indices:
                self.listbox.selection_set(i)
                if first_view is None: first_view = i
        
        if first_view is not None:
            self.listbox.see(first_view)

    def on_listbox_select(self, event):
        sel_rows = self.listbox.curselection()
        if not sel_rows: return
        
        self.selected_indices.clear()
        for row in sel_rows:
            slot_idx = self.list_map[row]
            self.selected_indices.add(slot_idx)
            
        self._update_editor_panel()
        self.refresh_markers()
        
        if self.selected_indices:
            last = list(self.selected_indices)[-1]
            self.center_on_map_coord(self.slots[last]["x"], self.slots[last]["y"])

    # Stat Randomizer
    def open_stat_randomizer(self):
        if not self.slots: return
        
        # Create a custom popup window
        top = tk.Toplevel(self.root)
        top.title("Stat Randomizer")
        top.geometry("300x300")
        top.resizable(False, False)
        
        tk.Label(top, text="Set Random Ranges (Min - Max)", font=("Arial", 10, "bold")).pack(pady=10)
        
        input_frame = tk.Frame(top)
        input_frame.pack(pady=5)
        
        # Helper to create input rows
        entries = {}
        def make_row(row, key, label, def_min, def_max):
            tk.Label(input_frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="e")
            e1 = tk.Entry(input_frame, width=6); e1.insert(0, str(def_min)); e1.grid(row=row, column=1)
            tk.Label(input_frame, text="-").grid(row=row, column=2)
            e2 = tk.Entry(input_frame, width=6); e2.insert(0, str(def_max)); e2.grid(row=row, column=3)
            entries[key] = (e1, e2)

        # Define fields to randomize
        make_row(0, "life", "Life:", 20, 400)
        make_row(1, "atk", "Attack:", 1, 255)
        make_row(2, "def", "Defense:", 1, 255)
        make_row(3, "ai_lvl", "AI Level:", 1, 255)

        def apply_randomization():
            try:
                # Parse limits
                ranges = {}
                for key, (e_min, e_max) in entries.items():
                    ranges[key] = (int(e_min.get()), int(e_max.get()))
                
                if not messagebox.askyesno("Confirm", "This will randomize stats for all units on the map.\nContinue?"):
                    return
                
                count = 0
                for s in self.slots:
                    # Skip empty slots
                    if s["leader"] == 255: continue
                    
                    # Apply Randoms
                    for key, (r_min, r_max) in ranges.items():
                        # Handle constraints
                        val = random.randint(min(r_min, r_max), max(r_min, r_max))
                        
                        # Special clamp for byte sized fields
                        if key in ["atk", "def", "ai_lvl"]:
                            val = max(0, min(255, val))
                        elif key == "life":
                            val = max(0, min(400, val))
                            
                        s[key] = val
                    
                    count += 1
                
                self.refresh_markers()
                self._update_editor_panel()
                self.refresh_listbox()
                messagebox.showinfo("Success", f"Randomized stats for {count} squads!")
                top.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers for all ranges.")

        # Apply Button
        tk.Button(top, text="Randomize Stats", command=apply_randomization, 
                  bg="#FF69B4", font=("Arial", 10, "bold"), width=15).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = DW2CoordinateGuider(root)
    root.mainloop()
