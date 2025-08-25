from BaseClasses import Location

class PTLocation(Location):
    game: str = "Pizza Tower"

pt_locations = { #TODO allow pumpkins to be checks eventually maybe
    #basics

#John Gutter
    "John Gutter Complete": 100,
    "John Gutter Mushroom Toppin": 101,
    "John Gutter Cheese Toppin": 102,
    "John Gutter Tomato Toppin": 103,
    "John Gutter Sausage Toppin": 104,
    "John Gutter Pineapple Toppin": 105,

#Pizzascape
    "Pizzascape Complete": 106,
    "Pizzascape Mushroom Toppin": 107,
    "Pizzascape Cheese Toppin": 108,
    "Pizzascape Tomato Toppin": 109,
    "Pizzascape Sausage Toppin": 110,
    "Pizzascape Pineapple Toppin": 111,

#Ancient Cheese
    "Ancient Cheese Complete": 112,
    "Ancient Cheese Mushroom Toppin": 113,
    "Ancient Cheese Cheese Toppin": 114,
    "Ancient Cheese Tomato Toppin": 115,
    "Ancient Cheese Sausage Toppin": 116,
    "Ancient Cheese Pineapple Toppin": 117,

#Bloodsauce Dungeon
    "Bloodsauce Dungeon Complete": 118,
    "Bloodsauce Dungeon Mushroom Toppin": 119,
    "Bloodsauce Dungeon Cheese Toppin": 120,
    "Bloodsauce Dungeon Tomato Toppin": 121,
    "Bloodsauce Dungeon Sausage Toppin": 122,
    "Bloodsauce Dungeon Pineapple Toppin": 123,

#Oregano Desert
    "Oregano Desert Complete": 124,
    "Oregano Desert Mushroom Toppin": 125,
    "Oregano Desert Cheese Toppin": 126,
    "Oregano Desert Tomato Toppin": 127,
    "Oregano Desert Sausage Toppin": 128,
    "Oregano Desert Pineapple Toppin": 129,

#Wasteyard
    "Wasteyard Complete": 130,
    "Wasteyard Mushroom Toppin": 131,
    "Wasteyard Cheese Toppin": 132,
    "Wasteyard Tomato Toppin": 133,
    "Wasteyard Sausage Toppin": 134,
    "Wasteyard Pineapple Toppin": 135,

#Fun Farm
    "Fun Farm Complete": 136,
    "Fun Farm Mushroom Toppin": 137,
    "Fun Farm Cheese Toppin": 138,
    "Fun Farm Tomato Toppin": 139,
    "Fun Farm Sausage Toppin": 140,
    "Fun Farm Pineapple Toppin": 141,

#Fastfood Saloon
    "Fastfood Saloon Complete": 142,
    "Fastfood Saloon Mushroom Toppin": 143,
    "Fastfood Saloon Cheese Toppin": 144,
    "Fastfood Saloon Tomato Toppin": 145,
    "Fastfood Saloon Sausage Toppin": 146,
    "Fastfood Saloon Pineapple Toppin": 147,

#Crust Cove
    "Crust Cove Complete": 148,
    "Crust Cove Mushroom Toppin": 149,
    "Crust Cove Cheese Toppin": 150,
    "Crust Cove Tomato Toppin": 151,
    "Crust Cove Sausage Toppin": 152,
    "Crust Cove Pineapple Toppin": 153,

#Gnome Forest
    "Gnome Forest Complete": 154,
    "Gnome Forest Mushroom Toppin": 155,
    "Gnome Forest Cheese Toppin": 156,
    "Gnome Forest Tomato Toppin": 157,
    "Gnome Forest Sausage Toppin": 158,
    "Gnome Forest Pineapple Toppin": 159,

#Deep-Dish 9
    "Deep-Dish 9 Complete": 160,
    "Deep-Dish 9 Mushroom Toppin": 161,
    "Deep-Dish 9 Cheese Toppin": 162,
    "Deep-Dish 9 Tomato Toppin": 163,
    "Deep-Dish 9 Sausage Toppin": 164,
    "Deep-Dish 9 Pineapple Toppin": 165,

#GOLF
    "GOLF Complete": 166,
    "GOLF Mushroom Toppin": 167,
    "GOLF Cheese Toppin": 168,
    "GOLF Tomato Toppin": 169,
    "GOLF Sausage Toppin": 170,
    "GOLF Pineapple Toppin": 171,

#The Pig City
    "The Pig City Complete": 172,
    "The Pig City Mushroom Toppin": 173,
    "The Pig City Cheese Toppin": 174,
    "The Pig City Tomato Toppin": 175,
    "The Pig City Sausage Toppin": 176,
    "The Pig City Pineapple Toppin": 177,

#Peppibot Factory
    "Peppibot Factory Complete": 178,
    "Peppibot Factory Mushroom Toppin": 179,
    "Peppibot Factory Cheese Toppin": 180,
    "Peppibot Factory Tomato Toppin": 181,
    "Peppibot Factory Sausage Toppin": 182,
    "Peppibot Factory Pineapple Toppin": 183,

#Oh Shit!
    "Oh Shit! Complete": 184,
    "Oh Shit! Mushroom Toppin": 185,
    "Oh Shit! Cheese Toppin": 186,
    "Oh Shit! Tomato Toppin": 187,
    "Oh Shit! Sausage Toppin": 188,
    "Oh Shit! Pineapple Toppin": 189,

#Freezerator
    "Freezerator Complete": 190,
    "Freezerator Mushroom Toppin": 191,
    "Freezerator Cheese Toppin": 192,
    "Freezerator Tomato Toppin": 193,
    "Freezerator Sausage Toppin": 194,
    "Freezerator Pineapple Toppin": 195,

#Pizzascare
    "Pizzascare Complete": 196,
    "Pizzascare Mushroom Toppin": 197,
    "Pizzascare Cheese Toppin": 198,
    "Pizzascare Tomato Toppin": 199,
    "Pizzascare Sausage Toppin": 200,
    "Pizzascare Pineapple Toppin": 201,

#Don't Make A Sound
    "Don't Make A Sound Complete": 202,
    "Don't Make A Sound Mushroom Toppin": 203,
    "Don't Make A Sound Cheese Toppin": 204,
    "Don't Make A Sound Tomato Toppin": 205,
    "Don't Make A Sound Sausage Toppin": 206,
    "Don't Make A Sound Pineapple Toppin": 207,

#WAR
    "WAR Complete": 208,
    "WAR Mushroom Toppin": 209,
    "WAR Cheese Toppin": 210,
    "WAR Tomato Toppin": 211,
    "WAR Sausage Toppin": 212,
    "WAR Pineapple Toppin": 213,

#Crumbling Tower of Pizza
    "The Crumbling Tower of Pizza Complete": 214,

#Bosses
    "Pepperman Defeated": 215,
    "The Vigilante Defeated": 216,
    "The Noise Defeated": 217,
    "Fake Peppino Defeated": 218,
    "Pizzaface Defeated": 219,

#misc
    "Snotty Murdered": 220,

#Tutorial
    "Tutorial Complete": 221,
    "Tutorial Complete in under 2 minutes": 222,
    "Tutorial Mushroom Toppin": 223,
    "Tutorial Cheese Toppin": 224,
    "Tutorial Tomato Toppin": 225,
    "Tutorial Sausage Toppin": 226,
    "Tutorial Pineapple Toppin": 227,
    
    #s ranks

    #Levels
    "John Gutter S Rank": 228,
    "Pizzascape S Rank": 229,
    "Ancient Cheese S Rank": 230,
    "Bloodsauce Dungeon S Rank": 231,
    "Oregano Desert S Rank": 232,
    "Wasteyard S Rank": 233,
    "Fun Farm S Rank": 234,
    "Fastfood Saloon S Rank": 235,
    "Crust Cove S Rank": 236,
    "Gnome Forest S Rank": 237,
    "Deep-Dish 9 S Rank": 238,
    "GOLF S Rank": 239,
    "The Pig City S Rank": 240,
    "Peppibot Factory S Rank": 241,
    "Oh Shit! S Rank": 242,
    "Freezerator S Rank": 243,
    "Pizzascare S Rank": 244,
    "Don't Make A Sound S Rank": 245,
    "WAR S Rank": 246,
    "The Crumbling Tower of Pizza S Rank": 247,

    #Bosses
    "Pepperman S Rank": 248,
    "The Vigilante S Rank": 249,
    "The Noise S Rank": 250,
    "Fake Peppino S Rank": 251,

    #secrets 

    #John Gutter
    "John Gutter Secret 1": 252,
    "John Gutter Secret 2": 253,
    "John Gutter Secret 3": 254,

    #Pizzascape
    "Pizzascape Secret 1": 255,
    "Pizzascape Secret 2": 256,
    "Pizzascape Secret 3": 257,

    #Ancient Cheese
    "Ancient Cheese Secret 1": 258,
    "Ancient Cheese Secret 2": 259,
    "Ancient Cheese Secret 3": 260,

    #Bloodsauce Dungeon
    "Bloodsauce Dungeon Secret 1": 261,
    "Bloodsauce Dungeon Secret 2": 262,
    "Bloodsauce Dungeon Secret 3": 263,

    #Oregano Desert
    "Oregano Desert Secret 1": 264,
    "Oregano Desert Secret 2": 265,
    "Oregano Desert Secret 3": 266,

    #Wasteyard
    "Wasteyard Secret 1": 267,
    "Wasteyard Secret 2": 268,
    "Wasteyard Secret 3": 269,

    #Fun Farm
    "Fun Farm Secret 1": 270,
    "Fun Farm Secret 2": 271,
    "Fun Farm Secret 3": 272,

    #Fastfood Saloon
    "Fastfood Saloon Secret 1": 273,
    "Fastfood Saloon Secret 2": 274,
    "Fastfood Saloon Secret 3": 275,

    #Crust Cove
    "Crust Cove Secret 1": 276,
    "Crust Cove Secret 2": 277,
    "Crust Cove Secret 3": 278,

    #Gnome Forest
    "Gnome Forest Secret 1": 279,
    "Gnome Forest Secret 2": 280,
    "Gnome Forest Secret 3": 281,

    #Deep-Dish 9
    "Deep-Dish 9 Secret 1": 282,
    "Deep-Dish 9 Secret 2": 283,
    "Deep-Dish 9 Secret 3": 284,

    #GOLF
    "GOLF Secret 1": 285,
    "GOLF Secret 2": 286,
    "GOLF Secret 3": 287,

    #The Pig City
    "The Pig City Secret 1": 288,
    "The Pig City Secret 2": 289,
    "The Pig City Secret 3": 290,

    #Peppibot Factory
    "Peppibot Factory Secret 1": 291,
    "Peppibot Factory Secret 2": 292,
    "Peppibot Factory Secret 3": 293,

    #Oh Shit!
    "Oh Shit! Secret 1": 294,
    "Oh Shit! Secret 2": 295,
    "Oh Shit! Secret 3": 296,

    #Freezerator
    "Freezerator Secret 1": 297,
    "Freezerator Secret 2": 298,
    "Freezerator Secret 3": 299,

    #Pizzascare
    "Pizzascare Secret 1": 300,
    "Pizzascare Secret 2": 301,
    "Pizzascare Secret 3": 302,

    #Don't Make A Sound
    "Don't Make A Sound Secret 1": 303,
    "Don't Make A Sound Secret 2": 304,
    "Don't Make A Sound Secret 3": 305,

    #WAR
    "WAR Secret 1": 306,
    "WAR Secret 2": 307,
    "WAR Secret 3": 308,

    #p ranks

    #Levels
    "John Gutter P Rank": 309,
    "Pizzascape P Rank": 310,
    "Ancient Cheese P Rank": 311,
    "Bloodsauce Dungeon P Rank": 312,
    "Oregano Desert P Rank": 313,
    "Wasteyard P Rank": 314,
    "Fun Farm P Rank": 315,
    "Fastfood Saloon P Rank": 316,
    "Crust Cove P Rank": 317,
    "Gnome Forest P Rank": 318,
    "Deep-Dish 9 P Rank": 319,
    "GOLF P Rank": 320,
    "The Pig City P Rank": 321,
    "Peppibot Factory P Rank": 322,
    "Oh Shit! P Rank": 323,
    "Freezerator P Rank": 324,
    "Pizzascare P Rank": 325,
    "Don't Make A Sound P Rank": 326,
    "WAR P Rank": 327,
    "The Crumbling Tower of Pizza P Rank": 328,

    #Bosses
    "Pepperman P Rank": 329,
    "The Vigilante P Rank": 330,
    "The Noise P Rank": 331,
    "Fake Peppino P Rank": 332,

    #cheftasks

    #John Gutter
    "Chef Task: John Gutted": 333,
    "Chef Task: Let's Make This Quick": 334,
    "Chef Task: Primate Rage": 335,

    #Pizzascape
    "Chef Task: Shining Armor": 336,
    "Chef Task: Spoonknight": 337,
    "Chef Task: Spherical": 338,

    #Ancient Cheese
    "Chef Task: Thrill Seeker": 339,
    "Chef Task: Volleybomb": 340,
    "Chef Task: Delicacy": 341,

    #Bloodsauce Dungeon
    "Chef Task: Very Very Hot Sauce": 342,
    "Chef Task: Eruption Man": 343,
    "Chef Task: Unsliced Pizzaman": 344,

    #Oregano Desert
    "Chef Task: Peppino's Rain Dance": 345,
    "Chef Task: Unnecessary Violence": 346,
    "Chef Task: Alien Cow": 347,

    #Wasteyard
    "Chef Task: Ghosted": 348,
    "Chef Task: Pretend Ghost": 349,
    "Chef Task: Alive and Well": 350,

    #Fun Farm
    "Chef Task: No One Is Safe": 351,
    "Chef Task: Cube Menace": 352,
    "Chef Task: Good Egg": 353,

    #Fastfood Saloon
    "Chef Task: Non-Alcoholic": 354,
    "Chef Task: Already Pressed": 355,
    "Chef Task: Royal Flush": 356,

    #Crust Cove
    "Chef Task: Blowback": 357,
    "Chef Task: X": 358,
    "Chef Task: Demolition Expert": 359,

    #Gnome Forest
    "Chef Task: Bee Nice": 360,
    "Chef Task: Lumberjack": 361,
    "Chef Task: Bullseye": 362,

    #Deep-Dish 9
    "Chef Task: Turbo Tunnel": 363,
    "Chef Task: Blast 'Em Asteroids": 364,
    "Chef Task: Man Meteor": 365,

    #GOLF
    "Chef Task: Primo Golfer": 366,
    "Chef Task: Nice Shot": 367,
    "Chef Task: Helpful Burger": 368,

    #The Pig City
    "Chef Task: Pan Fried": 369,
    "Chef Task: Strike!": 370,
    "Chef Task: Say Oink!": 371,

    #Peppibot Factory
    "Chef Task: Unflattening": 372,
    "Chef Task: Whoop This!": 373,
    "Chef Task: There Can Be Only One": 374,

    #Oh Shit!
    "Chef Task: Can't Fool Me": 375,
    "Chef Task: Food Clan": 376,
    "Chef Task: Penny Pincher": 377,

    #Freezerator
    "Chef Task: Frozen Nuggets": 378,
    "Chef Task: Season's Greetings": 379,
    "Chef Task: Ice Climber": 380,

    #Pizzascare
    "Chef Task: Cross To Bare": 381,
    "Chef Task: Haunted Playground": 382,
    "Chef Task: Skullsplitter": 383,

    #Don't Make A Sound
    "Chef Task: And This... Is My Gun On A Stick!": 384,
    "Chef Task: Let Them Sleep": 385,
    "Chef Task: Jumpspared": 386,

    #WAR
    "Chef Task: Decorated Veteran": 387,
    "Chef Task: Sharpshooter": 388,
    "Chef Task: Trip to the Warzone": 389,

    #Floor Tasks
    "Chef Task: S Ranked #1": 390,
    "Chef Task: P Ranked #1": 391,
    "Chef Task: S Ranked #2": 392,
    "Chef Task: P Ranked #2": 393,
    "Chef Task: S Ranked #3": 394,
    "Chef Task: P Ranked #3": 395,
    "Chef Task: S Ranked #4": 396,
    "Chef Task: P Ranked #4": 397,
    "Chef Task: S Ranked #5": 398,
    "Chef Task: P Ranked #5": 399,

    #Boss Tasks
    "Chef Task: The Critic": 400,
    "Chef Task: The Ugly": 401,
    "Chef Task: Denoise": 402,
    "Chef Task: Faker": 403,
    "Chef Task: Face Off": 404,

    #treasures
    "John Gutter Treasure": 405,
    "Pizzascape Treasure": 406,
    "Ancient Cheese Treasure": 407,
    "Bloodsauce Dungeon Treasure": 408,
    "Oregano Desert Treasure": 409,
    "Wasteyard Treasure": 410,
    "Fun Farm Treasure": 411,
    "Fastfood Saloon Treasure": 412,
    "Crust Cove Treasure": 413,
    "Gnome Forest Treasure": 414,
    "Deep-Dish 9 Treasure": 415,
    "GOLF Treasure": 416,
    "The Pig City Treasure": 417,
    "Peppibot Factory Treasure": 418,
    "Oh Shit! Treasure": 419,
    "Freezerator Treasure": 420,
    "Pizzascare Treasure": 421,
    "Don't Make A Sound Treasure": 422,
    "WAR Treasure": 423,

    #doise
    "The Doise Defeated": 424,
    "The Doise S Rank": 425,
    "The Doise P Rank": 426,

    #pumpkins
    "John Gutter Pumpkin": 427,
    "Pizzascape Pumpkin": 428,
    "Ancient Cheese Pumpkin": 429,
    "Bloodsauce Dungeon Pumpkin": 430,
    "Oregano Desert Pumpkin": 431,
    "Wasteyard Pumpkin": 432,
    "Fun Farm Pumpkin": 433,
    "Fastfood Saloon Pumpkin": 434,
    "Crust Cove Pumpkin": 435,
    "Gnome Forest Pumpkin": 436,
    "Deep-Dish 9 Pumpkin": 437,
    "GOLF Pumpkin": 438,
    "The Pig City Pumpkin": 439,
    "Peppibot Factory Pumpkin": 440,
    "Oh Shit! Pumpkin": 441,
    "Freezerator Pumpkin": 442,
    "Pizzascare Pumpkin": 443,
    "Don't Make A Sound Pumpkin": 444,
    "WAR Pumpkin": 445,
    "The Crumbling Tower of Pizza Pumpkin": 446,
    "Tricky Treat Main Path Pumpkin 1": 447,
    "Tricky Treat Main Path Pumpkin 2": 448,
    "Tricky Treat Main Path Pumpkin 3": 449,
    "Tricky Treat Main Path Pumpkin 4": 450,
    "Tricky Treat Main Path Pumpkin 5": 451,
    "Tricky Treat Side Path Pumpkin 1": 452,
    "Tricky Treat Side Path Pumpkin 2": 453,
    "Tricky Treat Side Path Pumpkin 3": 454,
    "Tricky Treat Side Path Pumpkin 4": 455,
    "Tricky Treat Side Path Pumpkin 5": 456,

    "Chef Task: Pumpkin Munchkin": 457,
    "Chef Task: Tricksy": 458,
}

# location groups definition starts here

levels_list = [ #ctop handled separately
    "John Gutter",
    "Pizzascape",
    "Ancient Cheese",
    "Bloodsauce Dungeon",
    "Oregano Desert",
    "Wasteyard",
    "Fun Farm",
    "Fastfood Saloon",
    "Crust Cove",
    "Gnome Forest",
    "Deep-Dish 9",
    "GOLF",
    "The Pig City",
    "Peppibot Factory",
    "Oh Shit!",
    "Freezerator",
    "Pizzascare",
    "Don't Make A Sound",
    "WAR"
]

level_checks = [
    "Complete",
    "Mushroom Toppin",
    "Cheese Toppin",
    "Tomato Toppin",
    "Sausage Toppin",
    "Pineapple Toppin",
    "S Rank",
    "P Rank",
    "Pumpkin",
    "Treasure",
    "Secret 1",
    "Secret 2",
    "Secret 3"
]

level_achievements = {
    "John Gutter": {"Chef Task: Let's Make This Quick", "Chef Task: John Gutted", "Chef Task: Primate Rage"},
    "Pizzascape": {"Chef Task: Shining Armor", "Chef Task: Spherical", "Chef Task: Spoonknight"},
    "Ancient Cheese": {"Chef Task: Thrill Seeker", "Chef Task: Volleybomb", "Chef Task: Delicacy"},
    "Bloodsauce Dungeon": {"Chef Task: Eruption Man", "Chef Task: Very Very Hot Sauce", "Chef Task: Unsliced Pizzaman"},
    "Oregano Desert": {"Chef Task: Peppino's Rain Dance", "Chef Task: Unnecessary Violence", "Chef Task: Alien Cow"},
    "Wasteyard": {"Chef Task: Alive and Well", "Chef Task: Ghosted", "Chef Task: Pretend Ghost"},
    "Fun Farm": {"Chef Task: Good Egg", "Chef Task: No One Is Safe", "Chef Task: Cube Menace"},
    "Fastfood Saloon": {"Chef Task: Royal Flush", "Chef Task: Already Pressed", "Chef Task: Non-Alcoholic"},
    "Crust Cove": {"Chef Task: X", "Chef Task: Demolition Expert", "Chef Task: Blowback"},
    "Gnome Forest": {"Chef Task: Bee Nice", "Chef Task: Bullseye", "Chef Task: Lumberjack"},
    "Deep-Dish 9": {"Chef Task: Blast 'Em Asteroids", "Chef Task: Man Meteor", "Chef Task: Turbo Tunnel"},
    "GOLF": {"Chef Task: Nice Shot", "Chef Task: Helpful Burger", "Chef Task: Primo Golfer"},
    "The Pig City": {"Chef Task: Strike!", "Chef Task: Say Oink!", "Chef Task: Pan Fried"},
    "Peppibot Factory": {"Chef Task: There Can Be Only One", "Chef Task: Unflattening", "Chef Task: Whoop This!"},
    "Oh Shit!": {"Chef Task: Penny Pincher", "Chef Task: Can't Fool Me", "Chef Task: Food Clan"},
    "Freezerator": {"Chef Task: Frozen Nuggets", "Chef Task: Season's Greetings", "Chef Task: Ice Climber"},
    "Pizzascare": {"Chef Task: Haunted Playground", "Chef Task: Skullsplitter", "Chef Task: Cross To Bare"},
    "Don't Make A Sound": {"Chef Task: And This... Is My Gun-On-A-Stick!", "Chef Task: Jumpspared", "Chef Task: Let Them Sleep"},
    "WAR": {"Chef Task: Decorated Veteran", "Chef Task: Sharpshooter", "Chef Task: Trip To The Warzone"}
}

boss_names = [
    "Pepperman",
    "The Vigilante",
    "The Noise",
    "The Doise",
    "Fake Peppino"
]

boss_checks = [
    "Defeated",
    "S Rank",
    "P Rank"
]

boss_achievements = {
    "Pepperman": "Chef Task: The Critic",
    "The Vigilante": "Chef Task: The Ugly",
    "The Noise": "Chef Task: Denoise",
    "The Doise": "Chef Task: Denoise",
    "Fake Peppino": "Chef Task: Faker"
}

checks_in_sets_lvl = { lvl: { lvl + " " + check for check in level_checks} for lvl in levels_list }
checks_in_sets_boss = { boss: { boss + " " + check for check in boss_checks } for boss in boss_names }

pt_location_groups = checks_in_sets_lvl
for lvl in levels_list:
    pt_location_groups[lvl].update(level_achievements[lvl]) # remnant from testing. this is no laughing matter. i'm sorry
pt_location_groups.update(checks_in_sets_boss)
for boss in boss_names:
    pt_location_groups[boss].add(boss_achievements[boss])
pt_location_groups.update({"The Crumbling Tower of Pizza": {
    "The Crumbling Tower of Pizza Complete", 
    "The Crumbling Tower of Pizza S Rank", 
    "The Crumbling Tower of Pizza P Rank", 
    "The Crumbling Tower of Pizza Pumpkin"
}})
pt_location_groups.update({"Tutorial": {
    "Tutorial Complete",
    "Tutorial Complete in under 2 minutes", 
    "Tutorial Mushroom Toppin", 
    "Tutorial Cheese Toppin", 
    "Tutorial Tomato Toppin", 
    "Tutorial Sausage Toppin", 
    "Tutorial Pineapple Toppin"
}})
pt_location_groups.update({"Tricky Treat": {
    "Tricky Treat Main Path Pumpkin 1",
    "Tricky Treat Main Path Pumpkin 2",
    "Tricky Treat Main Path Pumpkin 3",
    "Tricky Treat Main Path Pumpkin 4",
    "Tricky Treat Main Path Pumpkin 5",
    "Tricky Treat Side Path Pumpkin 1",
    "Tricky Treat Side Path Pumpkin 2",
    "Tricky Treat Side Path Pumpkin 3",
    "Tricky Treat Side Path Pumpkin 4",
    "Tricky Treat Side Path Pumpkin 5"
}})
pt_location_groups.update({"Pizzaface": {
    "Pizzaface Defeated",
    "Chef Task: Face Off"
}})