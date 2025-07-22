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
    "LAP2": "Lap 2 Portals"
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
            "SJUMP", 
            "SJUMP | CLIMB", 
            "SJUMP", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Mushroom Toppin": (
            "SJUMP | CLIMB | UPPER", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Cheese Toppin": (
            "SJUMP | CLIMB | UPPER", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Tomato Toppin": (
            "SJUMP | CLIMB | UPPER", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Sausage Toppin": (
            "SJUMP", 
            "SJUMP | CLIMB", 
            "SJUMP", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Pineapple Toppin": (
            "SJUMP", 
            "SJUMP | CLIMB", 
            "SJUMP", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Secret 1": (
            "SJUMP | CLIMB | UPPER", 
            "SJUMP | CLIMB | UPPER | GRAB | SLAM", 
            "SJUMP | BOUNCE | CRUSH | UPPER", 
            "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM"
        ),
        "John Gutter Secret 2": (
            "SJUMP+SLAM", 
            "SJUMP | CLIMB", 
            "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Secret 3": (
            "SJUMP", 
            "SJUMP | CLIMB", 
            "SJUMP", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "John Gutter Treasure": (
            "SJUMP", 
            "SJUMP | CLIMB", 
            "SJUMP", 
            "SJUMP | UPPER | CRUSH | BOUNCE"
        ),
        "Chef Task: John Gutted": (
			"SJUMP", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Primate Rage": (
			"LAP2+SJUMP", 
			"LAP2+SJUMP | LAP2+CLIMB", 
			"LAP2+SJUMP", 
			"LAP2+SJUMP | LAP2+UPPER | LAP2+CRUSH | LAP2+BOUNCE"
		),
        "Chef Task: Let's Make This Quick": (
			"CLIMB+SJUMP+MACH4", 
			"SJUMP | CLIMB", 
			"SJUMP+MACH4", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "John Gutter S Rank": (
			"SJUMP+SLAM", 
			"SJUMP | CLIMB", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),

    #Pizzascape
        "Pizzascape Complete": (
			"GRAB+CLIMB", 
			"UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+UPPER | GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH", 
			"GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH"
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
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape Sausage Toppin": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape Pineapple Toppin": (
			"GRAB","UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape Secret 1": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape Secret 2": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape Secret 3": (
			"GRAB+SJUMP", 
			"UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP", 
			"GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH"
		),
        "Pizzascape Treasure": (
			"GRAB+SJUMP | GRAB+CLIMB", 
			"UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP", 
			"GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH"
		),
        "Chef Task: Shining Armor": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB+UPPER | GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH", 
			"GRAB | UPPER"
		),
        "Chef Task: Spoonknight": (
			"TAUNT", 
			"TAUNT", 
			"TAUNT", 
			"TAUNT"
		),
        "Chef Task: Spherical": (
			"GRAB", 
			"UPPER | GRAB", 
			"GRAB", 
			"GRAB | UPPER"
		),
        "Pizzascape S Rank": (
			"GRAB+CLIMB", 
			"UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP", 
			"GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH"
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
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE"
		),

    #Oregano Desert
        "Oregano Desert Complete": (
			"CLIMB", 
			"SJUMP+GRAB | UPPER+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Mushroom Toppin": (
			"SJUMP | CLIMB", 
			"UPPER | SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Cheese Toppin": (
			"SJUMP | CLIMB", 
			"UPPER+GRAB | SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Tomato Toppin": (
			"CLIMB", 
			"UPPER+GRAB | SJUMP+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Sausage Toppin": (
			"CLIMB", 
			"UPPER+GRAB | SJUMP+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Pineapple Toppin": (
			"CLIMB", 
			"UPPER+GRAB | SJUMP+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Secret 1": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"BOUNCE", 
			"SJUMP | BOUNCE"
		),
        "Oregano Desert Secret 2": (
			"CLIMB", 
			"CLIMB", 
			 "SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Secret 3": (
			"CLIMB", 
			"CLIMB", 
			 "SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert Treasure": (
			"CLIMB", 
			"CLIMB", 
			 "SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Peppino's Rain Dance": (
			"SJUMP | CLIMB", 
			"UPPER | SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Unnecessary Violence": (
			"CLIMB", 
			"CLIMB", 
			 "SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Alien Cow": (
			"CLIMB", 
			"SJUMP+GRAB | UPPER+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Oregano Desert S Rank": (
			"CLIMB", 
			"SJUMP+GRAB | UPPER+GRAB | CLIMB", 
			"BOUNCE", 
			"SJUMP | BOUNCE"
		),

    #Wasteyard
        "Wasteyard Complete": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Mushroom Toppin": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Wasteyard Cheese Toppin": (
			"SJUMP | CLIMB", 
			"NONE", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"NONE"
		),
        "Wasteyard Tomato Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Sausage Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Pineapple Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Secret 1": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Secret 2": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Secret 3": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Treasure": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Alive and Well": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Pretend Ghost": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Chef Task: Ghosted": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | UPPER | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard S Rank": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),

    #Fun Farm
        "Fun Farm Complete": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),
        "Fun Farm Mushroom Toppin": (
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Cheese Toppin": (
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Tomato Toppin": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Sausage Toppin": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Pineapple Toppin": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),
        "Fun Farm Secret 1": (
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Secret 2": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm Secret 3": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),
        "Fun Farm Treasure": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),
        "Chef Task: Good Egg": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),
        "Chef Task: No One Is Safe": (
			"SLAM+CLIMB+STAUNT", 
			"SLAM+STAUNT+SJUMP | SLAM+STAUNT+CLIMB", 
			"BOUNCE+SLAM+STAUNT | UPPER+SLAM+STAUNT | SJUMP+SLAM+STAUNT | BOUNCE+TORN+STAUNT | UPPER+TORN+STAUNT | SJUMP+TORN+STAUNT | CRUSH+STAUNT", 
			"CRUSH+STAUNT | SLAM+UPPER+STAUNT | SLAM+BOUNCE+STAUNT | SLAM+SJUMP+STAUNT"
		),
        "Chef Task: Cube Menace": (
			"SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER", 
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fun Farm S Rank": (
			"SLAM+CLIMB+SJUMP", 
			"LAP2+SLAM+GRAB+CLIMB | LAP2+SLAM+SJUMP", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH", 
			"CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP"
		),

    #Fastfood Saloon
        "Fastfood Saloon Complete": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Mushroom Toppin": (
			"SJUMP", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Fastfood Saloon Cheese Toppin": (
			"SJUMP+GRAB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Tomato Toppin": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Sausage Toppin": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Pineapple Toppin": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Secret 1": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Secret 2": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon Secret 3": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
	    "Fastfood Saloon Treasure": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Chef Task: Royal Flush": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Chef Task: Non-Alcoholic": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Chef Task: Already Pressed": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Fastfood Saloon S Rank": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),

    #Crust Cove
        "Crust Cove Complete": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Crust Cove Mushroom Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Crust Cove Cheese Toppin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Crust Cove Tomato Toppin": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Crust Cove Sausage Toppin": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Crust Cove Pineapple Toppin": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Crust Cove Secret 1": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Crust Cove Secret 2": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Crust Cove Secret 3": (
			"CLIMB+SLAM+TAUNT", 
			"SLAM+CLIMB+TAUNT | SLAM+SJUMP+UPPER+TAUNT", 
			"SJUMP+SLAM+TAUNT | SJUMP+CRUSH+TAUNT | SJUMP+TORN+TAUNT", 
			"CRUSH+TAUNT | SJUMP+TORN+TAUNT | SJUMP+SLAM+TAUNT | SJUMP+BOUNCE+TAUNT"
		),
        "Crust Cove Treasure": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"CRUSH | SJUMP"
		),
        "Chef Task: Demolition Expert": (
			"CLIMB+SLAM", 
			"SLAM+CLIMB | SLAM+SJUMP+UPPER", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Chef Task: Blowback": (
			"SJUMP+TAUNT | CLIMB+TAUNT", 
			"SJUMP+TAUNT | CLIMB+TAUNT", 
			 "SJUMP+TAUNT", 
			"CRUSH+TAUNT | SJUMP+TAUNT"
		),
        "Chef Task: X": (
			"CLIMB+SLAM", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN", 
			"CRUSH | SJUMP+SLAM | BOUNCE+SLAM | UPPER+SLAM"
		),
        "Crust Cove S Rank": (
			"CLIMB+SLAM+TAUNT", 
			"SLAM+CLIMB+TAUNT | SLAM+SJUMP+UPPER+TAUNT", 
			"SJUMP+SLAM+TAUNT | SJUMP+CRUSH+TAUNT | SJUMP+TORN+TAUNT", 
			"CRUSH+TAUNT | SJUMP+TORN+TAUNT | SJUMP+SLAM+TAUNT | SJUMP+BOUNCE+TAUNT"
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

    #Deep-Dish 9
        "Deep-Dish 9 Complete": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Deep-Dish 9 Mushroom Toppin": (
			"SLAM", 
			"SLAM", 
			"SLAM | CRUSH | TORN", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Deep-Dish 9 Cheese Toppin": (
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			 "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Deep-Dish 9 Tomato Toppin": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Deep-Dish 9 Sausage Toppin": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Deep-Dish 9 Pineapple Toppin": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Deep-Dish 9 Secret 1": (
			"SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Deep-Dish 9 Secret 2": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Deep-Dish 9 Secret 3": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Deep-Dish 9 Treasure": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Chef Task: Blast 'Em Asteroids": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Chef Task: Turbo Tunnel": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Chef Task: Man Meteor": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+BOUNCE | SLAM+UPPER", 
			"SJUMP+SLAM | UPPER+SLAM | CRUSH+SLAM | BOUNCE+SLAM"
		),
        "Deep-Dish 9 S Rank": (
			"SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),

    #GOLF
        "GOLF Complete": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Mushroom Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Cheese Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Tomato Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Sausage Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Pineapple Toppin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Secret 1": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Secret 2": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Secret 3": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF Treasure": (
			"GRAB+CLIMB | GRAB+SJUMP", 
			"SJUMP | CLIMB+GRAB | CLIMB+SLAM", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"SJUMP | BOUNCE | CRUSH | UPPER"
		),
        "Chef Task: Primo Golfer": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "Chef Task: Helpful Burger": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "Chef Task: Nice Shot": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"NONE"
		),
        "GOLF S Rank": (
			"GRAB+CLIMB | GRAB+SJUMP", 
			"SJUMP | CLIMB+GRAB | CLIMB+SLAM", 
			"SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB", 
			"SJUMP | BOUNCE | CRUSH | UPPER"
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
			"SLAM+DJUMP", 
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

    #Peppibot Factory
        "Peppibot Factory Complete": (
			"SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM", 
			"SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
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
			"SJUMP+CLIMB | SJUMP+UPPER", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Peppibot Factory Pineapple Toppin": (
			"SJUMP+CLIMB | SJUMP+UPPER", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
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
			"SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM", 
			"SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Peppibot Factory Treasure": (
			"SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM", 
			"SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Chef Task: There Can Be Only One": (
			"LAP2+SJUMP+CLIMB+SLAM | LAP2+SJUMP+UPPER+SLAM", 
			"LAP2+SJUMP+SLAM | LAP2+CLIMB+GRAB+SLAM | LAP2+CLIMB+UPPER+SLAM", 
			"LAP2+SJUMP+SLAM | LAP2+SJUMP+TORN | LAP2+SJUMP+CRUSH", 
			"LAP2+SJUMP+BOUNCE | LAP2+SJUMP+TORN | LAP2+UPPER+BOUNCE | LAP2+UPPER+TORN | LAP2+CRUSH"
		),
        "Chef Task: Whoop This!": (
			"SJUMP", 
			"SJUMP | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Chef Task: Unflattening": (
			"SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM", 
			"SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),
        "Peppibot Factory S Rank": (
			"SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM", 
			"SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM", 
			"SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH", 
			"SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH"
		),

    #Oh Shit!
        "Oh Shit! Complete": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
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
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Sausage Toppin": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Pineapple Toppin": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Secret 1": (
			"SLAM", 
			"SLAM", 
			"SLAM | TORN | CRUSH", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Oh Shit! Secret 2": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Secret 3": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! Treasure": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Chef Task: Food Clan": (
			"SLAM+CLIMB+TAUNT", 
			"SLAM+SJUMP+TAUNT | SLAM+CLIMB+TAUNT | SLAM+UPPER+TAUNT", 
			"SLAM+BOUNCE+TAUNT | TORN+BOUNCE+TAUNT | CRUSH+TAUNT | SLAM+SJUMP+TAUNT | TORN+SJUMP+TAUNT | SLAM+UPPER+TAUNT | TORN+UPPER+TAUNT", 
			"SJUMP+SLAM+TAUNT | SJUMP+TORN+TAUNT | BOUNCE+TAUNT | CRUSH+TAUNT | UPPER+SLAM+TAUNT | UPPER+TORN+TAUNT"
		),
        "Chef Task: Can't Fool Me": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Chef Task: Penny Pincher": (
			"SLAM+CLIMB+SJUMP", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Oh Shit! S Rank": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
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
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Secret 3": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),
        "Pizzascare Treasure": (
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
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
			"CLIMB+SLAM", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH", 
			"CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE"
		),

    #Don't Make A Sound
        "Don't Make A Sound Complete": (
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
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
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
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
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
		),
        "Chef Task: Let Them Sleep": (
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
		),
        "Chef Task: Jumpspared": (
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
		),
        "Chef Task: And This... Is My Gun On A Stick!": (
			"CLIMB+SLAM+GRAB", 
			"CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP+SLAM+GRAB", 
			"SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER"
		),
        "Don't Make A Sound S Rank": (
			"CLIMB+SLAM+GRAB+TAUNT", 
			"CLIMB+GRAB+SLAM+TAUNT | CLIMB+UPPER+SLAM+TAUNT", 
			"SJUMP+GRAB+SLAM+TAUNT | SJUMP+UPPER+SLAM+TAUNT | SJUMP+GRAB+TORN+TAUNT | SJUMP+UPPER+TORN+TAUNT | CRUSH+GRAB+TAUNT | CRUSH+UPPER+TAUNT | BOUNCE+GRAB+TAUNT | BOUNCE+UPPER+TAUNT"
		),

    #WAR
        "WAR Complete": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH"
		),
        "WAR Mushroom Toppin": (
			"GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE | GRAB+SJUMP", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Cheese Toppin": (
			"GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE | GRAB+SJUMP", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Tomato Toppin": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Sausage Toppin": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Pineapple Toppin": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH"
		),
        "WAR Secret 1": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Secret 2": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Secret 3": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "WAR Treasure": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "Chef Task: Trip to the Warzone": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM+MACH4 | UPPER+SLAM+MACH4", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH"
		),
        "Chef Task: Sharpshooter": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH"
		),
        "Chef Task: Decorated Veteran": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH"
		),
        "WAR S Rank": (
			"GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN", 
			"GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH"
		),

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": (
			"SLAM+SJUMP+CLIMB", 
			"GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH", 
			"SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB"
		),
        "The Crumbling Tower of Pizza S Rank": (
			"SLAM+SJUMP+CLIMB", 
			"GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH", 
			"SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB"
		),
        "The Crumbling Tower of Pizza P Rank": (
			"SLAM+SJUMP+CLIMB", 
			"GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB", 
			"GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH", 
			"SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB"
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
			"GRAB", 
			"GRAB", 
			"BOMB", 
			"BOMB"
		),
        "Chef Task: The Ugly": (
			"GRAB", 
			"GRAB", 
			"BOMB", 
			"BOMB"
		),
        "The Vigilante S Rank": (
			"GRAB", 
			"GRAB", 
			"BOMB", 
			"BOMB"
		),
        "The Vigilante P Rank": (
			"GRAB", 
			"GRAB", 
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
			"GRAB", 
			"GRAB", 
			"BOMB", 
			"BOMB", 
			"BOMB"
		),
        "Chef Task: Face Off": (
			"GRAB", 
			"GRAB", 
			"BOMB", 
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

    #pumpkins
        "John Gutter Pumpkin": (
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | CLIMB | UPPER | GRAB", 
			"SJUMP | BOUNCE | UPPER | CRUSH", 
			"SJUMP | BOUNCE | UPPER | GRAB | CRUSH"
		),
        "Pizzascape Pumpkin": (
			"GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+BOUNCE | GRAB+UPPER", 
			"GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH | UPPER"
		),
        "Ancient Cheese Pumpkin": (
			"GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP", 
			"UPPER+SLAM+CLIMB | UPPER+SLAM+SJUMP | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM", 
			"GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH", 
			"GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH"
		),
        "Bloodsauce Dungeon Pumpkin": (
			"SLAM", 
			"SLAM", 
			"SLAM | CRUSH | BOUNCE | TORN", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "Oregano Desert Pumpkin": (
			"CLIMB", 
			"UPPER+GRAB | SJUMP+GRAB | CLIMB", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Wasteyard Pumpkin": (
			"SJUMP | CLIMB", 
			"SJUMP | CLIMB | UPPER", 
			"SJUMP | UPPER | CRUSH | BOUNCE", 
			"SJUMP | UPPER | CRUSH | BOUNCE"
		),
        "Fun Farm Pumpkin": (
			"SLAM+CLIMB", 
			"SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB", 
			"BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Fastfood Saloon Pumpkin": (
			"SJUMP+GRAB+CLIMB", 
			"GRAB+SJUMP | GRAB+CLIMB", 
			"SJUMP+GRAB", 
			"SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB"
		),
        "Crust Cove Pumpkin": (
			"CLIMB+SLAM+SJUMP", 
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE | SJUMP+CRUSH", 
			"CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE"
		),
        "Gnome Forest Pumpkin": (
			"SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK", 
			"SLAM+DJUMP", 
			"CRUSH", 
			"CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM"
		),
        "Deep-Dish 9 Pumpkin": (
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | SLAM+CLIMB", 
			"SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER", 
			"SLAM | CRUSH | BOUNCE | TORN"
		),
        "GOLF Pumpkin": (
			"GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER", 
			"NONE", 
			"GRAB+BOUNCE | GRAB+UPPER | GRAB+SJUMP | GRAB+CRUSH", 
			"NONE"
		),
        "The Pig City Pumpkin": (
			"SLAM+DJUMP", 
			"SLAM+DJUMP", 
			"SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM", 
			"CRUSH | SLAM"
		),
        "Peppibot Factory Pumpkin": (
			"SJUMP+CLIMB | SJUMP+UPPER", 
			"SJUMP+UPPER | CLIMB+GRAB | CLIMB+UPPER", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER"
		),
        "Oh Shit! Pumpkin": (
			"SLAM+CLIMB", 
			"SLAM+CLIMB", 
			"SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER", 
			"SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN"
		),
        "Freezerator Pumpkin": (
			"CLIMB+SLAM+SJUMP", 
			"SJUMP+SLAM | CLIMB+SLAM", 
			"NONE", 
			"NONE"
		),
        "Pizzascare Pumpkin": (
			"SJUMP | CLIMB", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Don't Make A Sound Pumpkin": (
			"CLIMB", 
			"SJUMP | CLIMB", 
			"SJUMP", 
			"SJUMP | CRUSH | UPPER | BOUNCE"
		),
        "WAR Pumpkin": (
			"GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM", 
			"GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM", 
			"GRAB+BOUNCE | GRAB+SJUMP", 
			"GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM"
		),
        "The Crumbling Tower of Pizza Pumpkin": (
			"GRAB+SLAM", 
			"GRAB+SLAM | UPPER+SLAM", 
			"GRAB+SLAM | GRAB+TORN | GRAB+CRUSH", 
			"GRAB+SLAM | GRAB+TORN | GRAB+CRUSH | GRAB+BOUNCE | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH | UPPER+BOUNCE"
		),
        "Tricky Treat Main Path Pumpkin 1": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Tricky Treat Main Path Pumpkin 2": (
			"NONE", 
			"NONE", 
			"NONE", 
			"NONE"
		),
        "Tricky Treat Main Path Pumpkin 3": (
			"UPPER | CLIMB | SJUMP", 
			"UPPER | CLIMB | SJUMP", 
			"UPPER | BOUNCE | SJUMP | CRUSH", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Main Path Pumpkin 4": (
			"CLIMB", 
			"CLIMB", 
			"BOUNCE | SJUMP", 
			"BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Main Path Pumpkin 5": (
			"CLIMB", 
			"CLIMB", 
			"BOUNCE+UPPER | SJUMP", 
			"BOUNCE+UPPER | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 1": (
			"UPPER | CLIMB | SJUMP", 
			"UPPER | CLIMB | SJUMP", 
			"UPPER | BOUNCE | SJUMP | CRUSH", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 2": (
			"CLIMB | SJUMP", 
			"CLIMB | SJUMP", 
			"UPPER | BOUNCE | SJUMP | CRUSH", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 3": (
			"UPPER | CLIMB | SJUMP", 
			"UPPER | CLIMB | SJUMP", 
			"UPPER | BOUNCE | SJUMP | CRUSH", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 4": (
			"CLIMB | SJUMP", 
			"CLIMB | SJUMP", 
			"UPPER | BOUNCE | SJUMP", 
			"UPPER | BOUNCE | SJUMP | CRUSH"
		),
        "Tricky Treat Side Path Pumpkin 5": (
			"CLIMB", 
			"CLIMB", 
			"BOUNCE | SJUMP", 
			"BOUNCE | SJUMP | CRUSH"
		),
        "Chef Task: Tricksy": (
			"CLIMB", 
			"CLIMB", 
			"BOUNCE+UPPER | SJUMP", 
			"BOUNCE+UPPER | SJUMP | CRUSH"
		),
    }

    access_rules_dict = { #tuples in this format: (pep, noise)
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
        "Deep-Dish 9": ("SJUMP | CLIMB",  "SJUMP | UPPER | CRUSH | BOUNCE"),
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

    def interpret_rule(rule_chk: str, access_rule: bool):
        if options.character != 2:
            rule_index = options.difficulty + (options.character * 2)
            if access_rule:
                rule_str = access_rules_dict[rule_chk][options.character]
            else:
                rule_str = rules_dict[rule_chk][rule_index]
        else:
            if access_rule:
                rule_str = access_rules_dict[rule_chk][0] + " | " + access_rules_dict[rule_chk][1]
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
            itemsets.append([rule_moves[move] for move in tokens if ((rule_moves[move] in options.move_rando_list and options.do_move_rando) or ("LAP2" in move and options.shuffle_lap2))])
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
            add_rule(location, lambda state: state.has("Pumpkin", world.player, floor(pumpkins * (options.tricky_treat_cost / 100))))
            lvls = levels_list.copy()
            lvls.append("The Crumbling Tower of Pizza")
            for lvl in lvls:
                add_rule(location, interpret_rule(lvl + " Pumpkin", False))
            for i in range(5):
                add_rule(location, interpret_rule(f"Tricky Treat Main Path Pumpkin {i+1}", False))
                add_rule(location, interpret_rule(f"Tricky Treat Side Path Pumpkin {i+1}", False))
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
            set_rule(multiworld.get_entrance("Floor 5 Staff Only to " + level_name, world.player), interpret_rule(levels_list[i+16], 1))

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