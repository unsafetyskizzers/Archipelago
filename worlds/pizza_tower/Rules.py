from worlds.AutoWorld import World
from BaseClasses import MultiWorld
from .Options import PTOptions
from ..generic.Rules import set_rule, add_rule
from math import floor
from typing import Callable
from BaseClasses import LocationProgressType, Location, Entrance, CollectionState

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

floors_list = [
    "Floor 1 Tower Lobby",
    "Floor 2 Western District",
    "Floor 3 Vacation Resort",
    "Floor 4 Slum",
    "Floor 5 Staff Only"
]

rule_moves = {
    "GRAB": "Grab",
    "UPPER": "Uppercut",
    "MACH4": "Mach 4",
    "SJUMP": "Superjump",
    "CLIMB": "Wallclimb",
    "TAUNT": "Taunt",
    "STAUNT": "Supertaunt",
    "SLAM": "Bodyslam",
    "DJUMP": "Double Jump",
    "KICK": "Rat Kick",
    "SPIN": "Spin Attack",
    "CRUSH": "Crusher",
    "BOUNCE": "Wallbounce",
    "TORN": "Tornado",
    "BOMB": "Bomb",
    "LAP2": "Lap 2 Portals",

    "BALL": "Ball",
    "KNIGHT": "Knight",
    "FIRE": "Firemouth",
    "GHOST": "Ghost",
    "MORT": "Mort",
    "WEEN": "Weenie",
    "BARR": "Barrel",
    "BUBB": "Olive Bubble",
    "ROCKET": "Rocket",
    "BOX": "Pizzabox",
    "STICKY": "Sticky Cheese",
    "SATAN": "Satan's Choice",
    "SHOTGUN": "Shotgun",
    "VIGIGUN": "Revolver"
}

#these levels don't require a second lap on expert difficulty
lap1_levels = [
    "Gnome Forest",
    "Freezerator"
]

def level_gate_rando(world: World, is_noise: bool, logic_type: int) -> list[str]:
    #replace john gutter and pizzascape with any of these levels
    ok_start_levels = [ 
        "Pizzascape",
        "Ancient Cheese",
        "Bloodsauce Dungeon",
        "The Pig City",
        "Don't Make A Sound"
    ]
    if is_noise:
        ok_start_levels.append("Freezerator")
    if logic_type > 0:
        ok_start_levels.append("Wasteyard")
        ok_start_levels.append("GOLF")

    #copies of level and boss lists to be shuffled
    level_queue = [
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

    rando_level_order = []

    #place two levels from ok_start_levels at the beginning of the rando level order
    if world.options.fairly_random:
        for i in range(2):
            rando_level = ok_start_levels[world.random.randrange(len(ok_start_levels) - 1)]
            rando_level_order.append(rando_level)
            ok_start_levels.remove(rando_level)
            level_queue.remove(rando_level)
    
    #don't care where the leftover levels go
    world.random.shuffle(level_queue)
    rando_level_order += level_queue

    return rando_level_order

def boss_gate_rando(world: World, is_noise: bool) -> list[str]:
    boss_queue = [
        "Pepperman",
        "The Vigilante",
        "The Noise",
        "Fake Peppino"
    ]
    if world.options.character != 0:
        boss_queue[2] = "The Doise"
    world.random.shuffle(boss_queue)
    if world.options.fairly_random and world.options.difficulty > 0:
        while boss_queue[0] == "The Vigilante" or boss_queue[0] == "Pepperman": #floor 1 boss should not be vigi or pepperman
            world.random.shuffle(boss_queue)
    return boss_queue

def get_secrets_list() -> list[str]:
    secrets_list = []
    for lvl in levels_list:
        for i in range(3):
            secrets_list.append(lvl + " Secret " + str(i+1))
    return secrets_list

def secret_rando(world: World, options: PTOptions) -> list[str]:
    secrets_queue = get_secrets_list()
    world.random.shuffle(secrets_queue)
    if options.cheftask_checks and secrets_queue[16] != "Wasteyard Secret 2":
        secrets_queue[secrets_queue.index("Wasteyard Secret 2")] = secrets_queue[16]
        secrets_queue[16] = "Wasteyard Secret 2"
    if options.cheftask_checks and secrets_queue[39] != "Peppibot Factory Secret 1":
        secrets_queue[secrets_queue.index("Peppibot Factory Secret 1")] = secrets_queue[39]
        secrets_queue[39] = "Peppibot Factory Secret 1"
    return secrets_queue

def set_rules(multiworld: MultiWorld, world: World, options: PTOptions, toppins: int, pumpkins: int):
    bosses_list = [ #pizzaface is handled separately because he does not give a rank
        "Pepperman",
        "The Vigilante",
        "The Noise",
        "Fake Peppino"
    ]
    if options.character != 0:
        bosses_list[2] = "The Doise"



    rules_dict = { #tuples in this format: (pep easy, pep hard, noise easy, noise hard)
        #John Gutter
        "John Gutter Complete": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Mushroom Toppin": (
            "SJUMP | CLIMB | UPPER", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Cheese Toppin": (
            "SJUMP+SLAM | CLIMB+SLAM | UPPER+SLAM", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Tomato Toppin": (
            "SJUMP+SLAM | CLIMB+SLAM | UPPER+SLAM", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Sausage Toppin": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Pineapple Toppin": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH",  
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Secret 1": (
            "SJUMP+SLAM | CLIMB+SLAM | UPPER+SLAM", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Secret 2": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Secret 3": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Treasure": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "Chef Task: John Gutted": (
			"SJUMP+SLAM", 
			"SJUMP | CLIMB", 
			"SJUMP+SLAM | SJUMP+CRUSH", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Primate Rage": (
			"LAP2+SJUMP+SLAM", 
			"LAP2+SJUMP | LAP2+CLIMB", 
			"LAP2+SJUMP+SLAM | LAP2+SJUMP+CRUSH", 
			"LAP2+SJUMP | LAP2+UPPER | LAP2+CRUSH | LAP2+BOUNCE"
		),
        "Chef Task: Let's Make This Quick": (
			"CLIMB+SJUMP+MACH4+SLAM", 
			"SJUMP | CLIMB", 
			"SJUMP+MACH4+SLAM | SJUMP+MACH4 + CRUSH", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "John Gutter S Rank": (
			"SJUMP+SLAM",
			"SJUMP | CLIMB", 
			"SJUMP+SLAM | SJUMP+CRUSH", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
		"John Gutter Pumpkin": (
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | CLIMB | UPPER | GRAB", 
			"SJUMP | BOUNCE | UPPER | CRUSH", 
			"SJUMP | BOUNCE | UPPER | GRAB | CRUSH"
		),

    #Pizzascape
        "Pizzascape Complete": (
			"GRAB+CLIMB+KNIGHT", 
			"UPPER+SJUMP+KNIGHT | UPPER+CLIMB+KNIGHT | GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | UPPER+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT"
		),
        "Pizzascape Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Pizzascape Cheese Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Pizzascape Tomato Toppin": (
			"GRAB+KNIGHT", 
			"UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Pizzascape Sausage Toppin": (
			"GRAB+KNIGHT", 
			"UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Pizzascape Pineapple Toppin": (
			"GRAB+KNIGHT",
            "UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Pizzascape Secret 1": (
			"GRAB+KNIGHT",
            "UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Pizzascape Secret 2": (
			"GRAB+KNIGHT",
            "UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Pizzascape Secret 3": (
			"GRAB+SJUMP+KNIGHT", 
			"UPPER+SJUMP+KNIGHT | UPPER+CLIMB+KNIGHT | GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | UPPER+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT"
		),
        "Pizzascape Treasure": (
			"GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"UPPER+SJUMP+KNIGHT | UPPER+CLIMB+KNIGHT | GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | UPPER+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT"
		),
        "Chef Task: Shining Armor": (
			"GRAB+KNIGHT", 
			"UPPER+KNIGHT | GRAB+KNIGHT", 
			"GRAB+UPPER+KNIGHT | GRAB+SJUMP+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT", 
			"GRAB+KNIGHT | UPPER+KNIGHT"
		),
        "Chef Task: Spoonknight": (
			"TAUNT", 
			"TAUNT", 
			"TAUNT", 
			"TAUNT"
		),
        "Chef Task: Spherical": (
			"GRAB+KNIGHT+BALL", 
			"UPPER+KNIGHT+BALL | GRAB+KNIGHT+BALL", 
			"GRAB+KNIGHT+BALL", 
			"GRAB+KNIGHT+BALL | UPPER+KNIGHT+BALL"
		),
        "Pizzascape S Rank": (
			"GRAB+CLIMB+KNIGHT+SJUMP", 
			"UPPER+SJUMP+KNIGHT | UPPER+CLIMB+KNIGHT | GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | UPPER+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT"
		),
        "Pizzascape Pumpkin": (
			"GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | GRAB+CLIMB+KNIGHT | UPPER+SJUMP+KNIGHT | UPPER+CLIMB+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+UPPER+KNIGHT", 
			"GRAB+SJUMP+KNIGHT | GRAB+BOUNCE+KNIGHT | GRAB+CRUSH+KNIGHT | UPPER+KNIGHT"
		),

    #Ancient Cheese
        "Ancient Cheese Complete": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH", 
			"GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH"
		),
        "Ancient Cheese Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Ancient Cheese Cheese Toppin": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB+SJUMP | GRAB+UPPER | GRAB+BOUNCE | GRAB+CRUSH", 
			"GRAB | UPPER"
		),
        "Ancient Cheese Tomato Toppin": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER | GRAB+CLIMB | GRAB+SJUMP", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE | GRAB+SJUMP | UPPER"
		),
        "Ancient Cheese Sausage Toppin": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH"
		),
        "Ancient Cheese Pineapple Toppin": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH"
		),
        "Ancient Cheese Secret 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Ancient Cheese Secret 2": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER | GRAB+CLIMB | GRAB+SJUMP", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE | GRAB+SJUMP | UPPER"
		),
        "Ancient Cheese Secret 3": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH"
		),
        "Ancient Cheese Treasure": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+CLIMB | UPPER+SJUMP | GRAB+CLIMB | GRAB+SJUMP", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE | GRAB+SJUMP | UPPER"
		),
        "Chef Task: Thrill Seeker": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH"
		),
        "Chef Task: Volleybomb": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER | GRAB+CLIMB | GRAB+SJUMP", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE | GRAB+SJUMP | UPPER"
		),
        "Chef Task: Delicacy": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Ancient Cheese S Rank": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH", 
			"GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH"
		),
        "Ancient Cheese Pumpkin": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+SLAM+CLIMB | UPPER+SLAM+SJUMP | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH"
		),

    #Bloodsauce Dungeon
        "Bloodsauce Dungeon Complete": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Bloodsauce Dungeon Mushroom Toppin": (
			"SJUMP | CLIMB", 
			"NONE", 
			"SJUMP | BOUNCE | UPPER | CRUSH", 
			"NONE"
		),
        "Bloodsauce Dungeon Cheese Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Bloodsauce Dungeon Tomato Toppin": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Bloodsauce Dungeon Sausage Toppin": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Bloodsauce Dungeon Pineapple Toppin": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Bloodsauce Dungeon Secret 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Bloodsauce Dungeon Secret 2": (
			"SJUMP+SLAM", 
			"SJUMP+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+BOUNCE | SJUMP+CRUSH | SJUMP+TORN"
		),
        "Bloodsauce Dungeon Secret 3": (
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Bloodsauce Dungeon Treasure": (
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Chef Task: Eruption Man": (
			"SJUMP+SLAM", 
			"SJUMP+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Chef Task: Very Very Hot Sauce": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Chef Task: Unsliced Pizzaman": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Bloodsauce Dungeon S Rank": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),
        "Bloodsauce Dungeon Pumpkin": (
			"SLAM", 
			"SLAM", 
			"SLAM | CRUSH | BOUNCE | TORN", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),

    #Oregano Desert
        "Oregano Desert Complete": (
			"CLIMB+FIRE", 
			"SJUMP+GRAB+FIRE | UPPER+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
		),
        "Oregano Desert Mushroom Toppin": (
			"SJUMP | CLIMB", 
			"UPPER | SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Cheese Toppin": (
			"SJUMP+FIRE | CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Tomato Toppin": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Sausage Toppin": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Pineapple Toppin": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Secret 1": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"BOUNCE", 
			"SJUMP | BOUNCE"
		),
        "Oregano Desert Secret 2": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Secret 3": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Treasure": (
			"CLIMB+FIRE", 
			"CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Chef Task: Peppino's Rain Dance": (
			"SJUMP | CLIMB", 
			"UPPER | SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Unnecessary Violence": (
			"CLIMB+FIRE", 
			"CLIMB+FIRE", 
			 "SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Chef Task: Alien Cow": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert S Rank": (
			"CLIMB+FIRE", 
			"SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"BOUNCE+FIRE", 
			"SJUMP+FIRE | BOUNCE+FIRE"
		),
        "Oregano Desert Pumpkin": (
			"CLIMB+FIRE", 
			"UPPER+GRAB+FIRE | SJUMP+GRAB+FIRE | CLIMB+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE", 
			"SJUMP+FIRE | UPPER+FIRE | CRUSH+FIRE | BOUNCE+FIRE"
		),

    #Wasteyard
        "Wasteyard Complete": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Wasteyard Cheese Toppin": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"GHOST"
		),
        "Wasteyard Tomato Toppin": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST | UPPER+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Sausage Toppin": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST | UPPER+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Pineapple Toppin": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST | UPPER+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Secret 1": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Secret 2": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST | UPPER+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Secret 3": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard Treasure": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Chef Task: Alive and Well": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Chef Task: Pretend Ghost": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Chef Task: Ghosted": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
        "Wasteyard S Rank": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),
		"Wasteyard Pumpkin": (
			"SJUMP+GHOST | CLIMB+GHOST", 
			"SJUMP+GHOST | CLIMB+GHOST | UPPER+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST", 
			"SJUMP+GHOST | UPPER+GHOST | CRUSH+GHOST | BOUNCE+GHOST"
		),

    #Fun Farm
        "Fun Farm Complete": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Fun Farm Mushroom Toppin": (
			"SLAM+SJUMP+MORT | SLAM+CLIMB+MORT | SLAM+UPPER+MORT", 
			"SLAM+UPPER+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm Cheese Toppin": (
			"SLAM+SJUMP+MORT | SLAM+CLIMB+MORT | SLAM+UPPER+MORT", 
			"SLAM+UPPER+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm Tomato Toppin": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm Sausage Toppin": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm Pineapple Toppin": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Fun Farm Secret 1": (
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Secret 2": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm Secret 3": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Fun Farm Treasure": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Chef Task: Good Egg": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Chef Task: No One Is Safe": (
			"SLAM+CLIMB+STAUNT+MORT", 
			"SLAM+STAUNT+SJUMP+MORT | SLAM+STAUNT+CLIMB+MORT", 
			"BOUNCE+SLAM+STAUNT+MORT | UPPER+SLAM+STAUNT+MORT | SJUMP+SLAM+STAUNT+MORT | BOUNCE+TORN+STAUNT+MORT | UPPER+TORN+STAUNT+MORT | SJUMP+TORN+STAUNT+MORT | CRUSH+STAUNT+MORT", 
			"CRUSH+STAUNT+MORT | SLAM+UPPER+STAUNT+MORT | SLAM+BOUNCE+STAUNT+MORT | SLAM+SJUMP+STAUNT+MORT"
		),
        "Chef Task: Cube Menace": (
			"SLAM+SJUMP+MORT | SLAM+CLIMB+MORT | SLAM+UPPER+MORT", 
			"SLAM+UPPER+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),
        "Fun Farm S Rank": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | CRUSH+MORT", 
			"CRUSH+MORT | SLAM+UPPER+MORT | SLAM+BOUNCE+MORT | SLAM+SJUMP+MORT"
		),
        "Fun Farm Pumpkin": (
			"SLAM+CLIMB+MORT", 
			"SLAM+UPPER+GRAB+MORT | SLAM+SJUMP+MORT | SLAM+CLIMB+MORT", 
			"BOUNCE+SLAM+MORT | UPPER+SLAM+MORT | SJUMP+SLAM+MORT | BOUNCE+TORN+MORT | UPPER+TORN+MORT | SJUMP+TORN+MORT | CRUSH+MORT", 
			"SJUMP+SLAM+MORT | SJUMP+TORN+MORT | BOUNCE+MORT | CRUSH+MORT | UPPER+SLAM+MORT | UPPER+TORN+MORT"
		),

    #Fastfood Saloon
        "Fastfood Saloon Complete": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Mushroom Toppin": (
			"SJUMP", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Fastfood Saloon Cheese Toppin": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Tomato Toppin": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Sausage Toppin": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Pineapple Toppin": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Secret 1": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Secret 2": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Secret 3": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
	    "Fastfood Saloon Treasure": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Chef Task: Royal Flush": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Chef Task: Non-Alcoholic": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Chef Task: Already Pressed": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon S Rank": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),
        "Fastfood Saloon Pumpkin": (
			"SJUMP+GRAB+CLIMB+WEEN", 
			"GRAB+SJUMP+WEEN | GRAB+CLIMB+WEEN", 
			"SJUMP+GRAB+WEEN", 
			"SJUMP+GRAB+WEEN | UPPER+GRAB+WEEN | CRUSH+GRAB+WEEN | BOUNCE+GRAB+WEEN"
		),

    #Crust Cove
        "Crust Cove Complete": (
			"CLIMB+SLAM+BARR",
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Crust Cove Mushroom Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Crust Cove Cheese Toppin": (
			"SJUMP+BARR | CLIMB+BARR", 
			"SJUMP+BARR | CLIMB+BARR", 
			"SJUMP+BARR", 
			"CRUSH+BARR | SJUMP+BARR"
		),
        "Crust Cove Tomato Toppin": (
			"CLIMB+SLAM+BARR", 
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Crust Cove Sausage Toppin": (
			"CLIMB+SLAM+BARR", 
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Crust Cove Pineapple Toppin": (
			"CLIMB+SLAM+BARR", 
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR| SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Crust Cove Secret 1": (
			"SJUMP+BARR | CLIMB+BARR", 
			"SJUMP+BARR | CLIMB+BARR", 
			"SJUMP+BARR", 
			"CRUSH+BARR | SJUMP+BARR"
		),
        "Crust Cove Secret 2": (
			"CLIMB+SLAM+BARR", 
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Crust Cove Secret 3": (
			"CLIMB+SLAM+TAUNT+BARR", 
			"SLAM+CLIMB+TAUNT+BARR | SLAM+SJUMP+UPPER+TAUNT+BARR", 
			"SJUMP+SLAM+TAUNT+BARR | SJUMP+CRUSH+TAUNT+BARR | SJUMP+TORN+TAUNT+BARR", 
			"CRUSH+TAUNT+BARR | SJUMP+TORN+TAUNT+BARR | SJUMP+SLAM+TAUNT+BARR | SJUMP+BOUNCE+TAUNT+BARR"
		),
        "Crust Cove Treasure": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Chef Task: Demolition Expert": (
			"CLIMB+SLAM+BARR", 
			"SLAM+CLIMB+BARR | SLAM+SJUMP+UPPER+BARR", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),
        "Chef Task: Blowback": (
			"SJUMP+TAUNT | CLIMB+TAUNT", 
			"SJUMP+TAUNT | CLIMB+TAUNT", 
			"SJUMP+TAUNT", 
			"CRUSH+TAUNT | SJUMP+TAUNT"
		),
        "Chef Task: X": (
			"CLIMB+SLAM+BARR", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SJUMP+SLAM+BARR | SJUMP+CRUSH+BARR | SJUMP+TORN+BARR", 
			"CRUSH | SJUMP+SLAM | BOUNCE+SLAM | UPPER+SLAM"
		),
        "Crust Cove S Rank": (
			"CLIMB+SLAM+TAUNT+BARR", 
			"SLAM+CLIMB+TAUNT+BARR | SLAM+SJUMP+UPPER+TAUNT+BARR", 
			"SJUMP+SLAM+TAUNT+BARR | SJUMP+CRUSH+TAUNT+BARR | SJUMP+TORN+TAUNT+BARR", 
			"CRUSH+TAUNT+BARR | SJUMP+TORN+TAUNT+BARR | SJUMP+SLAM+TAUNT+BARR | SJUMP+BOUNCE+TAUNT+BARR"
		),
        "Crust Cove Pumpkin": (
			"CLIMB+SLAM+SJUMP+BARR", 
			"CLIMB+SLAM+SJUMP+BARR", 
			"SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR | SJUMP+CRUSH+BARR", 
			"CRUSH+BARR | SJUMP+TORN+BARR | SJUMP+SLAM+BARR | SJUMP+BOUNCE+BARR"
		),

    #Gnome Forest
        "Gnome Forest Complete": (
			"SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest Mushroom Toppin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Gnome Forest Cheese Toppin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Gnome Forest Tomato Toppin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Gnome Forest Sausage Toppin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest Pineapple Toppin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest Secret 1": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Gnome Forest Secret 2": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Gnome Forest Secret 3": (
			"SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest Treasure": (
			"SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH", 
			"CRUSH"
		),
        "Chef Task: Bee Nice": (
			"TAUNT", 
			"TAUNT", 
			"TAUNT", 
			"TAUNT"
		),
        "Chef Task: Bullseye": (
			"TAUNT", 
			"TAUNT", 
			"TAUNT", 
			"TAUNT"
		),
        "Chef Task: Lumberjack": (
			"SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest S Rank": (
			"SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"BOUNCE+CRUSH | SJUMP+CRUSH", 
			"CRUSH"
		),
        "Gnome Forest Pumpkin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),

    #Deep-Dish 9
        "Deep-Dish 9 Complete": (
			"SLAM+CLIMB+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB",
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB",
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Mushroom Toppin": (
			"SLAM+ROCKET+BUBB", 
			"SLAM+ROCKET+BUBB",
			"SLAM+ROCKET+BUBB | CRUSH+ROCKET+BUBB | TORN+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+ROCKET | BUBB+TORN+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Cheese Toppin": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+ROCKET | BUBB+TORN+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Tomato Toppin": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+ROCKET | BUBB+TORN+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Sausage Toppin": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB",  
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Pineapple Toppin": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB",  
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Secret 1": (
			"SLAM+UPPER+ROCKET+BUBB | SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+ROCKET+BUBB",
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+ROCKET | BUBB+TORN+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Secret 2": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+ROCKET | BUBB+TORN+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Secret 3": (
			"SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Treasure": (
			"SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Chef Task: Blast 'Em Asteroids": (
			"SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Chef Task: Turbo Tunnel": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Chef Task: Man Meteor": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 S Rank": (
			"SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+GRAB+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),
        "Deep-Dish 9 Pumpkin": (
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | SLAM+CLIMB+ROCKET+BUBB", 
			"SLAM+SJUMP+ROCKET+BUBB | TORN+SJUMP+ROCKET+BUBB | CRUSH+SJUMP+ROCKET+BUBB | SLAM+BOUNCE+ROCKET+BUBB | TORN+BOUNCE+ROCKET+BUBB | CRUSH+BOUNCE+ROCKET+BUBB | SLAM+UPPER+ROCKET+BUBB | TORN+UPPER+ROCKET+BUBB | CRUSH+UPPER+ROCKET+BUBB", 
			"SJUMP+SLAM+ROCKET | SJUMP+TORN+ROCKET | SJUMP+BOUNCE+ROCKET | BUBB+SLAM+UPPER+ROCKET | BUBB+TORN+UPPER+ROCKET | BUBB+BOUNCE+ROCKET | CRUSH+ROCKET"
		),

    #GOLF
        "GOLF Complete": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Mushroom Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Cheese Toppin": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Tomato Toppin": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Sausage Toppin": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Pineapple Toppin": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Secret 1": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Secret 2": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Secret 3": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF Treasure": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL", 
			"SJUMP+BALL | CLIMB+GRAB+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"SJUMP+BALL | BOUNCE+BALL | CRUSH+BALL | UPPER+BALL"
		),
        "Chef Task: Primo Golfer": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "Chef Task: Helpful Burger": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "Chef Task: Nice Shot": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"BALL"
		),
        "GOLF S Rank": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL", 
			"SJUMP+BALL | CLIMB+GRAB+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+GRAB+BALL | CRUSH+GRAB+BALL | UPPER+GRAB+BALL | BOUNCE+GRAB+BALL", 
			"SJUMP+BALL | BOUNCE+BALL | CRUSH+BALL | UPPER+BALL"
		),
        "GOLF Pumpkin": (
			"GRAB+CLIMB+BALL | GRAB+SJUMP+BALL | GRAB+UPPER+BALL", 
			"BALL", 
			"GRAB+BOUNCE+BALL | GRAB+UPPER+BALL | GRAB+SJUMP+BALL | GRAB+CRUSH+BALL", 
			"BALL"
		),

    #The Pig City
        "The Pig City Complete": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "The Pig City Cheese Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER | BOUNCE"
		),
        "The Pig City Tomato Toppin": (
			"SLAM", 
			"SLAM", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"CRUSH | SLAM"
		),
        "The Pig City Sausage Toppin": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Pineapple Toppin": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Secret 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "The Pig City Secret 2": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Secret 3": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Treasure": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Chef Task: Say Oink!": (
			"SLAM+DJUMP+TAUNT", 
			"SLAM+DJUMP+TAUNT", 
			"SJUMP+SLAM+TAUNT | CRUSH+TAUNT | BOUNCE+SLAM+TAUNT | UPPER+SLAM+TAUNT", 
			"CRUSH+TAUNT | SLAM+SJUMP+TAUNT | SLAM+BOUNCE+TAUNT | SLAM+UPPER+TAUNT"
		),
        "Chef Task: Pan Fried": (
			"SLAM+SJUMP", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"CRUSH | SLAM+SJUMP | SLAM+UPPER | SLAM+BOUNCE"
		),
        "Chef Task: Strike!": (
			"SLAM+DJUMP+KICK", 
			"SLAM+DJUMP+KICK", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City S Rank": (
			"SJUMP+SLAM+DJUMP+SPIN | CLIMB+SLAM+DJUMP+SPIN | SJUMP+SLAM+DJUMP+KICK | CLIMB+SLAM+DJUMP+KICK", 
			"SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP", 
			"SJUMP+SLAM | SJUMP+CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "The Pig City Pumpkin": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"CRUSH | SLAM"
		),

    #Peppibot Factory
        "Peppibot Factory Complete": (
			"SJUMP+CLIMB+SLAM+BOX | SJUMP+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | CLIMB+GRAB+SLAM+BOX | CLIMB+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | SJUMP+TORN+BOX | SJUMP+CRUSH+BOX", 
			"SJUMP+BOUNCE+BOX | SJUMP+TORN+BOX | UPPER+BOUNCE+BOX | UPPER+TORN+BOX | CRUSH+BOX"
		),
        "Peppibot Factory Mushroom Toppin": (
			"SJUMP", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Cheese Toppin": (
			"SJUMP+CLIMB | SJUMP+UPPER", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Tomato Toppin": (
			"SJUMP+CLIMB | SJUMP+UPPER", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Sausage Toppin": (
			"SJUMP+CLIMB+BOX | SJUMP+UPPER+BOX", 
			"SJUMP+BOX | CLIMB+GRAB+BOX | CLIMB+UPPER+BOX", 
			"SJUMP+BOX", 
			"SJUMP+BOX | CRUSH+BOX | UPPER+BOX"
		),
        "Peppibot Factory Pineapple Toppin": (
			"SJUMP+CLIMB+BOX | SJUMP+UPPER+BOX", 
			"SJUMP+BOX | CLIMB+GRAB+BOX | CLIMB+UPPER+BOX", 
			"SJUMP+BOX", 
			"SJUMP+BOX | CRUSH+BOX | UPPER+BOX"
		),
        "Peppibot Factory Secret 1": (
			"SJUMP", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Secret 2": (
			"SJUMP+UPPER", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Secret 3": (
			"SJUMP+CLIMB+SLAM+BOX | SJUMP+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | CLIMB+GRAB+SLAM+BOX | CLIMB+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | SJUMP+TORN+BOX | SJUMP+CRUSH+BOX", 
			"SJUMP+BOUNCE+BOX | SJUMP+TORN+BOX | UPPER+BOUNCE+BOX | UPPER+TORN+BOX | CRUSH+BOX"
		),
        "Peppibot Factory Treasure": (
			"SJUMP+CLIMB+SLAM+BOX | SJUMP+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | CLIMB+GRAB+SLAM+BOX | CLIMB+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | SJUMP+TORN+BOX | SJUMP+CRUSH+BOX", 
			"SJUMP+BOUNCE+BOX | SJUMP+TORN+BOX | UPPER+BOUNCE+BOX | UPPER+TORN+BOX | CRUSH+BOX"
		),
        "Chef Task: There Can Be Only One": (
			"LAP2+SJUMP+CLIMB+SLAM+BOX | LAP2+SJUMP+UPPER+SLAM+BOX", 
			"LAP2+SJUMP+SLAM+BOX | LAP2+CLIMB+GRAB+SLAM+BOX | LAP2+CLIMB+UPPER+SLAM+BOX", 
			"LAP2+SJUMP+SLAM+BOX | LAP2+SJUMP+TORN+BOX | LAP2+SJUMP+CRUSH+BOX", 
			"LAP2+SJUMP+BOUNCE+BOX | LAP2+SJUMP+TORN+BOX | LAP2+UPPER+BOUNCE+BOX | LAP2+UPPER+TORN+BOX | LAP2+CRUSH+BOX"
		),
        "Chef Task: Whoop This!": (
			"SJUMP", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Chef Task: Unflattening": (
			"SJUMP+CLIMB+SLAM+BOX | SJUMP+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | CLIMB+GRAB+SLAM+BOX | CLIMB+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX | SJUMP+TORN+BOX | SJUMP+CRUSH+BOX", 
			"SJUMP+BOUNCE+BOX | SJUMP+TORN+BOX | UPPER+BOUNCE+BOX | UPPER+TORN+BOX | CRUSH+BOX"
		),
        "Peppibot Factory S Rank": (
			"SJUMP+CLIMB+SLAM+BOX+GRAB | SJUMP+UPPER+SLAM+BOX+GRAB", 
			"SJUMP+SLAM+BOX+GRAB | SJUMP+SLAM+BOX+UPPER | CLIMB+GRAB+SLAM+BOX | CLIMB+UPPER+SLAM+BOX", 
			"SJUMP+SLAM+BOX+GRAB | SJUMP+TORN+BOX+GRAB | SJUMP+CRUSH+BOX+GRAB", 
			"SJUMP+BOUNCE+BOX+GRAB | SJUMP+TORN+BOX+GRAB | UPPER+BOUNCE+BOX | UPPER+TORN+BOX | CRUSH+BOX+GRAB | CRUSH+BOX+UPPER"
		),
        "Peppibot Factory Pumpkin": (
			"SJUMP+CLIMB+BOX | SJUMP+UPPER+BOX", 
			"SJUMP+UPPER+BOX | CLIMB+GRAB+BOX | CLIMB+UPPER+BOX", 
			"SJUMP+BOX", 
			"SJUMP+BOX | CRUSH+BOX | UPPER+BOX"
		),

    #Oh Shit!
        "Oh Shit! Complete": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Mushroom Toppin": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Oh Shit! Cheese Toppin": (
			"SLAM+CLIMB | SLAM+SJUMP | SLAM+UPPER", 
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+BOUNCE | TORN+BOUNCE | CRUSH | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Tomato Toppin": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Sausage Toppin": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Pineapple Toppin": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Secret 1": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Oh Shit! Secret 2": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Secret 3": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Treasure": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Chef Task: Food Clan": (
			"SLAM+CLIMB+TAUNT+STICKY", 
			"SLAM+SJUMP+TAUNT+STICKY | SLAM+CLIMB+TAUNT+STICKY | SLAM+UPPER+TAUNT+STICKY", 
			"SLAM+BOUNCE+TAUNT+STICKY | TORN+BOUNCE+TAUNT+STICKY | CRUSH+TAUNT+STICKY | SLAM+SJUMP+TAUNT+STICKY | TORN+SJUMP+TAUNT+STICKY | SLAM+UPPER+TAUNT+STICKY | TORN+UPPER+TAUNT+STICKY", 
			"SJUMP+SLAM+TAUNT+STICKY | SJUMP+TORN+TAUNT+STICKY | BOUNCE+TAUNT+STICKY | CRUSH+TAUNT+STICKY | UPPER+SLAM+TAUNT+STICKY | UPPER+TORN+TAUNT+STICKY"
		),
        "Chef Task: Can't Fool Me": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Chef Task: Penny Pincher": (
			"SLAM+CLIMB+SJUMP+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! S Rank": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),
        "Oh Shit! Pumpkin": (
			"SLAM+CLIMB+STICKY", 
			"SLAM+CLIMB+STICKY", 
			"SLAM+BOUNCE+STICKY | TORN+BOUNCE+STICKY | SLAM+SJUMP+STICKY | TORN+SJUMP+STICKY | SLAM+UPPER+STICKY | TORN+UPPER+STICKY | CRUSH+SJUMP+STICKY | CRUSH+BOUNCE+STICKY | CRUSH+UPPER+STICKY", 
			"SJUMP+SLAM+STICKY | SJUMP+TORN+STICKY | BOUNCE+STICKY | CRUSH+STICKY | UPPER+SLAM+STICKY | UPPER+TORN+STICKY"
		),

    #Freezerator
        "Freezerator Complete": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Mushroom Toppin": (
			"CLIMB | SJUMP", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Freezerator Cheese Toppin": (
			"CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"NONE", 
			"NONE"
		),
        "Freezerator Tomato Toppin": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Sausage Toppin": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Pineapple Toppin": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Secret 1": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Secret 2": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Secret 3": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator Treasure": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Chef Task: Ice Climber": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Chef Task: Season's Greetings": (
			"CLIMB+SLAM+SJUMP+GRAB+STAUNT", 
			"SJUMP+SLAM+STAUNT | CLIMB+SLAM+STAUNT", 
			"GRAB | STAUNT", 
			"STAUNT | GRAB"
		),
        "Chef Task: Frozen Nuggets": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Freezerator S Rank": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM | CRUSH | TORN | BOUNCE", 
			"SLAM | CRUSH | TORN | BOUNCE"
		),
        "Freezerator Pumpkin": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),

    #Pizzascare
        "Pizzascare Complete": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Mushroom Toppin": (
			"CLIMB+SLAM | SJUMP+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM | SJUMP+TORN | BOUNCE+TORN | UPPER+TORN", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Cheese Toppin": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM | SJUMP+TORN | BOUNCE+TORN | UPPER+TORN", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Tomato Toppin": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Sausage Toppin": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Pineapple Toppin": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Secret 1": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Secret 2": (
			"CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | BOUNCE+SLAM+BALL | SJUMP+TORN+BALL | BOUNCE+TORN+BALL | SJUMP+CRUSH+BALL | BOUNCE+CRUSH+BALL", 
			"CRUSH+BALL | SJUMP+SLAM+BALL | SJUMP+TORN+BALL | UPPER+SLAM+BALL | UPPER+TORN+BALL | BOUNCE+BALL"
		),
        "Pizzascare Secret 3": (
			"CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | BOUNCE+SLAM+BALL | SJUMP+TORN+BALL | BOUNCE+TORN+BALL | SJUMP+CRUSH+BALL | BOUNCE+CRUSH+BALL", 
			"CRUSH+BALL | SJUMP+SLAM+BALL | SJUMP+TORN+BALL | UPPER+SLAM+BALL | UPPER+TORN+BALL | BOUNCE+BALL"
		),
        "Pizzascare Treasure": (
			"CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | BOUNCE+SLAM+BALL | SJUMP+TORN+BALL | BOUNCE+TORN+BALL | SJUMP+CRUSH+BALL | BOUNCE+CRUSH+BALL", 
			"CRUSH+BALL | SJUMP+SLAM+BALL | SJUMP+TORN+BALL | UPPER+SLAM+BALL | UPPER+TORN+BALL | BOUNCE+BALL"
		),
        "Chef Task: Haunted Playground": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Chef Task: Skullsplitter": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Chef Task: Cross To Bare": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare S Rank": (
			"CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | CLIMB+SLAM+BALL", 
			"SJUMP+SLAM+BALL | BOUNCE+SLAM+BALL | SJUMP+TORN+BALL | BOUNCE+TORN+BALL | SJUMP+CRUSH+BALL | BOUNCE+CRUSH+BALL", 
			"CRUSH+BALL | SJUMP+SLAM+BALL | SJUMP+TORN+BALL | UPPER+SLAM+BALL | UPPER+TORN+BALL | BOUNCE+BALL"
		),
        "Pizzascare Pumpkin": (
			"SJUMP | CLIMB", 
			"NONE", 
			"SJUMP | BOUNCE | UPPER | CRUSH", 
			"NONE"
		),

    #Don't Make A Sound
        "Don't Make A Sound Complete": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Don't Make A Sound Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Don't Make A Sound Cheese Toppin": (
			"CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | CRUSH | BOUNCE | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Don't Make A Sound Tomato Toppin": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | BOUNCE"
		),
        "Don't Make A Sound Sausage Toppin": (
			"CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER | BOUNCE"
		),
        "Don't Make A Sound Pineapple Toppin": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Don't Make A Sound Secret 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Don't Make A Sound Secret 2": (
			"CLIMB", 
			"SJUMP+UPPER | CLIMB", 
			"SJUMP | CRUSH | BOUNCE | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Don't Make A Sound Secret 3": (
			"CLIMB", 
			"SJUMP+UPPER | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | BOUNCE"
		),
        "Don't Make A Sound Treasure": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Chef Task: Let Them Sleep": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Chef Task: Jumpspared": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Chef Task: And This... Is My Gun On A Stick!": (
			"CLIMB+SLAM+GRAB+SHOTGUN", 
			"CLIMB+GRAB+SHOTGUN | CLIMB+UPPER+SHOTGUN", 
			"SJUMP+SLAM+GRAB+SHOTGUN", 
			"SJUMP+GRAB+SHOTGUN | SJUMP+UPPER+SHOTGUN | CRUSH+GRAB+SHOTGUN | CRUSH+UPPER+SHOTGUN | BOUNCE+GRAB+SHOTGUN | BOUNCE+UPPER+SHOTGUN"
		),
        "Don't Make A Sound S Rank": (
			"CLIMB+SLAM+GRAB+SHOTGUN+TAUNT", 
			"CLIMB+GRAB+SHOTGUN+SLAM+TAUNT | CLIMB+UPPER+SHOTGUN+SLAM+TAUNT", 
            "SJUMP+SLAM+GRAB+SHOTGUN+TAUNT", 
			"SJUMP+GRAB+SHOTGUN+SLAM+TAUNT | SJUMP+UPPER+SHOTGUN+SLAM+TAUNT | SJUMP+GRAB+SHOTGUN+TORN+TAUNT | SJUMP+UPPER+SHOTGUN+TORN+TAUNT | CRUSH+GRAB+SHOTGUN+TAUNT | CRUSH+UPPER+SHOTGUN+TAUNT | BOUNCE+GRAB+SHOTGUN+TAUNT | BOUNCE+UPPER+SHOTGUN+TAUNT"
		),
        "Don't Make A Sound Pumpkin": (
			"CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER | BOUNCE"
		),

    #WAR
        "WAR Complete": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "WAR Mushroom Toppin": (
			"GRAB+SHOTGUN+SJUMP | GRAB+SHOTGUN+CLIMB", 
			"GRAB+SHOTGUN+SJUMP | GRAB+SHOTGUN+CLIMB | UPPER+SHOTGUN+SJUMP | UPPER+SHOTGUN+CLIMB | GRAB+SHOTGUN+SLAM | UPPER+SHOTGUN+SLAM", 
			"GRAB+SHOTGUN+BOUNCE | GRAB+SHOTGUN+SJUMP", 
			"GRAB+SHOTGUN+CRUSH | GRAB+SHOTGUN+SJUMP | GRAB+SHOTGUN+BOUNCE | GRAB+SHOTGUN+SLAM | UPPER+SHOTGUN+CRUSH | UPPER+SHOTGUN+SJUMP | UPPER+SHOTGUN+BOUNCE | UPPER+SHOTGUN+SLAM"
		),
        "WAR Cheese Toppin": (
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Tomato Toppin": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+CLIMB+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+BOUNCE+SLAM+ROCKET | GRAB+SHOTGUN+BOUNCE+CRUSH+ROCKET | GRAB+SHOTGUN+BOUNCE+TORN+ROCKET | GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Sausage Toppin": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+CLIMB+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+BOUNCE+SLAM+ROCKET | GRAB+SHOTGUN+BOUNCE+CRUSH+ROCKET | GRAB+SHOTGUN+BOUNCE+TORN+ROCKET | GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Pineapple Toppin": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "WAR Secret 1": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+CLIMB+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+BOUNCE+SLAM+ROCKET | GRAB+SHOTGUN+BOUNCE+CRUSH+ROCKET | GRAB+SHOTGUN+BOUNCE+TORN+ROCKET | GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Secret 2": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+CLIMB+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+BOUNCE+SLAM+ROCKET | GRAB+SHOTGUN+BOUNCE+CRUSH+ROCKET | GRAB+SHOTGUN+BOUNCE+TORN+ROCKET | GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Secret 3": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "WAR Treasure": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+BOUNCE+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+BOUNCE+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET"
		),
        "Chef Task: Trip to the Warzone": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+MACH4+ROCKET | UPPER+SHOTGUN+SLAM+MACH4+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "Chef Task: Sharpshooter": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "Chef Task: Decorated Veteran": (
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "WAR S Rank": (
			"GRAB+SHOTGUN+SJUMP+SLAM+CLIMB+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CLIMB+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+CLIMB+ROCKET | GRAB+SHOTGUN+SLAM+ROCKET | UPPER+SHOTGUN+SLAM+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+SLAM+BOUNCE+ROCKET | GRAB+SHOTGUN+SJUMP+CRUSH+BOUNCE+ROCKET | GRAB+SHOTGUN+SJUMP+TORN+BOUNCE+ROCKET", 
			"GRAB+SHOTGUN+SJUMP+ROCKET | UPPER+SHOTGUN+SJUMP+ROCKET | GRAB+SHOTGUN+CRUSH+ROCKET | UPPER+SHOTGUN+CRUSH+ROCKET"
		),
        "WAR Pumpkin": (
			"GRAB+SJUMP+SLAM+SHOTGUN+ROCKET | GRAB+CLIMB+SLAM+SHOTGUN+ROCKET", 
			"GRAB+SJUMP+SHOTGUN+ROCKET | GRAB+CLIMB+SHOTGUN+ROCKET | UPPER+SJUMP+SHOTGUN+ROCKET | UPPER+CLIMB+SHOTGUN+ROCKET | GRAB+SLAM+SHOTGUN+ROCKET | UPPER+SLAM+SHOTGUN+ROCKET", 
			"GRAB+BOUNCE+SHOTGUN+ROCKET | GRAB+SJUMP+SHOTGUN+ROCKET", 
			"GRAB+CRUSH+SHOTGUN+ROCKET | GRAB+SJUMP+SHOTGUN+ROCKET | GRAB+BOUNCE+SHOTGUN+ROCKET | GRAB+SLAM+SHOTGUN+ROCKET | UPPER+CRUSH+SHOTGUN+ROCKET | UPPER+SJUMP+SHOTGUN+ROCKET | UPPER+BOUNCE+SHOTGUN+ROCKET | UPPER+SLAM+SHOTGUN+ROCKET"
		),

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": (
			"SLAM+SJUMP+CLIMB+GRAB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | GRAB+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SHOTGUN+SJUMP+SLAM+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+TORN+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+CRUSH+WEEN+ROCKET+BUBB", 
			"SJUMP+GRAB+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+GRAB+SHOTGUN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+UPPER+SHOTGUN+WEEN+ROCKET+BUBB"
		),
        "The Crumbling Tower of Pizza S Rank": (
			"SLAM+SJUMP+CLIMB+GRAB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | GRAB+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SHOTGUN+SJUMP+SLAM+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+TORN+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+CRUSH+WEEN+ROCKET+BUBB", 
			"SJUMP+GRAB+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+GRAB+SHOTGUN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+UPPER+SHOTGUN+WEEN+ROCKET+BUBB"
		),
        "The Crumbling Tower of Pizza P Rank": (
			"SLAM+SJUMP+CLIMB+GRAB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | GRAB+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+SJUMP+SHOTGUN+WEEN+ROCKET+BUBB | UPPER+SLAM+CLIMB+SHOTGUN+WEEN+ROCKET+BUBB", 
			"GRAB+SHOTGUN+SJUMP+SLAM+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+TORN+WEEN+ROCKET+BUBB | GRAB+SHOTGUN+SJUMP+CRUSH+WEEN+ROCKET+BUBB", 
			"SJUMP+GRAB+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+GRAB+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+GRAB+SHOTGUN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+SLAM+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+TORN+WEEN+ROCKET+BUBB | SJUMP+UPPER+SHOTGUN+BOUNCE+WEEN+ROCKET+BUBB | CRUSH+UPPER+SHOTGUN+WEEN+ROCKET+BUBB"
		),
        "The Crumbling Tower of Pizza Pumpkin": (
			"GRAB+SLAM+SHOTGUN", 
			"GRAB+SLAM+SHOTGUN | UPPER+SLAM+SHOTGUN", 
			"GRAB+SLAM+SHOTGUN | GRAB+TORN+SHOTGUN | GRAB+CRUSH+SHOTGUN", 
			"GRAB+SLAM+SHOTGUN | GRAB+TORN+SHOTGUN | GRAB+CRUSH+SHOTGUN | GRAB+BOUNCE+SHOTGUN | UPPER+SLAM+SHOTGUN | UPPER+TORN+SHOTGUN | UPPER+CRUSH+SHOTGUN | UPPER+BOUNCE+SHOTGUN"
		),

    #Pepperman
        "Pepperman Defeated": (
			"GRAB", 
			"GRAB", 
			"BOMB | GRAB", 
			"BOMB | GRAB"
		),
        "Chef Task: The Critic": (
			"GRAB", 
			"GRAB", 
			"BOMB | GRAB", 
			"BOMB | GRAB"
		),
        "Pepperman S Rank": (
			"GRAB", 
			"GRAB", 
			"BOMB | GRAB", 
			"BOMB | GRAB"
		),
        "Pepperman P Rank": (
			"GRAB", 
			"GRAB", 
			"BOMB | GRAB", 
			"BOMB | GRAB"
		),

    #Vigilante
        "The Vigilante Defeated": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN", 
			"BOMB", 
			"BOMB"
		),
        "Chef Task: The Ugly": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN", 
			"BOMB", 
			"BOMB"
		),
        "The Vigilante S Rank": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN", 
			"BOMB", 
			"BOMB"
		),
        "The Vigilante P Rank": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN", 
			"BOMB", 
			"BOMB"
		),

    #Noise
        "The Noise Defeated": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "Chef Task: Denoise": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "The Noise S Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "The Noise P Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),

    #Fake Pep
        "Fake Peppino Defeated": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "Chef Task: Faker": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "Fake Peppino S Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "Fake Peppino P Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),

    #Pizzaface
        "Pizzaface Defeated": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN", 
			"BOMB",
			"BOMB"
		),
        "Chef Task: Face Off": (
			"GRAB+VIGIGUN", 
			"GRAB+VIGIGUN",
			"BOMB", 
			"BOMB"
		),

    #Tutorial
        "Tutorial Complete": (
			"SLAM+CLIMB+SJUMP+GRAB", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+BOUNCE | CRUSH"
		),
        "Tutorial Complete in under 2 minutes": (
			"SLAM+CLIMB+SJUMP+GRAB", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+BOUNCE | CRUSH"
		),
        "Tutorial Mushroom Toppin": (
			"SLAM", 
			"SLAM", 
			"NONE", 
			"NONE"
		),
        "Tutorial Cheese Toppin": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB", 
			"NONE", 
			"NONE"
		),
        "Tutorial Tomato Toppin": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB", 
			"NONE", 
			"NONE"
		),
        "Tutorial Sausage Toppin": (
			"SLAM+CLIMB+SJUMP", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB", 
			"NONE", 
			"NONE"
		),
        "Tutorial Pineapple Toppin": (
			"SLAM+CLIMB+SJUMP+GRAB", 
			"SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB", 
			"NONE", 
			"NONE"
		),

    #misc
        "Snotty Murdered": (
			"NONE", 
			"NONE", 
			"NONE",
            "NONE"
		),

    #for swap mode
        "The Doise Defeated": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "Chef Task: Denoise": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "The Doise S Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),
        "The Doise P Rank": (
			"GRAB | UPPER", 
			"NONE", 
			"BOMB | GRAB", 
			"NONE"
		),

    #tricky treat
        "Tricky Treat Main Path Pumpkin 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Tricky Treat Main Path Pumpkin 2": (
			"GHOST", 
			"GHOST", 
			"GHOST", 
			"GHOST"
		),
        "Tricky Treat Main Path Pumpkin 3": (
			"GHOST+UPPER | GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH"
		),
        "Tricky Treat Main Path Pumpkin 4": (
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+BOUNCE | GHOST+BALL+SJUMP", 
			"GHOST+BALL+BOUNCE | GHOST+BALL+SJUMP | GHOST+BALL+CRUSH"
		),
        "Tricky Treat Main Path Pumpkin 5": (
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+BOUNCE+UPPER | GHOST+BALL+SJUMP", 
			"GHOST+BALL+BOUNCE+UPPER | GHOST+BALL+SJUMP | GHOST+BALL+CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 1": (
			"UPPER | CLIMB", 
			"UPPER | CLIMB", 
			"UPPER | BOUNCE | SJUMP | CRUSH", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 2": (
			"GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 3": (
			"GHOST+UPPER | GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 4": (
			"GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+CLIMB | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP", 
			"GHOST+UPPER | GHOST+BOUNCE | GHOST+SJUMP | GHOST+CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 5": (
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+BOUNCE | GHOST+BALL+SJUMP", 
			"GHOST+BALL+BOUNCE | GHOST+BALL+SJUMP | GHOST+BALL+CRUSH"
		),
        "Chef Task: Tricksy": (
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+CLIMB", 
			"GHOST+BALL+BOUNCE+UPPER | GHOST+BALL+SJUMP", 
			"GHOST+BALL+BOUNCE+UPPER | GHOST+BALL+SJUMP | GHOST+BALL+CRUSH"
		),
    }

    hub_rules_dict = { #tuples in this format: (pep, noise)
        #levels
        "John Gutter": ("NONE", "NONE"),
        "Pizzascape": ("NONE", "NONE"),
        "Ancient Cheese": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Bloodsauce Dungeon": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Oregano Desert": ("NONE", "NONE"),
        "Wasteyard": ("NONE", "NONE"),
        "Fun Farm": ("NONE", "NONE"),
        "Fastfood Saloon": ("NONE", "NONE"),
        "Crust Cove": ("NONE", "NONE"),
        "Gnome Forest": ("SJUMP | CLIMB | UPPER",  "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Deep-Dish 9": ("SJUMP+BUBB | CLIMB+BUBB",  "SJUMP+BUBB | UPPER+BUBB | CRUSH+BUBB | BOUNCE+BUBB"),
        "GOLF": ("SJUMP | CLIMB",  "SJUMP | UPPER | CRUSH | BOUNCE"),
        "The Pig City": ("NONE",  "NONE"),
        "Peppibot Factory": ("NONE",  "NONE"),
        "Oh Shit!": ("NONE",  "NONE"),
        "Freezerator": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Pizzascare": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Don't Make A Sound": ("SJUMP | CLIMB",  "SJUMP | UPPER | CRUSH | BOUNCE"),
        "WAR": ("SJUMP", "SJUMP | CRUSH"),
        #bosses
        "Pepperman": ("NONE", "NONE"),
        "The Vigilante": ("NONE", "NONE"),
        "The Noise": ("SJUMP | CLIMB | UPPER", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "The Doise": ("SJUMP | CLIMB | UPPER", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Fake Peppino": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        #floors
        "Floor 1 Tower Lobby": ("SJUMP | CLIMB", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Floor 2 Western District": ("NONE", "NONE"),
        "Floor 3 Vacation Resort": ("SJUMP | CLIMB | UPPER", "SJUMP | UPPER | CRUSH | BOUNCE"),
        "Floor 4 Slum": ("NONE", "NONE"),
    }

    pt_swap_rules = { #for swap-specific rules
        "Chef Task: Strike!": "SLAM+DJUMP+KICK | CRUSH+KICK | BOUNCE+SLAM+KICK | UPPER+SLAM+KICK | SJUMP+SLAM+KICK",
    }

    secrets_list = get_secrets_list() 
    if not world.level_map:
        if options.randomize_levels:
            levels_map = dict(zip(levels_list, level_gate_rando(world, options.character != 0, options.difficulty)))
        else:
            levels_map = dict(zip(levels_list, levels_list))
        world.level_map = levels_map
    else:
        levels_map = world.level_map

    if not world.boss_map:
        if options.randomize_bosses:
            bosses_map = dict(zip(bosses_list, boss_gate_rando(world, options.character != 0)))
        else:
            bosses_map = dict(zip(bosses_list, bosses_list))
        world.boss_map = bosses_map
    else:
        bosses_map = world.boss_map

    if not world.secret_map:
        if options.randomize_secrets:
            secrets_map = dict(zip(secrets_list, secret_rando(world, options)))
        else:
            secrets_map = dict(zip(secrets_list, secrets_list))
        world.secret_map = secrets_map
    else:
        secrets_map = world.secret_map

    def interpret_rule(rule_chk: str, hub_rule: bool):
        if options.character != 2:
            rule_index = options.difficulty + (options.character * 2)
            if hub_rule:
                rule_str = hub_rules_dict[rule_chk][options.character]
            else:
                rule_str = rules_dict[rule_chk][rule_index]
        else:
            if hub_rule:
                rule_str = hub_rules_dict[rule_chk][0] + " | " + hub_rules_dict[rule_chk][1]
            else:
                if rule_chk in pt_swap_rules:
                    rule_str = pt_swap_rules[rule_chk]
                else:
                    rule_str = rules_dict[rule_chk][options.difficulty] + " | " + rules_dict[rule_chk][options.difficulty + 2]
        itemsets = []
        rules = rule_str.split(" | ")
        if "NONE" in rules:
            return (lambda state: True)
        for rule in rules:
            tokens = rule.split("+")
            itemsets.append([rule_moves[move] for move in tokens])
        return lambda state: rule_from_itemset(state, itemsets)

    def rule_from_itemset(state: CollectionState, itemsets):
        for itemset in itemsets:
            if itemset == [] or state.has_all(itemset, world.player):
                return True
        return False
    
    def add_s_rank_rule(lvl: str, location: Location):
        set_rule(location, interpret_rule(lvl + " S Rank", False))
        if options.shuffle_lap2:
            if "P Rank" in location.name or options.difficulty == 0 or not (lvl in lap1_levels):
                add_rule(location, lambda state: state.has("Lap 2 Portals", world.player))
    
    def add_s_ranked_task_rule(lvls: list, location: Location):
        for lvl in lvls:
            add_rule(location, interpret_rule(lvl + " S Rank", False))
        if options.shuffle_lap2:
            add_rule(location, lambda state: state.has("Lap 2 Portals", world.player))

    #connect regions
    multiworld.get_region("Menu", world.player).connect(multiworld.get_region("Floor 1 Tower Lobby", world.player), "Menu to Floor 1 Tower Lobby")
    for i in range(4):
        multiworld.get_region(floors_list[i], world.player).connect(multiworld.get_region(floors_list[i+1], world.player), floors_list[i] + " to " + floors_list[i+1])
    
    multiworld.get_region("Floor 5 Staff Only", world.player).connect(multiworld.get_region("Pizzaface", world.player), "Floor 5 Staff Only to Pizzaface")
    multiworld.get_region("Pizzaface", world.player).connect(multiworld.get_region("The Crumbling Tower of Pizza", world.player), "Pizzaface to The Crumbling Tower of Pizza")
    if options.character != 2:
        multiworld.get_region("Floor 1 Tower Lobby", world.player).connect(multiworld.get_region("Tutorial", world.player), "Floor 1 Tower Lobby to Tutorial")
    if options.pumpkin_checks:
        multiworld.get_region("Floor 1 Tower Lobby", world.player).connect(multiworld.get_region("Tricky Treat", world.player), "Floor 1 Tower Lobby to Tricky Treat")

    for i in range(4):
        for ii in range(4):
            level_name = levels_map[levels_list[(4*i)+ii]]
            multiworld.get_region(floors_list[i], world.player).connect(multiworld.get_region(level_name, world.player), floors_list[i] + " to " + level_name)
        multiworld.get_region(floors_list[i], world.player).connect(multiworld.get_region(bosses_map[bosses_list[i]], world.player), floors_list[i] + " to " + bosses_map[bosses_list[i]])

    for i in range(3):
        level_name = levels_map[levels_list[i + 16]]
        multiworld.get_region("Floor 5 Staff Only", world.player).connect(multiworld.get_region(level_name, world.player), "Floor 5 Staff Only to " + level_name)

    #set rules
    for location in multiworld.get_locations(world.player):
        if (("S Rank" in location.name) or ("P Rank" in location.name)) and (location.parent_region.name in levels_list):
            add_s_rank_rule(location.parent_region.name, location)
        elif ("Chef Task: S Ranked" in location.name) or ("Chef Task: P Ranked" in location.name):
            if ("S Ranked" in location.name) and not options.srank_checks:
                location.progress_type = LocationProgressType.EXCLUDED
            if ("P Ranked" in location.name) and not options.prank_checks:
                location.progress_type = LocationProgressType.EXCLUDED
            lvls_on_floor = []
            if (location.parent_region.name != "Floor 5 Staff Only"):
                floor_first_lvl_index = (floors_list.index(location.parent_region.name) * 4)
                for i in range(4):
                    lvls_on_floor.append(levels_map[levels_list[floor_first_lvl_index + i]])
            else:
                floor_first_lvl_index = (floors_list.index(location.parent_region.name) * 3)
                for i in range(3):
                    lvls_on_floor.append(levels_map[levels_list[floor_first_lvl_index + i]])
            add_s_ranked_task_rule(lvls_on_floor, location)
        elif ("Chef Task: Pumpkin Munchkin" in location.name):
            for lvl in levels_list:
                add_rule(location, lambda state, level=lvl: state.can_reach(world.get_location(f"{level} Pumpkin")))
            add_rule(location, lambda state: state.can_reach(world.get_location("The Crumbling Tower of Pizza Pumpkin")))
            for i in range(5):
                add_rule(location, lambda state, index=i: state.can_reach(world.get_location(f"Tricky Treat Main Path Pumpkin {index+1}")))
                add_rule(location, lambda state, index=i: state.can_reach(world.get_location(f"Tricky Treat Side Path Pumpkin {index+1}")))
        else:
            if ("The Critic" in location.name) or ("The Ugly" in location.name) or ("Denoise" in location.name) or ("Faker" in location.name) or ("Face Off" in location.name):
                if not options.prank_checks:
                    location.progress_type = LocationProgressType.EXCLUDED
            set_rule(location, interpret_rule(location.name, False))

    def get_toppin_prop(perc: int) -> int:
        return floor(toppins * (perc / 100))

    #access rules for floors
    for i in range(4): 
        if options.bonus_ladders < (i+1):
            set_rule(multiworld.get_entrance(floors_list[i] + " to " + floors_list[i+1], world.player), interpret_rule(floors_list[i], True))

    #access rules for levels
    for i in range(4):
        if options.bonus_ladders < (i+1):
            for ii in range(4):
                level_name = levels_map[levels_list[(4*i)+ii]]
                set_rule(multiworld.get_entrance(floors_list[i] + " to " + level_name, world.player), interpret_rule(levels_list[(4*i)+ii], True))
    for i in range(3):
        if options.bonus_ladders < 5:
            level_name = levels_map[levels_list[i+16]]
            set_rule(multiworld.get_entrance("Floor 5 Staff Only to " + level_name, world.player), interpret_rule(levels_list[i+16], True))

    #access rules for bosses
    for i in range(4):
        if options.bonus_ladders < (i+1):
            set_rule(multiworld.get_entrance(floors_list[i] + " to " + bosses_map[bosses_list[i]], world.player), interpret_rule(bosses_list[i], True))
    #...and pizzaface
    if options.bonus_ladders < 5:
        if "Superjump" in options.move_rando_list and options.do_move_rando: set_rule(multiworld.get_entrance("Floor 5 Staff Only to Pizzaface", world.player), lambda state: state.has("Superjump", world.player))
        #if options.character != 0 and "Crusher" in options.move_rando_list and options.do_move_rando: add_rule(multiworld.get_entrance("Floor 5 Staff Only to Pizzaface", world.player), lambda state: state.has("Crusher", world.player))

    #toppin requirements for bosses
    add_rule(multiworld.get_entrance("Floor 1 Tower Lobby to " + bosses_map["Pepperman"], world.player), lambda state: state.has("Toppin", world.player, get_toppin_prop(options.floor_1_cost)))
    add_rule(multiworld.get_entrance("Floor 2 Western District to " + bosses_map["The Vigilante"], world.player), lambda state: state.has("Toppin", world.player, get_toppin_prop(options.floor_2_cost)))
    add_rule(multiworld.get_entrance("Floor 3 Vacation Resort to " + bosses_map[bosses_list[2]], world.player), lambda state: state.has("Toppin", world.player, get_toppin_prop(options.floor_3_cost))) #the noise or the doise, depending on character played
    add_rule(multiworld.get_entrance("Floor 4 Slum to " + bosses_map["Fake Peppino"], world.player), lambda state: state.has("Toppin", world.player, get_toppin_prop(options.floor_4_cost)))
    add_rule(multiworld.get_entrance("Floor 5 Staff Only to Pizzaface", world.player), lambda state: state.has("Toppin", world.player, get_toppin_prop(options.floor_5_cost)))

    #pumpkin requirement for tricky treat
    if options.pumpkin_checks:
        add_rule(multiworld.get_entrance("Floor 1 Tower Lobby to Tricky Treat", world.player), lambda state: state.has("Pumpkin", world.player, floor(pumpkins * (options.tricky_treat_cost / 100))))

    #boss key requirements for floors
    if not options.open_world:
        add_rule(multiworld.get_entrance("Floor 1 Tower Lobby to Floor 2 Western District", world.player), lambda state: state.has("Boss Key", world.player, 1))
        add_rule(multiworld.get_entrance("Floor 2 Western District to Floor 3 Vacation Resort", world.player), lambda state: state.has("Boss Key", world.player, 2))
        add_rule(multiworld.get_entrance("Floor 3 Vacation Resort to Floor 4 Slum", world.player), lambda state: state.has("Boss Key", world.player, 3))
        add_rule(multiworld.get_entrance("Floor 4 Slum to Floor 5 Staff Only", world.player), lambda state: state.has("Boss Key", world.player, 4))