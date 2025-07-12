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
    "Fastfood Saloon",
    "Gnome Forest",
    "Peppibot Factory",
    "Freezerator",
    "Pizzascare"
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

    peppino_level_access_rules = {
        "John Gutter": "NONE",
        "Pizzascape": "NONE",
        "Ancient Cheese": "SJUMP | CLIMB",
        "Bloodsauce Dungeon": "SJUMP | CLIMB",
        "Oregano Desert": "NONE",
        "Wasteyard": "NONE",
        "Fun Farm": "NONE",
        "Fastfood Saloon": "NONE",
        "Crust Cove": "NONE",
        "Gnome Forest": "SJUMP | CLIMB | UPPER", 
        "Deep-Dish 9": "SJUMP | CLIMB",
        "GOLF": "SJUMP | CLIMB", 
        "The Pig City": "NONE", 
        "Peppibot Factory": "NONE", 
        "Oh Shit!": "NONE", 
        "Freezerator": "SJUMP | CLIMB",
        "Pizzascare": "SJUMP | CLIMB",
        "Don't Make A Sound": "SJUMP | CLIMB", 
        "WAR": "SJUMP",
    }

    peppino_boss_access_rules = {
        "Pepperman": "NONE",
        "The Vigilante": "NONE",
        "The Noise": "SJUMP | CLIMB | UPPER",
        "The Doise": "SJUMP | CLIMB | UPPER",
        "Fake Peppino": "SJUMP | CLIMB"
    }

    peppino_next_floor_access_rules = {
        "Floor 1 Tower Lobby": "SJUMP | CLIMB",
        "Floor 2 Western District": "NONE",
        "Floor 3 Vacation Resort": "SJUMP | CLIMB | UPPER",
        "Floor 4 Slum": "NONE"
    }

    pt_peppino_rules = { #access rules within levels, which do not change
    #John Gutter
        "John Gutter Complete": "SJUMP | CLIMB",
        "John Gutter Mushroom Toppin": "SJUMP | CLIMB | UPPER | GRAB | SLAM",
        "John Gutter Cheese Toppin": "SJUMP | CLIMB | UPPER | GRAB | SLAM",
        "John Gutter Tomato Toppin": "SJUMP | CLIMB | UPPER | GRAB | SLAM",
        "John Gutter Sausage Toppin": "SJUMP | CLIMB",
        "John Gutter Pineapple Toppin": "SJUMP | CLIMB",
        "John Gutter Secret 1": "SJUMP | CLIMB | UPPER | GRAB | SLAM",
        "John Gutter Secret 2": "SJUMP | CLIMB",
        "John Gutter Secret 3": "SJUMP | CLIMB",
        "John Gutter Treasure": "SJUMP | CLIMB",
        "Chef Task: John Gutted": "SJUMP | CLIMB",
        "Chef Task: Primate Rage": "LAP2+SJUMP | LAP2+CLIMB",
        "Chef Task: Let's Make This Quick": "SJUMP | CLIMB",
        "John Gutter S Rank": "SJUMP | CLIMB",

    #Pizzascape
        "Pizzascape Complete": "UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB",
        "Pizzascape Mushroom Toppin": "NONE",
        "Pizzascape Cheese Toppin": "NONE",
        "Pizzascape Tomato Toppin": "UPPER | GRAB",
        "Pizzascape Sausage Toppin": "UPPER | GRAB",
        "Pizzascape Pineapple Toppin": "UPPER | GRAB",
        "Pizzascape Secret 1": "UPPER | GRAB",
        "Pizzascape Secret 2": "UPPER | GRAB",
        "Pizzascape Secret 3": "UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB",
        "Pizzascape Treasure": "UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB",
        "Chef Task: Shining Armor": "UPPER | GRAB",
        "Chef Task: Spoonknight": "TAUNT",
        "Chef Task: Spherical": "UPPER | GRAB",
        "Pizzascape S Rank": "UPPER+SJUMP | UPPER+CLIMB | GRAB+SJUMP | GRAB+CLIMB",

    #Ancient Cheese
        "Ancient Cheese Complete": "UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Ancient Cheese Mushroom Toppin": "NONE",
        "Ancient Cheese Cheese Toppin": "UPPER | GRAB",
        "Ancient Cheese Tomato Toppin": "UPPER | GRAB+CLIMB | GRAB+SJUMP",
        "Ancient Cheese Sausage Toppin": "UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Ancient Cheese Pineapple Toppin": "UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Ancient Cheese Secret 1": "NONE",
        "Ancient Cheese Secret 2": "UPPER | GRAB+CLIMB | GRAB+SJUMP",
        "Ancient Cheese Secret 3": "UPPER+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Ancient Cheese Treasure": "UPPER+CLIMB | UPPER+SJUMP | GRAB+CLIMB | GRAB+SJUMP",
        "Chef Task: Thrill Seeker": "UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Chef Task: Volleybomb": "UPPER | GRAB+CLIMB | GRAB+SJUMP",
        "Chef Task: Delicacy": "NONE",
        "Ancient Cheese S Rank": "UPPER+CLIMB+SLAM | UPPER+SJUMP+SLAM | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",

    #Bloodsauce Dungeon
        "Bloodsauce Dungeon Complete": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon Mushroom Toppin": "NONE",
        "Bloodsauce Dungeon Cheese Toppin": "NONE",
        "Bloodsauce Dungeon Tomato Toppin": "SLAM",
        "Bloodsauce Dungeon Sausage Toppin": "SLAM",
        "Bloodsauce Dungeon Pineapple Toppin": "SLAM",
        "Bloodsauce Dungeon Secret 1": "NONE",
        "Bloodsauce Dungeon Secret 2": "SJUMP+SLAM",
        "Bloodsauce Dungeon Secret 3": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon Treasure": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Eruption Man": "SJUMP+SLAM",
        "Chef Task: Very Very Hot Sauce": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Unsliced Pizzaman": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon S Rank": "SJUMP+SLAM | CLIMB+SLAM",

    #Oregano Desert
        "Oregano Desert Complete": "SJUMP+GRAB | UPPER+GRAB | CLIMB",
        "Oregano Desert Mushroom Toppin": "UPPER | SJUMP | CLIMB",
        "Oregano Desert Cheese Toppin": "UPPER+GRAB | SJUMP | CLIMB",
        "Oregano Desert Tomato Toppin": "UPPER+GRAB | SJUMP+GRAB | CLIMB",
        "Oregano Desert Sausage Toppin": "UPPER+GRAB | SJUMP+GRAB | CLIMB",
        "Oregano Desert Pineapple Toppin": "UPPER+GRAB | SJUMP+GRAB | CLIMB",
        "Oregano Desert Secret 1": "SJUMP | CLIMB",
        "Oregano Desert Secret 2": "CLIMB",
        "Oregano Desert Secret 3": "CLIMB",
        "Oregano Desert Treasure": "CLIMB",
        "Chef Task: Peppino's Rain Dance": "UPPER | SJUMP | CLIMB",
        "Chef Task: Unnecessary Violence": "CLIMB",
        "Chef Task: Alien Cow": "SJUMP+GRAB | UPPER+GRAB | CLIMB",
        "Oregano Desert S Rank": "SJUMP+GRAB | UPPER+GRAB | CLIMB",

    #Wasteyard
        "Wasteyard Complete": "SJUMP | CLIMB",
        "Wasteyard Mushroom Toppin": "NONE",
        "Wasteyard Cheese Toppin": "NONE",
        "Wasteyard Tomato Toppin": "SJUMP | CLIMB | UPPER",
        "Wasteyard Sausage Toppin": "SJUMP | CLIMB | UPPER",
        "Wasteyard Pineapple Toppin": "SJUMP | CLIMB | UPPER",
        "Wasteyard Secret 1": "SJUMP | CLIMB",
        "Wasteyard Secret 2": "SJUMP | CLIMB | UPPER",
        "Wasteyard Secret 3": "SJUMP | CLIMB",
        "Wasteyard Treasure": "SJUMP | CLIMB",
        "Chef Task: Alive and Well": "SJUMP | CLIMB",
        "Chef Task: Pretend Ghost": "SJUMP | CLIMB",
        "Chef Task: Ghosted": "SJUMP | CLIMB",
        "Wasteyard S Rank": "SJUMP | CLIMB",

    #Fun Farm
        "Fun Farm Complete": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Mushroom Toppin": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Cheese Toppin": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Tomato Toppin": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Sausage Toppin": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Pineapple Toppin": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Secret 1": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Secret 2": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Secret 3": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Treasure": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Good Egg": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: No One Is Safe": "SLAM+STAUNT+SJUMP | SLAM+STAUNT+CLIMB",
        "Chef Task: Cube Menace": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm S Rank": "LAP2+SLAM+GRAB+CLIMB | LAP2+SLAM+SJUMP",

    #Fastfood Saloon
        "Fastfood Saloon Complete": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Mushroom Toppin": "SJUMP | CLIMB",
        "Fastfood Saloon Cheese Toppin": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Tomato Toppin": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Sausage Toppin": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Pineapple Toppin": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Secret 1": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Secret 2": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon Secret 3": "GRAB+CLIMB",
	    "Fastfood Saloon Treasure": "GRAB+SJUMP | GRAB+CLIMB",
        "Chef Task: Royal Flush": "GRAB+SJUMP | GRAB+CLIMB",
        "Chef Task: Non-Alcoholic": "GRAB+SJUMP | GRAB+CLIMB",
        "Chef Task: Already Pressed": "GRAB+SJUMP | GRAB+CLIMB",
        "Fastfood Saloon S Rank": "GRAB+CLIMB",

    #Crust Cove
        "Crust Cove Complete": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Crust Cove Mushroom Toppin": "SJUMP | CLIMB",
        "Crust Cove Cheese Toppin": "SJUMP | CLIMB",
        "Crust Cove Tomato Toppin": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Crust Cove Sausage Toppin": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Crust Cove Pineapple Toppin": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Crust Cove Secret 1": "SJUMP | CLIMB",
        "Crust Cove Secret 2": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Crust Cove Secret 3": "SLAM+CLIMB+TAUNT | SLAM+SJUMP+UPPER+TAUNT",
        "Crust Cove Treasure": "SJUMP | CLIMB",
        "Chef Task: Demolition Expert": "SLAM+CLIMB | SLAM+SJUMP+UPPER",
        "Chef Task: Blowback": "SLAM+SJUMP+TAUNT | SLAM+CLIMB+TAUNT",
        "Chef Task: X": "SLAM+SJUMP | SLAM+CLIMB",
        "Crust Cove S Rank": "SLAM+CLIMB+TAUNT | SLAM+SJUMP+UPPER+TAUNT",

    #Gnome Forest
        "Gnome Forest Complete": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP",
        "Gnome Forest Mushroom Toppin": "SLAM+DJUMP",
        "Gnome Forest Cheese Toppin": "SLAM+DJUMP",
        "Gnome Forest Tomato Toppin": "SLAM+DJUMP",
        "Gnome Forest Sausage Toppin": "SLAM+DJUMP",
        "Gnome Forest Pineapple Toppin": "SLAM+DJUMP",
        "Gnome Forest Secret 1": "SLAM+DJUMP",
        "Gnome Forest Secret 2": "SLAM+DJUMP",
        "Gnome Forest Secret 3": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP",
        "Gnome Forest Treasure": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP",
        "Chef Task: Bee Nice": "TAUNT",
        "Chef Task: Bullseye": "TAUNT",
        "Chef Task: Lumberjack": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP",
        "Gnome Forest S Rank": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP",

    #Deep-Dish 9
        "Deep-Dish 9 Complete": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Mushroom Toppin": "SLAM",
        "Deep-Dish 9 Cheese Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Tomato Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Sausage Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Pineapple Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Secret 1": "SLAM",
        "Deep-Dish 9 Secret 2": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Secret 3": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Treasure": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Blast 'Em Asteroids": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Turbo Tunnel": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Man Meteor": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 S Rank": "SLAM+SJUMP | SLAM+CLIMB",

    #GOLF
        "GOLF Complete": "NONE",
        "GOLF Mushroom Toppin": "NONE",
        "GOLF Cheese Toppin": "NONE",
        "GOLF Tomato Toppin": "NONE",
        "GOLF Sausage Toppin": "NONE",
        "GOLF Pineapple Toppin": "NONE",
        "GOLF Secret 1": "NONE",
        "GOLF Secret 2": "NONE",
        "GOLF Secret 3": "NONE",
        "GOLF Treasure": "SJUMP | CLIMB+GRAB | CLIMB+SLAM",
        "Chef Task: Primo Golfer": "NONE",
        "Chef Task: Helpful Burger": "NONE",
        "Chef Task: Nice Shot": "NONE",
        "GOLF S Rank": "SJUMP | CLIMB+GRAB | CLIMB+SLAM",

    #The Pig City
        "The Pig City Complete": "SLAM+DJUMP",
        "The Pig City Mushroom Toppin": "NONE",
        "The Pig City Cheese Toppin": "SJUMP | CLIMB",
        "The Pig City Tomato Toppin": "SLAM",
        "The Pig City Sausage Toppin": "SLAM+DJUMP",
        "The Pig City Pineapple Toppin": "SLAM+DJUMP",
        "The Pig City Secret 1": "NONE",
        "The Pig City Secret 2": "SLAM+DJUMP",
        "The Pig City Secret 3": "SLAM+DJUMP",
        "The Pig City Treasure": "SLAM+DJUMP",
        "Chef Task: Say Oink!": "SLAM+DJUMP+TAUNT",
        "Chef Task: Pan Fried": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Strike!": "SLAM+DJUMP+KICK",
        "The Pig City S Rank": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP | UPPER+SLAM+DJUMP",

    #Peppibot Factory
        "Peppibot Factory Complete": "SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM",
        "Peppibot Factory Mushroom Toppin": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Cheese Toppin": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Tomato Toppin": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Sausage Toppin": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Pineapple Toppin": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Secret 1": "SJUMP | CLIMB",
        "Peppibot Factory Secret 2": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Peppibot Factory Secret 3": "SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM",
        "Peppibot Factory Treasure": "SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM",
        "Chef Task: There Can Be Only One": "LAP2+SJUMP+SLAM | LAP2+CLIMB+GRAB+SLAM | LAP2+CLIMB+UPPER+SLAM",
        "Chef Task: Whoop This!": "SJUMP | CLIMB+GRAB | CLIMB+UPPER",
        "Chef Task: Unflattening": "SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM",
        "Peppibot Factory S Rank": "SJUMP+SLAM | CLIMB+GRAB+SLAM | CLIMB+UPPER+SLAM",

    #Oh Shit!
        "Oh Shit! Complete": "SLAM+CLIMB",
        "Oh Shit! Mushroom Toppin": "SLAM",
        "Oh Shit! Cheese Toppin": "SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER",
        "Oh Shit! Tomato Toppin": "SLAM+CLIMB",
        "Oh Shit! Sausage Toppin": "SLAM+CLIMB",
        "Oh Shit! Pineapple Toppin": "SLAM+CLIMB",
        "Oh Shit! Secret 1": "SLAM",
        "Oh Shit! Secret 2": "SLAM+CLIMB",
        "Oh Shit! Secret 3": "SLAM+CLIMB",
        "Oh Shit! Treasure": "SLAM+CLIMB",
        "Chef Task: Food Clan": "SLAM+SJUMP+TAUNT | SLAM+CLIMB+TAUNT | SLAM+UPPER+TAUNT",
        "Chef Task: Can't Fool Me": "SLAM+CLIMB",
        "Chef Task: Penny Pincher": "SLAM+CLIMB",
        "Oh Shit! S Rank": "SLAM+CLIMB",

    #Freezerator
        "Freezerator Complete": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Mushroom Toppin": "NONE",
        "Freezerator Cheese Toppin": "SJUMP | CLIMB | UPPER",
        "Freezerator Tomato Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Sausage Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Pineapple Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Secret 1": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Secret 2": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Secret 3": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator Treasure": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Ice Climber": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Season's Greetings": "SJUMP+SLAM+STAUNT | CLIMB+SLAM+STAUNT",
        "Chef Task: Frozen Nuggets": "SJUMP+SLAM | CLIMB+SLAM",
        "Freezerator S Rank": "SJUMP+SLAM | CLIMB+SLAM",

    #Pizzascare
        "Pizzascare Complete": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Mushroom Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Cheese Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Tomato Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Sausage Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Pineapple Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Secret 1": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Secret 2": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Secret 3": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Treasure": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Haunted Playground": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Skullsplitter": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Cross To Bare": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare S Rank": "SJUMP+SLAM | CLIMB+SLAM",

    #Don't Make A Sound
        "Don't Make A Sound Complete": "CLIMB+GRAB | CLIMB+UPPER",
        "Don't Make A Sound Mushroom Toppin": "NONE",
        "Don't Make A Sound Cheese Toppin": "SJUMP | CLIMB",
        "Don't Make A Sound Tomato Toppin": "SJUMP+SLAM | CLIMB+SLAM",
        "Don't Make A Sound Sausage Toppin": "SJUMP | CLIMB",
        "Don't Make A Sound Pineapple Toppin": "CLIMB+GRAB | CLIMB+UPPER",
        "Don't Make A Sound Secret 1": "NONE",
        "Don't Make A Sound Secret 2": "SJUMP+UPPER | CLIMB",
        "Don't Make A Sound Secret 3": "SJUMP+UPPER | CLIMB",
        "Don't Make A Sound Treasure": "CLIMB+GRAB | CLIMB+UPPER",
        "Chef Task: Let Them Sleep": "CLIMB+GRAB | CLIMB+UPPER",
        "Chef Task: Jumpspared": "CLIMB+GRAB | CLIMB+UPPER",
        "Chef Task: And This... Is My Gun On A Stick!": "CLIMB+GRAB | CLIMB+UPPER",
        "Don't Make A Sound S Rank": "CLIMB+GRAB | CLIMB+UPPER",

    #WAR
        "WAR Complete": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Mushroom Toppin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Cheese Toppin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Tomato Toppin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Sausage Toppin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Pineapple Toppin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Secret 1": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Secret 2": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Secret 3": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR Treasure": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "Chef Task: Trip to the Warzone": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM+MACH4 | UPPER+SLAM+MACH4",
        "Chef Task: Sharpshooter": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB",
        "Chef Task: Decorated Veteran": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "WAR S Rank": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": "GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB",
        "The Crumbling Tower of Pizza S Rank": "GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB",
        "The Crumbling Tower of Pizza P Rank": "GRAB+SLAM+SJUMP | GRAB+SLAM+CLIMB",

    #Pepperman
        "Pepperman Defeated": "GRAB",
        "Chef Task: The Critic": "GRAB",
        "Pepperman S Rank": "GRAB",
        "Pepperman P Rank": "GRAB",

    #Vigilante
        "The Vigilante Defeated": "GRAB",
        "Chef Task: The Ugly": "GRAB",
        "The Vigilante S Rank": "GRAB",
        "The Vigilante P Rank": "GRAB",

    #Noise
        "The Noise Defeated": "NONE",
        "Chef Task: Denoise": "NONE",
        "The Noise S Rank": "NONE",
        "The Noise P Rank": "NONE",

    #Fake Pep
        "Fake Peppino Defeated": "NONE",
        "Chef Task: Faker": "NONE",
        "Fake Peppino S Rank": "NONE",
        "Fake Peppino P Rank": "NONE",

    #Pizzaface
        "Pizzaface Defeated": "GRAB",
        "Chef Task: Face Off": "GRAB",

    #Tutorial
        "Tutorial Complete": "SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB",
        "Tutorial Complete in under 2 minutes": "SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB",
        "Tutorial Mushroom Toppin": "SLAM",
        "Tutorial Cheese Toppin": "SLAM+SJUMP+GRAB | SLAM+CLIMB",
        "Tutorial Tomato Toppin": "SLAM+SJUMP+GRAB | SLAM+CLIMB",
        "Tutorial Sausage Toppin": "SLAM+SJUMP+GRAB | SLAM+CLIMB",
        "Tutorial Pineapple Toppin": "SLAM+SJUMP+GRAB | SLAM+CLIMB+GRAB",

    #misc
        "Snotty Murdered": "NONE",

    #for swap mode
        "The Doise Defeated": "NONE",
        "Chef Task: Denoise": "NONE",
        "The Doise S Rank": "NONE",
        "The Doise P Rank": "NONE",
    
    #pumpkins
        "John Gutter Pumpkin": "SJUMP | CLIMB | UPPER | GRAB",
        "Pizzascape Pumpkin": "GRAB+SJUMP | GRAB+CLIMB",
        "Ancient Cheese Pumpkin": "UPPER+SLAM+CLIMB | UPPER+SLAM+SJUMP | GRAB+CLIMB+SLAM | GRAB+SJUMP+SLAM",
        "Bloodsauce Dungeon Pumpkin": "SLAM",
        "Oregano Desert Pumpkin": "UPPER+GRAB | SJUMP+GRAB | CLIMB",
        "Wasteyard Pumpkin": "SJUMP | CLIMB | UPPER",
        "Fun Farm Pumpkin": "SLAM+UPPER+GRAB | SLAM+SJUMP | SLAM+CLIMB",
        "Fastfood Saloon Pumpkin": "GRAB+SJUMP | GRAB+CLIMB",
        "Crust Cove Pumpkin": "CLIMB+SLAM+SJUMP",
        "Gnome Forest Pumpkin": "SLAM+DJUMP",
        "Deep-Dish 9 Pumpkin": "SLAM+SJUMP | SLAM+CLIMB",
        "GOLF Pumpkin": "NONE",
        "The Pig City Pumpkin": "SLAM+DJUMP",
        "Peppibot Factory Pumpkin": "SJUMP+UPPER | CLIMB+GRAB | CLIMB+UPPER",
        "Oh Shit! Pumpkin": "SLAM+CLIMB",
        "Freezerator Pumpkin": "SJUMP+SLAM | CLIMB+SLAM",
        "Pizzascare Pumpkin": "NONE",
        "Don't Make A Sound Pumpkin": "SJUMP | CLIMB",
        "WAR Pumpkin": "GRAB+SJUMP | GRAB+CLIMB | UPPER+SJUMP | UPPER+CLIMB | GRAB+SLAM | UPPER+SLAM",
        "The Crumbling Tower of Pizza Pumpkin": "GRAB+SLAM | UPPER+SLAM",
        "Tricky Treat Main Path Pumpkin 1": "NONE",
        "Tricky Treat Main Path Pumpkin 2": "NONE",
        "Tricky Treat Main Path Pumpkin 3": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Main Path Pumpkin 4": "CLIMB",
        "Tricky Treat Main Path Pumpkin 5": "CLIMB",
        "Tricky Treat Side Path Pumpkin 1": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 2": "CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 3": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 4": "CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 5": "CLIMB",
        "Chef Task: Tricksy": "CLIMB",
    }

    pt_peppino_rules_easy = { #access rules within levels, which do not change
    #John Gutter
        "John Gutter Complete": "SJUMP",
        "John Gutter Mushroom Toppin": "SJUMP | CLIMB | UPPER",
        "John Gutter Cheese Toppin": "SJUMP | CLIMB | UPPER",
        "John Gutter Tomato Toppin": "SJUMP | CLIMB | UPPER",
        "John Gutter Sausage Toppin": "SJUMP",
        "John Gutter Pineapple Toppin": "SJUMP",
        "John Gutter Secret 1": "SJUMP | CLIMB | UPPER",
        "John Gutter Secret 2": "SJUMP+SLAM",
        "John Gutter Secret 3": "SJUMP",
        "John Gutter Treasure": "SJUMP",
        "Chef Task: John Gutted": "SJUMP",
        "Chef Task: Primate Rage": "LAP2+SJUMP",
        "Chef Task: Let's Make This Quick": "SJUMP+MACH4", 
        "John Gutter S Rank": "SJUMP+SLAM",

    #Pizzascape
        "Pizzascape Complete": "GRAB+CLIMB",
        "Pizzascape Mushroom Toppin": "NONE",
        "Pizzascape Cheese Toppin": "NONE",
        "Pizzascape Tomato Toppin": "GRAB",
        "Pizzascape Sausage Toppin": "GRAB",
        "Pizzascape Pineapple Toppin": "GRAB",
        "Pizzascape Secret 1": "GRAB",
        "Pizzascape Secret 2": "GRAB",
        "Pizzascape Secret 3": "GRAB+SJUMP",
        "Pizzascape Treasure": "GRAB+SJUMP | GRAB+CLIMB",
        "Chef Task: Shining Armor": "GRAB",
        "Chef Task: Spoonknight": "TAUNT",
        "Chef Task: Spherical": "GRAB",
        "Pizzascape S Rank": "GRAB+CLIMB",

    #Ancient Cheese
        "Ancient Cheese Complete": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "Ancient Cheese Mushroom Toppin": "NONE",
        "Ancient Cheese Cheese Toppin": "GRAB",
        "Ancient Cheese Tomato Toppin": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Ancient Cheese Sausage Toppin": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Ancient Cheese Pineapple Toppin": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Ancient Cheese Secret 1": "NONE",
        "Ancient Cheese Secret 2": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Ancient Cheese Secret 3": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Ancient Cheese Treasure": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Chef Task: Thrill Seeker": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Chef Task: Volleybomb": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Chef Task: Delicacy": "NONE",
        "Ancient Cheese S Rank": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",

    #Bloodsauce Dungeon
        "Bloodsauce Dungeon Complete": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon Mushroom Toppin": "SJUMP | CLIMB",
        "Bloodsauce Dungeon Cheese Toppin": "NONE",
        "Bloodsauce Dungeon Tomato Toppin": "SLAM",
        "Bloodsauce Dungeon Sausage Toppin": "SLAM",
        "Bloodsauce Dungeon Pineapple Toppin": "SLAM",
        "Bloodsauce Dungeon Secret 1": "NONE",
        "Bloodsauce Dungeon Secret 2": "SJUMP+SLAM",
        "Bloodsauce Dungeon Secret 3": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon Treasure": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Eruption Man": "SJUMP+SLAM",
        "Chef Task: Very Very Hot Sauce": "SJUMP+SLAM | CLIMB+SLAM",
        "Chef Task: Unsliced Pizzaman": "SJUMP+SLAM | CLIMB+SLAM",
        "Bloodsauce Dungeon S Rank": "SJUMP+SLAM | CLIMB+SLAM",

    #Oregano Desert
        "Oregano Desert Complete": "CLIMB",
        "Oregano Desert Mushroom Toppin": "SJUMP | CLIMB",
        "Oregano Desert Cheese Toppin": "SJUMP | CLIMB",
        "Oregano Desert Tomato Toppin": "CLIMB",
        "Oregano Desert Sausage Toppin": "CLIMB",
        "Oregano Desert Pineapple Toppin": "CLIMB",
        "Oregano Desert Secret 1": "SJUMP | CLIMB",
        "Oregano Desert Secret 2": "CLIMB",
        "Oregano Desert Secret 3": "CLIMB",
        "Oregano Desert Treasure": "CLIMB",
        "Chef Task: Peppino's Rain Dance": "SJUMP | CLIMB",
        "Chef Task: Unnecessary Violence": "CLIMB",
        "Chef Task: Alien Cow": "CLIMB",
        "Oregano Desert S Rank": "CLIMB",

    #Wasteyard
        "Wasteyard Complete": "SJUMP | CLIMB",
        "Wasteyard Mushroom Toppin": "NONE",
        "Wasteyard Cheese Toppin": "SJUMP | CLIMB",
        "Wasteyard Tomato Toppin": "SJUMP | CLIMB",
        "Wasteyard Sausage Toppin": "SJUMP | CLIMB",
        "Wasteyard Pineapple Toppin": "SJUMP | CLIMB",
        "Wasteyard Secret 1": "SJUMP | CLIMB",
        "Wasteyard Secret 2": "SJUMP | CLIMB",
        "Wasteyard Secret 3": "SJUMP | CLIMB",
        "Wasteyard Treasure": "SJUMP | CLIMB",
        "Chef Task: Alive and Well": "SJUMP | CLIMB",
        "Chef Task: Pretend Ghost": "SJUMP | CLIMB",
        "Chef Task: Ghosted": "SJUMP | CLIMB",
        "Wasteyard S Rank": "SJUMP | CLIMB",

    #Fun Farm
        "Fun Farm Complete": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Mushroom Toppin": "SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER",
        "Fun Farm Cheese Toppin": "SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER",
        "Fun Farm Tomato Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Sausage Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Pineapple Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Secret 1": "SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER",
        "Fun Farm Secret 2": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Secret 3": "SLAM+SJUMP | SLAM+CLIMB",
        "Fun Farm Treasure": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Good Egg": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: No One Is Safe": "SLAM+SJUMP+STAUNT | SLAM+CLIMB+STAUNT",
        "Chef Task: Cube Menace": "SLAM+SJUMP | SLAM+CLIMB | SLAM+UPPER",
        "Fun Farm S Rank": "SLAM+SJUMP",

    #Fastfood Saloon
        "Fastfood Saloon Complete": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Mushroom Toppin": "SJUMP",
        "Fastfood Saloon Cheese Toppin": "SJUMP+GRAB",
        "Fastfood Saloon Tomato Toppin": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Sausage Toppin": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Pineapple Toppin": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Secret 1": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Secret 2": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon Secret 3": "SJUMP+GRAB+CLIMB",
	    "Fastfood Saloon Treasure": "SJUMP+GRAB+CLIMB",
        "Chef Task: Royal Flush": "SJUMP+GRAB+CLIMB",
        "Chef Task: Non-Alcoholic": "SJUMP+GRAB+CLIMB",
        "Chef Task: Already Pressed": "SJUMP+GRAB+CLIMB",
        "Fastfood Saloon S Rank": "SJUMP+GRAB+CLIMB",

    #Crust Cove
        "Crust Cove Complete": "CLIMB+SLAM",
        "Crust Cove Mushroom Toppin": "SJUMP | CLIMB",
        "Crust Cove Cheese Toppin": "SJUMP | CLIMB",
        "Crust Cove Tomato Toppin": "CLIMB+SLAM",
        "Crust Cove Sausage Toppin": "CLIMB+SLAM",
        "Crust Cove Pineapple Toppin": "CLIMB+SLAM",
        "Crust Cove Secret 1": "SJUMP | CLIMB",
        "Crust Cove Secret 2": "CLIMB+SLAM",
        "Crust Cove Secret 3": "CLIMB+SLAM+TAUNT",
        "Crust Cove Treasure": "SJUMP | CLIMB",
        "Chef Task: Demolition Expert": "CLIMB+SLAM",
        "Chef Task: Blowback": "SJUMP+TAUNT | CLIMB+TAUNT",
        "Chef Task: X": "CLIMB+SLAM",
        "Crust Cove S Rank": "CLIMB+SLAM+TAUNT",

    #Gnome Forest
        "Gnome Forest Complete": "SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB",
        "Gnome Forest Mushroom Toppin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Cheese Toppin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Tomato Toppin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Sausage Toppin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Pineapple Toppin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Secret 1": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Secret 2": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Gnome Forest Secret 3": "SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB",
        "Gnome Forest Treasure": "SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB",
        "Chef Task: Bee Nice": "TAUNT",
        "Chef Task: Bullseye": "TAUNT",
        "Chef Task: Lumberjack": "SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB",
        "Gnome Forest S Rank": "SLAM+DJUMP+SPIN+SJUMP | SLAM+DJUMP+KICK+SJUMP | SLAM+DJUMP+SPIN+CLIMB | SLAM+DJUMP+KICK+CLIMB",

    #Deep-Dish 9
        "Deep-Dish 9 Complete": "SLAM+CLIMB",
        "Deep-Dish 9 Mushroom Toppin": "SLAM",
        "Deep-Dish 9 Cheese Toppin": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Tomato Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Sausage Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Pineapple Toppin": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Secret 1": "SLAM+UPPER | SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Secret 2": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 Secret 3": "SLAM+CLIMB",
        "Deep-Dish 9 Treasure": "SLAM+CLIMB",
        "Chef Task: Blast 'Em Asteroids": "SLAM+CLIMB",
        "Chef Task: Turbo Tunnel": "SLAM+SJUMP | SLAM+CLIMB",
        "Chef Task: Man Meteor": "SLAM+SJUMP | SLAM+CLIMB",
        "Deep-Dish 9 S Rank": "SLAM+CLIMB",

    #GOLF
        "GOLF Complete": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Mushroom Toppin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Cheese Toppin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Tomato Toppin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Sausage Toppin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Pineapple Toppin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Secret 1": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Secret 2": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Secret 3": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF Treasure": "GRAB+CLIMB | GRAB+SJUMP",
        "Chef Task: Primo Golfer": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "Chef Task: Helpful Burger": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "Chef Task: Nice Shot": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "GOLF S Rank": "GRAB+CLIMB | GRAB+SJUMP",

    #The Pig City
        "The Pig City Complete": "SLAM+DJUMP",
        "The Pig City Mushroom Toppin": "NONE",
        "The Pig City Cheese Toppin": "SJUMP | CLIMB",
        "The Pig City Tomato Toppin": "SLAM",
        "The Pig City Sausage Toppin": "SLAM+DJUMP",
        "The Pig City Pineapple Toppin": "SLAM+DJUMP",
        "The Pig City Secret 1": "NONE",
        "The Pig City Secret 2": "SLAM+DJUMP",
        "The Pig City Secret 3": "SLAM+DJUMP",
        "The Pig City Treasure": "SLAM+DJUMP",
        "Chef Task: Say Oink!": "SLAM+DJUMP+TAUNT",
        "Chef Task: Pan Fried": "SLAM+DJUMP",
        "Chef Task: Strike!": "SLAM+DJUMP+KICK",
        "The Pig City S Rank": "SJUMP+SLAM+DJUMP | CLIMB+SLAM+DJUMP | UPPER+SLAM+DJUMP",

    #Peppibot Factory
        "Peppibot Factory Complete": "SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM",
        "Peppibot Factory Mushroom Toppin": "SJUMP",
        "Peppibot Factory Cheese Toppin": "SJUMP+CLIMB | SJUMP+UPPER",
        "Peppibot Factory Tomato Toppin": "SJUMP+CLIMB | SJUMP+UPPER",
        "Peppibot Factory Sausage Toppin": "SJUMP+CLIMB | SJUMP+UPPER",
        "Peppibot Factory Pineapple Toppin": "SJUMP+CLIMB | SJUMP+UPPER",
        "Peppibot Factory Secret 1": "SJUMP",
        "Peppibot Factory Secret 2": "SJUMP+UPPER",
        "Peppibot Factory Secret 3": "SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM",
        "Peppibot Factory Treasure": "SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM",
        "Chef Task: There Can Be Only One": "LAP2+SJUMP+CLIMB+SLAM | LAP2+SJUMP+UPPER+SLAM",
        "Chef Task: Whoop This!": "SJUMP",
        "Chef Task: Unflattening": "SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM",
        "Peppibot Factory S Rank": "SJUMP+CLIMB+SLAM | SJUMP+UPPER+SLAM",

    #Oh Shit!
        "Oh Shit! Complete": "SLAM+CLIMB",
        "Oh Shit! Mushroom Toppin": "SLAM",
        "Oh Shit! Cheese Toppin": "SLAM+CLIMB | SLAM+SJUMP | SLAM+UPPER",
        "Oh Shit! Tomato Toppin": "SLAM+CLIMB",
        "Oh Shit! Sausage Toppin": "SLAM+CLIMB",
        "Oh Shit! Pineapple Toppin": "SLAM+CLIMB",
        "Oh Shit! Secret 1": "SLAM",
        "Oh Shit! Secret 2": "SLAM+CLIMB",
        "Oh Shit! Secret 3": "SLAM+CLIMB",
        "Oh Shit! Treasure": "SLAM+CLIMB",
        "Chef Task: Food Clan": "SLAM+CLIMB+TAUNT",
        "Chef Task: Can't Fool Me": "SLAM+CLIMB",
        "Chef Task: Penny Pincher": "SLAM+CLIMB+SJUMP",
        "Oh Shit! S Rank": "SLAM+CLIMB",

    #Freezerator
        "Freezerator Complete": "CLIMB+SLAM+SJUMP",
        "Freezerator Mushroom Toppin": "CLIMB | SJUMP",
        "Freezerator Cheese Toppin": "CLIMB",
        "Freezerator Tomato Toppin": "CLIMB+SLAM+SJUMP",
        "Freezerator Sausage Toppin": "CLIMB+SLAM+SJUMP",
        "Freezerator Pineapple Toppin": "CLIMB+SLAM+SJUMP",
        "Freezerator Secret 1": "CLIMB+SLAM+SJUMP",
        "Freezerator Secret 2": "CLIMB+SLAM+SJUMP",
        "Freezerator Secret 3": "CLIMB+SLAM+SJUMP",
        "Freezerator Treasure": "CLIMB+SLAM+SJUMP",
        "Chef Task: Ice Climber": "CLIMB+SLAM+SJUMP",
        "Chef Task: Season's Greetings": "CLIMB+SLAM+SJUMP+GRAB+STAUNT",
        "Chef Task: Frozen Nuggets": "CLIMB+SLAM+SJUMP",
        "Freezerator S Rank": "CLIMB+SLAM+SJUMP",

    #Pizzascare
        "Pizzascare Complete": "CLIMB+SLAM",
        "Pizzascare Mushroom Toppin": "CLIMB+SLAM | SJUMP+SLAM",
        "Pizzascare Cheese Toppin": "CLIMB+SLAM",
        "Pizzascare Tomato Toppin": "CLIMB+SLAM",
        "Pizzascare Sausage Toppin": "CLIMB+SLAM",
        "Pizzascare Pineapple Toppin": "CLIMB+SLAM",
        "Pizzascare Secret 1": "CLIMB+SLAM",
        "Pizzascare Secret 2": "CLIMB+SLAM",
        "Pizzascare Secret 3": "CLIMB+SLAM",
        "Pizzascare Treasure": "CLIMB+SLAM",
        "Chef Task: Haunted Playground": "CLIMB+SLAM",
        "Chef Task: Skullsplitter": "CLIMB+SLAM",
        "Chef Task: Cross To Bare": "CLIMB+SLAM",
        "Pizzascare S Rank": "CLIMB+SLAM",

    #Don't Make A Sound
        "Don't Make A Sound Complete": "CLIMB+SLAM+GRAB",
        "Don't Make A Sound Mushroom Toppin": "NONE",
        "Don't Make A Sound Cheese Toppin": "CLIMB",
        "Don't Make A Sound Tomato Toppin": "CLIMB+SLAM",
        "Don't Make A Sound Sausage Toppin": "CLIMB",
        "Don't Make A Sound Pineapple Toppin": "CLIMB+SLAM+GRAB",
        "Don't Make A Sound Secret 1": "NONE",
        "Don't Make A Sound Secret 2": "CLIMB",
        "Don't Make A Sound Secret 3": "CLIMB",
        "Don't Make A Sound Treasure": "CLIMB+SLAM+GRAB",
        "Chef Task: Let Them Sleep": "CLIMB+SLAM+GRAB",
        "Chef Task: Jumpspared": "CLIMB+SLAM+GRAB",
        "Chef Task: And This... Is My Gun On A Stick!": "CLIMB+SLAM+GRAB",
        "Don't Make A Sound S Rank": "CLIMB+SLAM+GRAB",

    #WAR
        "WAR Complete": "GRAB+SJUMP+SLAM",
        "WAR Mushroom Toppin": "GRAB+SJUMP | GRAB+CLIMB",
        "WAR Cheese Toppin": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "WAR Tomato Toppin": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "WAR Sausage Toppin": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "WAR Pineapple Toppin": "GRAB+SJUMP+SLAM",
        "WAR Secret 1": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "WAR Secret 2": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "WAR Secret 3": "GRAB+SJUMP+SLAM",
        "WAR Treasure": "GRAB+SJUMP+SLAM",
        "Chef Task: Trip to the Warzone": "GRAB+SJUMP+SLAM",
        "Chef Task: Sharpshooter": "GRAB+SJUMP+SLAM",
        "Chef Task: Decorated Veteran": "GRAB+SJUMP+SLAM",
        "WAR S Rank": "GRAB+SJUMP+SLAM",

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": "SLAM+SJUMP+CLIMB",
        "The Crumbling Tower of Pizza S Rank": "SLAM+SJUMP+CLIMB",
        "The Crumbling Tower of Pizza P Rank": "SLAM+SJUMP+CLIMB",

    #Pepperman
        "Pepperman Defeated": "GRAB",
        "Chef Task: The Critic": "GRAB",
        "Pepperman S Rank": "GRAB",
        "Pepperman P Rank": "GRAB",

    #Vigilante
        "The Vigilante Defeated": "GRAB",
        "Chef Task: The Ugly": "GRAB",
        "The Vigilante S Rank": "GRAB",
        "The Vigilante P Rank": "GRAB",

    #Noise
        "The Noise Defeated": "GRAB | UPPER",
        "Chef Task: Denoise": "GRAB | UPPER",
        "The Noise S Rank": "GRAB | UPPER",
        "The Noise P Rank": "GRAB | UPPER",

    #Fake Pep
        "Fake Peppino Defeated": "GRAB | UPPER",
        "Chef Task: Faker": "GRAB | UPPER",
        "Fake Peppino S Rank": "GRAB | UPPER",
        "Fake Peppino P Rank": "GRAB | UPPER",

    #Pizzaface
        "Pizzaface Defeated": "GRAB",
        "Chef Task: Face Off": "GRAB",

    #Tutorial
        "Tutorial Complete": "SLAM+SJUMP+GRAB",
        "Tutorial Complete in under 2 minutes": "SLAM+CLIMB+SJUMP+GRAB",
        "Tutorial Mushroom Toppin": "SLAM",
        "Tutorial Cheese Toppin": "SLAM+CLIMB",
        "Tutorial Tomato Toppin": "SLAM+CLIMB",
        "Tutorial Sausage Toppin": "SLAM+CLIMB+SJUMP",
        "Tutorial Pineapple Toppin": "SLAM+SJUMP+GRAB",

    #misc
        "Snotty Murdered": "NONE",

    #for swap mode
        "The Doise Defeated": "GRAB | UPPER",
        "Chef Task: Denoise": "GRAB | UPPER",
        "The Doise S Rank": "GRAB | UPPER",
        "The Doise P Rank": "GRAB | UPPER",

    #pumpkins
        "John Gutter Pumpkin": "SJUMP | CLIMB | UPPER",
        "Pizzascape Pumpkin": "GRAB+SJUMP | GRAB+CLIMB",
        "Ancient Cheese Pumpkin": "GRAB+SLAM+CLIMB | GRAB+SLAM+SJUMP",
        "Bloodsauce Dungeon Pumpkin": "SLAM",
        "Oregano Desert Pumpkin": "CLIMB",
        "Wasteyard Pumpkin": "SJUMP | CLIMB",
        "Fun Farm Pumpkin": "SLAM+SJUMP | SLAM+CLIMB",
        "Fastfood Saloon Pumpkin": "SJUMP+GRAB+CLIMB",
        "Crust Cove Pumpkin": "CLIMB+SLAM+SJUMP",
        "Gnome Forest Pumpkin": "SLAM+DJUMP+SPIN | SLAM+DJUMP+KICK",
        "Deep-Dish 9 Pumpkin": "SLAM+SJUMP | SLAM+CLIMB",
        "GOLF Pumpkin": "GRAB+CLIMB | GRAB+SJUMP | GRAB+UPPER",
        "The Pig City Pumpkin": "SLAM+DJUMP",
        "Peppibot Factory Pumpkin": "SJUMP+CLIMB | SJUMP+UPPER",
        "Oh Shit! Pumpkin": "SLAM+CLIMB",
        "Freezerator Pumpkin": "CLIMB+SLAM+SJUMP",
        "Pizzascare Pumpkin": "SJUMP | CLIMB",
        "Don't Make A Sound Pumpkin": "CLIMB",
        "WAR Pumpkin": "GRAB+SJUMP+SLAM | GRAB+CLIMB+SLAM",
        "The Crumbling Tower of Pizza Pumpkin": "GRAB+SLAM",
        "Tricky Treat Main Path Pumpkin 1": "NONE",
        "Tricky Treat Main Path Pumpkin 2": "NONE",
        "Tricky Treat Main Path Pumpkin 3": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Main Path Pumpkin 4": "CLIMB",
        "Tricky Treat Main Path Pumpkin 5": "CLIMB",
        "Tricky Treat Side Path Pumpkin 1": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 2": "CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 3": "UPPER | CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 4": "CLIMB | SJUMP",
        "Tricky Treat Side Path Pumpkin 5": "CLIMB",
        "Chef Task: Tricksy": "CLIMB"
    }

    pt_peppino_extra_rules = { #internal rules for rando purposes; do not correspond to real checks
	    "John Gutter Secret 1 Passed": "NONE",
        "John Gutter Secret 2 Passed": "CLIMB",
        "John Gutter Secret 3 Passed": "SJUMP | CLIMB",

        "Pizzascape Secret 1 Passed": "NONE",
        "Pizzascape Secret 2 Passed": "UPPER | GRAB",
        "Pizzascape Secret 3 Passed": "NONE",

        "Ancient Cheese Secret 1 Passed": "NONE",
        "Ancient Cheese Secret 2 Passed": "UPPER | GRAB",
        "Ancient Cheese Secret 3 Passed": "SJUMP | CLIMB",

        "Bloodsauce Dungeon Secret 1 Passed": "SJUMP | CLIMB",
        "Bloodsauce Dungeon Secret 2 Passed": "CLIMB",
        "Bloodsauce Dungeon Secret 3 Passed": "NONE",

        "Oregano Desert Secret 1 Passed": "SLAM",
        "Oregano Desert Secret 2 Passed": "NONE",
        "Oregano Desert Secret 3 Passed": "SJUMP",

        "Wasteyard Secret 1 Passed": "NONE",
        "Wasteyard Secret 2 Passed": "NONE",
        "Wasteyard Secret 3 Passed": "CLIMB | UPPER",

        "Fun Farm Secret 1 Passed": "NONE",
        "Fun Farm Secret 2 Passed": "NONE",
        "Fun Farm Secret 3 Passed": "SJUMP | CLIMB",

        "Fastfood Saloon Secret 1 Passed": "SJUMP | CLIMB",
        "Fastfood Saloon Secret 2 Passed": "CLIMB",
        "Fastfood Saloon Secret 3 Passed": "SJUMP | CLIMB",

        "Crust Cove Secret 1 Passed": "NONE",
        "Crust Cove Secret 2 Passed": "SJUMP | CLIMB",
        "Crust Cove Secret 3 Passed": "TAUNT",

        "Gnome Forest Secret 1 Passed": "DJUMP",
        "Gnome Forest Secret 2 Passed": "DJUMP",
        "Gnome Forest Secret 3 Passed": "SJUMP | CLIMB",

        "Deep-Dish 9 Secret 1 Passed": "NONE",
        "Deep-Dish 9 Secret 2 Passed": "NONE",
        "Deep-Dish 9 Secret 3 Passed": "SLAM",

        "GOLF Secret 1 Passed": "NONE",
        "GOLF Secret 2 Passed": "NONE",
        "GOLF Secret 3 Passed": "NONE",

        "The Pig City Secret 1 Passed": "SJUMP | CLIMB | UPPER",
        "The Pig City Secret 2 Passed": "DJUMP",
        "The Pig City Secret 3 Passed": "NONE",

        "Peppibot Factory Secret 1 Passed": "NONE",
        "Peppibot Factory Secret 2 Passed": "GRAB | UPPER",
        "Peppibot Factory Secret 3 Passed": "NONE",

        "Oh Shit! Secret 1 Passed": "NONE",
        "Oh Shit! Secret 2 Passed": "NONE",
        "Oh Shit! Secret 3 Passed": "NONE",

        "Freezerator Secret 1 Passed": "NONE",
        "Freezerator Secret 2 Passed": "NONE",
        "Freezerator Secret 3 Passed": "NONE",

        "Pizzascare Secret 1 Passed": "SJUMP | CLIMB",
        "Pizzascare Secret 2 Passed": "CLIMB",
        "Pizzascare Secret 3 Passed": "SJUMP | CLIMB",

        "Don't Make A Sound Secret 1 Passed": "NONE",
        "Don't Make A Sound Secret 2 Passed": "CLIMB",
        "Don't Make A Sound Secret 3 Passed": "SJUMP | CLIMB",

        "WAR Secret 1 Passed": "NONE",
        "WAR Secret 2 Passed": "SJUMP | CLIMB",
        "WAR Secret 3 Passed": "NONE",
    }

    noise_level_access_rules = {
        "John Gutter": "NONE",
        "Pizzascape": "NONE",
        "Ancient Cheese": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Bloodsauce Dungeon": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert": "NONE",
        "Wasteyard": "NONE",
        "Fun Farm": "NONE",
        "Fastfood Saloon": "NONE",
        "Crust Cove": "NONE",
        "Gnome Forest": "SJUMP | UPPER | CRUSH | BOUNCE", 
        "Deep-Dish 9": "NONE",
        "GOLF": "SJUMP | UPPER | CRUSH | BOUNCE", 
        "The Pig City": "NONE", 
        "Peppibot Factory": "NONE", 
        "Oh Shit!": "NONE", 
        "Freezerator": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Pizzascare": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Don't Make A Sound": "SJUMP | UPPER | CRUSH | BOUNCE", 
        "WAR": "SJUMP | CRUSH",
    }

    noise_boss_access_rules = {
        "Pepperman": "NONE",
        "The Vigilante": "NONE",
        "The Doise": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Fake Peppino": "SJUMP | UPPER | CRUSH | BOUNCE"
    }

    noise_next_floor_access_rules = {
        "Floor 1 Tower Lobby": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Floor 2 Western District": "NONE",
        "Floor 3 Vacation Resort": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Floor 4 Slum": "NONE"
    }

    pt_noise_rules = { #access rules within levels, which do not change
    #John Gutter
        "John Gutter Complete": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Mushroom Toppin": "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM",
        "John Gutter Cheese Toppin": "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM",
        "John Gutter Tomato Toppin": "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM",
        "John Gutter Sausage Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Pineapple Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Secret 1": "SJUMP | UPPER | CRUSH | BOUNCE | GRAB | SLAM",
        "John Gutter Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Secret 3": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Treasure": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: John Gutted": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Primate Rage": "LAP2+SJUMP | LAP2+UPPER | LAP2+CRUSH | LAP2+BOUNCE",
        "Chef Task: Let's Make This Quick": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter S Rank": "SJUMP | UPPER | CRUSH | BOUNCE",

    #Pizzascape
        "Pizzascape Complete": "GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH",
        "Pizzascape Mushroom Toppin": "NONE",
        "Pizzascape Cheese Toppin": "NONE",
        "Pizzascape Tomato Toppin": "GRAB | UPPER",
        "Pizzascape Sausage Toppin": "GRAB | UPPER",
        "Pizzascape Pineapple Toppin": "GRAB | UPPER",
        "Pizzascape Secret 1": "GRAB | UPPER",
        "Pizzascape Secret 2": "GRAB | UPPER",
        "Pizzascape Secret 3": "GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH",
        "Pizzascape Treasure": "GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH",
        "Chef Task: Shining Armor": "GRAB | UPPER",
        "Chef Task: Spoonknight": "TAUNT",
        "Chef Task: Spherical": "GRAB | UPPER",
        "Pizzascape S Rank": "GRAB+SJUMP | UPPER | GRAB+BOUNCE | GRAB+CRUSH",

    #Ancient Cheese
        "Ancient Cheese Complete": "GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH",
        "Ancient Cheese Mushroom Toppin": "NONE",
        "Ancient Cheese Cheese Toppin": "GRAB | UPPER",
        "Ancient Cheese Tomato Toppin": "GRAB+BOUNCE | GRAB+SJUMP | UPPER",
        "Ancient Cheese Sausage Toppin": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH",
        "Ancient Cheese Pineapple Toppin": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH",
        "Ancient Cheese Secret 1": "NONE",
        "Ancient Cheese Secret 2": "GRAB+BOUNCE | GRAB+SJUMP | UPPER",
        "Ancient Cheese Secret 3": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH",
        "Ancient Cheese Treasure": "GRAB+BOUNCE | GRAB+SJUMP | UPPER",
        "Chef Task: Thrill Seeker": "GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH",
        "Chef Task: Volleybomb": "GRAB+BOUNCE | GRAB+SJUMP | UPPER",
        "Chef Task: Delicacy": "NONE",
        "Ancient Cheese S Rank": "GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SJUMP+SLAM | UPPER+SJUMP+TORN | UPPER+SJUMP+CRUSH | UPPER+BOUNCE+SLAM | UPPER+BOUNCE+TORN | UPPER+BOUNCE+CRUSH",

    #Bloodsauce Dungeon
        "Bloodsauce Dungeon Complete": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Bloodsauce Dungeon Mushroom Toppin": "NONE",
        "Bloodsauce Dungeon Cheese Toppin": "NONE",
        "Bloodsauce Dungeon Tomato Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Bloodsauce Dungeon Sausage Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Bloodsauce Dungeon Pineapple Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Bloodsauce Dungeon Secret 1": "NONE",
        "Bloodsauce Dungeon Secret 2": "SJUMP+SLAM | SJUMP+BOUNCE | SJUMP+CRUSH | SJUMP+TORN",
        "Bloodsauce Dungeon Secret 3": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Bloodsauce Dungeon Treasure": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Chef Task: Eruption Man": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Chef Task: Very Very Hot Sauce": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Chef Task: Unsliced Pizzaman": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",
        "Bloodsauce Dungeon S Rank": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH | SJUMP+BOUNCE",

    #Oregano Desert
        "Oregano Desert Complete": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Mushroom Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Cheese Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Tomato Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Sausage Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Pineapple Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Secret 1": "SJUMP | BOUNCE",
        "Oregano Desert Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Secret 3": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Treasure": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Peppino's Rain Dance": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Unnecessary Violence": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Alien Cow": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert S Rank": "SJUMP | BOUNCE",

    #Wasteyard
        "Wasteyard Complete": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Mushroom Toppin": "NONE",
        "Wasteyard Cheese Toppin": "NONE",
        "Wasteyard Tomato Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Sausage Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Pineapple Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Secret 1": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Secret 3": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Treasure": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Alive and Well": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Pretend Ghost": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Ghosted": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard S Rank": "SJUMP | UPPER | CRUSH | BOUNCE",

    #Fun Farm
        "Fun Farm Complete": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",
        "Fun Farm Mushroom Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Cheese Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Tomato Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Sausage Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Pineapple Toppin": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",
        "Fun Farm Secret 1": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Secret 2": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm Secret 3": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",
        "Fun Farm Treasure": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",
        "Chef Task: Good Egg": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",
        "Chef Task: No One Is Safe": "CRUSH+STAUNT | SLAM+UPPER+STAUNT | SLAM+BOUNCE+STAUNT | SLAM+SJUMP+STAUNT",
        "Chef Task: Cube Menace": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fun Farm S Rank": "CRUSH | SLAM+UPPER | SLAM+BOUNCE | SLAM+SJUMP",

    #Fastfood Saloon
        "Fastfood Saloon Complete": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Mushroom Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Fastfood Saloon Cheese Toppin": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Tomato Toppin": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Sausage Toppin": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Pineapple Toppin": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Secret 1": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Secret 2": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon Secret 3": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
	    "Fastfood Saloon Treasure": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Chef Task: Royal Flush": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Chef Task: Non-Alcoholic": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Chef Task: Already Pressed": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Fastfood Saloon S Rank": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",

    #Crust Cove
        "Crust Cove Complete": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Crust Cove Mushroom Toppin": "CRUSH | SJUMP",
        "Crust Cove Cheese Toppin": "CRUSH | SJUMP",
        "Crust Cove Tomato Toppin": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Crust Cove Sausage Toppin": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Crust Cove Pineapple Toppin": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Crust Cove Secret 1": "CRUSH | SJUMP",
        "Crust Cove Secret 2": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Crust Cove Secret 3": "CRUSH+TAUNT | SJUMP+TORN+TAUNT | SJUMP+SLAM+TAUNT | SJUMP+BOUNCE+TAUNT",
        "Crust Cove Treasure": "CRUSH | SJUMP",
        "Chef Task: Demolition Expert": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Chef Task: Blowback": "CRUSH+TAUNT | SJUMP+TAUNT",
        "Chef Task: X": "CRUSH | SJUMP+SLAM | BOUNCE+SLAM | UPPER+SLAM",
        "Crust Cove S Rank": "CRUSH+TAUNT | SJUMP+TORN+TAUNT | SJUMP+SLAM+TAUNT | SJUMP+BOUNCE+TAUNT",

    #Gnome Forest
        "Gnome Forest Complete": "CRUSH",
        "Gnome Forest Mushroom Toppin": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Gnome Forest Cheese Toppin": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Gnome Forest Tomato Toppin": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Gnome Forest Sausage Toppin": "CRUSH",
        "Gnome Forest Pineapple Toppin": "CRUSH",
        "Gnome Forest Secret 1": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Gnome Forest Secret 2": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Gnome Forest Secret 3": "CRUSH",
        "Gnome Forest Treasure": "CRUSH",
        "Chef Task: Bee Nice": "TAUNT",
        "Chef Task: Bullseye": "TAUNT",
        "Chef Task: Lumberjack": "CRUSH",
        "Gnome Forest S Rank": "CRUSH",

    #Deep-Dish 9
        "Deep-Dish 9 Complete": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Deep-Dish 9 Mushroom Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Deep-Dish 9 Cheese Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Deep-Dish 9 Tomato Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Deep-Dish 9 Sausage Toppin": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Deep-Dish 9 Pineapple Toppin": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Deep-Dish 9 Secret 1": "SLAM | CRUSH | BOUNCE | TORN",
        "Deep-Dish 9 Secret 2": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Deep-Dish 9 Secret 3": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Deep-Dish 9 Treasure": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Chef Task: Blast 'Em Asteroids": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Chef Task: Turbo Tunnel": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Chef Task: Man Meteor": "SJUMP+SLAM | UPPER+SLAM | CRUSH+SLAM | BOUNCE+SLAM",
        "Deep-Dish 9 S Rank": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",

    #GOLF
        "GOLF Complete": "NONE",
        "GOLF Mushroom Toppin": "NONE",
        "GOLF Cheese Toppin": "NONE",
        "GOLF Tomato Toppin": "NONE",
        "GOLF Sausage Toppin": "NONE",
        "GOLF Pineapple Toppin": "NONE",
        "GOLF Secret 1": "NONE",
        "GOLF Secret 2": "NONE",
        "GOLF Secret 3": "NONE",
        "GOLF Treasure": "SJUMP | BOUNCE | CRUSH | UPPER",
        "Chef Task: Primo Golfer": "NONE",
        "Chef Task: Helpful Burger": "NONE",
        "Chef Task: Nice Shot": "NONE",
        "GOLF S Rank": "SJUMP | BOUNCE | CRUSH | UPPER",

    #The Pig City
        "The Pig City Complete": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City Mushroom Toppin": "NONE",
        "The Pig City Cheese Toppin": "SJUMP | CRUSH | UPPER | BOUNCE",
        "The Pig City Tomato Toppin": "CRUSH | SLAM",
        "The Pig City Sausage Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City Pineapple Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City Secret 1": "NONE",
        "The Pig City Secret 2": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City Secret 3": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City Treasure": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Chef Task: Say Oink!": "CRUSH+TAUNT | SLAM+SJUMP+TAUNT | SLAM+BOUNCE+TAUNT | SLAM+UPPER+TAUNT",
        "Chef Task: Pan Fried": "CRUSH | SLAM+SJUMP | SLAM+UPPER | SLAM+BOUNCE",
        "Chef Task: Strike!": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "The Pig City S Rank": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",

    #Peppibot Factory
        "Peppibot Factory Complete": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Peppibot Factory Mushroom Toppin": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Cheese Toppin": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Tomato Toppin": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Sausage Toppin": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Pineapple Toppin": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Secret 1": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Secret 2": "SJUMP | CRUSH | UPPER",
        "Peppibot Factory Secret 3": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Peppibot Factory Treasure": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Chef Task: There Can Be Only One": "LAP2+SJUMP+BOUNCE | LAP2+SJUMP+TORN | LAP2+UPPER+BOUNCE | LAP2+UPPER+TORN | LAP2+CRUSH",
        "Chef Task: Whoop This!": "SJUMP | CRUSH | UPPER",
        "Chef Task: Unflattening": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",
        "Peppibot Factory S Rank": "SJUMP+BOUNCE | SJUMP+TORN | UPPER+BOUNCE | UPPER+TORN | CRUSH",

    #Oh Shit!
        "Oh Shit! Complete": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Mushroom Toppin": "SLAM | CRUSH | BOUNCE | TORN",
        "Oh Shit! Cheese Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Tomato Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Sausage Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Pineapple Toppin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Secret 1": "SLAM | CRUSH | BOUNCE | TORN",
        "Oh Shit! Secret 2": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Secret 3": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! Treasure": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Chef Task: Food Clan": "SJUMP+SLAM+TAUNT | SJUMP+TORN+TAUNT | BOUNCE+TAUNT | CRUSH+TAUNT | UPPER+SLAM+TAUNT | UPPER+TORN+TAUNT",
        "Chef Task: Can't Fool Me": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Chef Task: Penny Pincher": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Oh Shit! S Rank": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",

    #Freezerator
        "Freezerator Complete": "NONE",
        "Freezerator Mushroom Toppin": "NONE",
        "Freezerator Cheese Toppin": "NONE",
        "Freezerator Tomato Toppin": "NONE",
        "Freezerator Sausage Toppin": "NONE",
        "Freezerator Pineapple Toppin": "NONE",
        "Freezerator Secret 1": "NONE",
        "Freezerator Secret 2": "NONE",
        "Freezerator Secret 3": "NONE",
        "Freezerator Treasure": "NONE",
        "Chef Task: Ice Climber": "NONE",
        "Chef Task: Season's Greetings": "STAUNT | GRAB",
        "Chef Task: Frozen Nuggets": "NONE",
        "Freezerator S Rank": "SLAM | CRUSH | TORN | BOUNCE",

    #Pizzascare
        "Pizzascare Complete": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Mushroom Toppin": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Cheese Toppin": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Tomato Toppin": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Sausage Toppin": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Pineapple Toppin": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Secret 1": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Secret 2": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Secret 3": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare Treasure": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Chef Task: Haunted Playground": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Chef Task: Skullsplitter": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Chef Task: Cross To Bare": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",
        "Pizzascare S Rank": "CRUSH | SJUMP+SLAM | SJUMP+TORN | UPPER+SLAM | UPPER+TORN | BOUNCE",

    #Don't Make A Sound
        "Don't Make A Sound Complete": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Don't Make A Sound Mushroom Toppin": "NONE",
        "Don't Make A Sound Cheese Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Don't Make A Sound Tomato Toppin": "CRUSH | SJUMP+TORN | SJUMP+SLAM | BOUNCE",
        "Don't Make A Sound Sausage Toppin": "SJUMP | CRUSH | UPPER | BOUNCE",
        "Don't Make A Sound Pineapple Toppin": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Don't Make A Sound Secret 1": "NONE",
        "Don't Make A Sound Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Don't Make A Sound Secret 3": "SJUMP | CRUSH | BOUNCE",
        "Don't Make A Sound Treasure": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Chef Task: Let Them Sleep": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Chef Task: Jumpspared": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Chef Task: And This... Is My Gun On A Stick!": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",
        "Don't Make A Sound S Rank": "SJUMP+GRAB | SJUMP+UPPER | CRUSH+GRAB | CRUSH+UPPER | BOUNCE+GRAB | BOUNCE+UPPER",

    #WAR
        "WAR Complete": "GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH",
        "WAR Mushroom Toppin": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Cheese Toppin": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Tomato Toppin": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Sausage Toppin": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Pineapple Toppin": "GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH",
        "WAR Secret 1": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Secret 2": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Secret 3": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "WAR Treasure": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "Chef Task: Trip to the Warzone": "GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH",
        "Chef Task: Sharpshooter": "GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH",
        "Chef Task: Decorated Veteran": "GRAB+SJUMP | UPPER+SJUMP | GRAB+SLAM | UPPER+SLAM | GRAB+CRUSH | UPPER+CRUSH",
        "WAR S Rank": "GRAB+SJUMP | UPPER+SJUMP | GRAB+CRUSH | UPPER+CRUSH",

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": "SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB",
        "The Crumbling Tower of Pizza S Rank": "SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB",
        "The Crumbling Tower of Pizza P Rank": "SJUMP+GRAB+SLAM | SJUMP+GRAB+TORN | SJUMP+GRAB+BOUNCE | CRUSH+GRAB",

    #Pepperman
        "Pepperman Defeated": "BOMB",
        "Chef Task: The Critic": "BOMB",
        "Pepperman S Rank": "BOMB",
        "Pepperman P Rank": "BOMB",

    #Vigilante
        "The Vigilante Defeated": "BOMB",
        "Chef Task: The Ugly": "BOMB",
        "The Vigilante S Rank": "BOMB",
        "The Vigilante P Rank": "BOMB",

    #Noise
        "The Doise Defeated": "NONE",
        "Chef Task: Denoise": "NONE",
        "The Doise S Rank": "NONE",
        "The Doise P Rank": "NONE",

    #Fake Pep
        "Fake Peppino Defeated": "NONE",
        "Chef Task: Faker": "NONE",
        "Fake Peppino S Rank": "NONE",
        "Fake Peppino P Rank": "NONE",

    #Pizzaface
        "Pizzaface Defeated": "BOMB",
        "Chef Task: Face Off": "BOMB",

    #Tutorial
        "Tutorial Complete": "SJUMP+SLAM | SJUMP+TORN | SJUMP+BOUNCE | CRUSH",
        "Tutorial Complete in under 2 minutes": "SJUMP+SLAM | SJUMP+TORN | SJUMP+BOUNCE | CRUSH",

    #misc
        "Snotty Murdered": "NONE",

    #pumpkins
        "John Gutter Pumpkin": "SJUMP | BOUNCE | UPPER | GRAB | CRUSH",
        "Pizzascape Pumpkin": "GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH | UPPER",
        "Ancient Cheese Pumpkin": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+TORN | GRAB+BOUNCE+CRUSH | GRAB+SJUMP+CRUSH | GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH",
        "Bloodsauce Dungeon Pumpkin": "SLAM | CRUSH | BOUNCE | TORN",
        "Oregano Desert Pumpkin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Pumpkin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Fun Farm Pumpkin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Fastfood Saloon Pumpkin": "SJUMP+GRAB | UPPER+GRAB | CRUSH+GRAB | BOUNCE+GRAB",
        "Crust Cove Pumpkin": "CRUSH | SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE",
        "Gnome Forest Pumpkin": "CRUSH | SJUMP+GRAB+SLAM | BOUNCE+GRAB+SLAM | UPPER+GRAB+SLAM",
        "Deep-Dish 9 Pumpkin": "SLAM | CRUSH | BOUNCE | TORN",
        "GOLF Pumpkin": "NONE",
        "The Pig City Pumpkin": "CRUSH | SLAM",
        "Peppibot Factory Pumpkin": "SJUMP | CRUSH | UPPER",
        "Oh Shit! Pumpkin": "SJUMP+SLAM | SJUMP+TORN | BOUNCE | CRUSH | UPPER+SLAM | UPPER+TORN",
        "Freezerator Pumpkin": "NONE",
        "Pizzascare Pumpkin": "NONE",
        "Don't Make A Sound Pumpkin": "SJUMP | CRUSH | UPPER | BOUNCE",
        "WAR Pumpkin": "GRAB+CRUSH | GRAB+SJUMP | GRAB+BOUNCE | GRAB+SLAM | UPPER+CRUSH | UPPER+SJUMP | UPPER+BOUNCE | UPPER+SLAM",
        "The Crumbling Tower of Pizza Pumpkin": "GRAB+SLAM | GRAB+TORN | GRAB+CRUSH | GRAB+BOUNCE | UPPER+SLAM | UPPER+TORN | UPPER+CRUSH | UPPER+BOUNCE",
        "Tricky Treat Main Path Pumpkin 1": "NONE",
        "Tricky Treat Main Path Pumpkin 2": "NONE",
        "Tricky Treat Main Path Pumpkin 3": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Main Path Pumpkin 4": "BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Main Path Pumpkin 5": "BOUNCE+UPPER | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 1": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 2": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 3": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 4": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 5": "BOUNCE | SJUMP | CRUSH",
        "Chef Task: Tricksy": "BOUNCE+UPPER | SJUMP | CRUSH",
    }

    pt_noise_rules_easy = { #access rules within levels, which do not change
    #John Gutter
        "John Gutter Complete": "SJUMP",
        "John Gutter Mushroom Toppin": "SJUMP | BOUNCE | CRUSH | UPPER",
        "John Gutter Cheese Toppin": "SJUMP | BOUNCE | CRUSH | UPPER",
        "John Gutter Tomato Toppin": "SJUMP | BOUNCE | CRUSH | UPPER",
        "John Gutter Sausage Toppin": "SJUMP",
        "John Gutter Pineapple Toppin": "SJUMP",
        "John Gutter Secret 1": "SJUMP | BOUNCE | CRUSH | UPPER",
        "John Gutter Secret 2": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "John Gutter Secret 3": "SJUMP",
        "John Gutter Treasure": "SJUMP",
        "Chef Task: John Gutted": "SJUMP",
        "Chef Task: Primate Rage": "LAP2+SJUMP",
        "Chef Task: Let's Make This Quick": "SJUMP+MACH4",
        "John Gutter S Rank": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",

    #Pizzascape
        "Pizzascape Complete": "GRAB+UPPER | GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH",
        "Pizzascape Mushroom Toppin": "NONE",
        "Pizzascape Cheese Toppin": "NONE",
        "Pizzascape Tomato Toppin": "GRAB",
        "Pizzascape Sausage Toppin": "GRAB",
        "Pizzascape Pineapple Toppin": "GRAB",
        "Pizzascape Secret 1": "GRAB",
        "Pizzascape Secret 2": "GRAB",
        "Pizzascape Secret 3": "GRAB+SJUMP",
        "Pizzascape Treasure": "GRAB+SJUMP",
        "Chef Task: Shining Armor": "GRAB+UPPER | GRAB+SJUMP | GRAB+BOUNCE | GRAB+CRUSH",
        "Chef Task: Spoonknight": "TAUNT",
        "Chef Task: Spherical": "GRAB",
        "Pizzascape S Rank": "GRAB+SJUMP",

    #Ancient Cheese
        "Ancient Cheese Complete": "GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH",
        "Ancient Cheese Mushroom Toppin": "NONE",
        "Ancient Cheese Cheese Toppin": "GRAB+SJUMP | GRAB+UPPER | GRAB+BOUNCE | GRAB+CRUSH",
        "Ancient Cheese Tomato Toppin": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Ancient Cheese Sausage Toppin": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Ancient Cheese Pineapple Toppin": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Ancient Cheese Secret 1": "NONE",
        "Ancient Cheese Secret 2": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Ancient Cheese Secret 3": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Ancient Cheese Treasure": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Chef Task: Thrill Seeker": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Chef Task: Volleybomb": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Chef Task: Delicacy": "NONE",
        "Ancient Cheese S Rank": "GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH",

    #Bloodsauce Dungeon
        "Bloodsauce Dungeon Complete": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Bloodsauce Dungeon Mushroom Toppin": "SJUMP | BOUNCE | UPPER | CRUSH",
        "Bloodsauce Dungeon Cheese Toppin": "NONE",
        "Bloodsauce Dungeon Tomato Toppin": "SLAM | TORN | CRUSH",
        "Bloodsauce Dungeon Sausage Toppin": "SLAM | TORN | CRUSH",
        "Bloodsauce Dungeon Pineapple Toppin": "SLAM | TORN | CRUSH",
        "Bloodsauce Dungeon Secret 1": "NONE",
        "Bloodsauce Dungeon Secret 2": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Bloodsauce Dungeon Secret 3": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Bloodsauce Dungeon Treasure": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Chef Task: Eruption Man": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Chef Task: Very Very Hot Sauce": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Chef Task: Unsliced Pizzaman": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",
        "Bloodsauce Dungeon S Rank": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP",

    #Oregano Desert
        "Oregano Desert Complete": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Mushroom Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Cheese Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Tomato Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Sausage Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Pineapple Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Secret 1": "BOUNCE",
        "Oregano Desert Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Secret 3": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert Treasure": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Peppino's Rain Dance": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Unnecessary Violence": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Alien Cow": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Oregano Desert S Rank": "BOUNCE",

    #Wasteyard
        "Wasteyard Complete": "SJUMP | UPPER | BOUNCE",
        "Wasteyard Mushroom Toppin": "NONE",
        "Wasteyard Cheese Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Tomato Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Sausage Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Pineapple Toppin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Secret 1": "SJUMP | BOUNCE",
        "Wasteyard Secret 2": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Secret 3": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Treasure": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Alive and Well": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Chef Task: Pretend Ghost": "SJUMP | UPPER | BOUNCE",
        "Chef Task: Ghosted": "SJUMP | UPPER | BOUNCE",
        "Wasteyard S Rank": "SJUMP | BOUNCE",

    #Fun Farm
        "Fun Farm Complete": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",
        "Fun Farm Mushroom Toppin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Cheese Toppin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Tomato Toppin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Sausage Toppin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Pineapple Toppin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",
        "Fun Farm Secret 1": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Secret 2": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm Secret 3": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",
        "Fun Farm Treasure": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",
        "Chef Task: Good Egg": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",
        "Chef Task: No One Is Safe": "BOUNCE+SLAM+STAUNT | UPPER+SLAM+STAUNT | SJUMP+SLAM+STAUNT | CRUSH+STAUNT",
        "Chef Task: Cube Menace": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fun Farm S Rank": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | CRUSH",

    #Fastfood Saloon
        "Fastfood Saloon Complete": "SJUMP+GRAB",
        "Fastfood Saloon Mushroom Toppin": "SJUMP",
        "Fastfood Saloon Cheese Toppin": "SJUMP+GRAB",
        "Fastfood Saloon Tomato Toppin": "SJUMP+GRAB",
        "Fastfood Saloon Sausage Toppin": "SJUMP+GRAB",
        "Fastfood Saloon Pineapple Toppin": "SJUMP+GRAB",
        "Fastfood Saloon Secret 1": "SJUMP+GRAB",
        "Fastfood Saloon Secret 2": "SJUMP+GRAB",
        "Fastfood Saloon Secret 3": "SJUMP+GRAB",
	    "Fastfood Saloon Treasure": "SJUMP+GRAB",
        "Chef Task: Royal Flush": "SJUMP+GRAB",
        "Chef Task: Non-Alcoholic": "SJUMP+GRAB",
        "Chef Task: Already Pressed": "SJUMP+GRAB",
        "Fastfood Saloon S Rank": "SJUMP+GRAB",

    #Crust Cove
        "Crust Cove Complete": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove Mushroom Toppin": "SJUMP",
        "Crust Cove Cheese Toppin": "SJUMP",
        "Crust Cove Tomato Toppin": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove Sausage Toppin": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove Pineapple Toppin": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove Secret 1": "SJUMP",
        "Crust Cove Secret 2": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove Secret 3": "SJUMP+SLAM+TAUNT | SJUMP+CRUSH+TAUNT | SJUMP+TORN+TAUNT",
        "Crust Cove Treasure": "SJUMP",
        "Chef Task: Demolition Expert": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Chef Task: Blowback": "SJUMP+TAUNT",
        "Chef Task: X": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Crust Cove S Rank": "SJUMP+SLAM+TAUNT | SJUMP+CRUSH+TAUNT | SJUMP+TORN+TAUNT",

    #Gnome Forest
        "Gnome Forest Complete": "BOUNCE+CRUSH | SJUMP+CRUSH",
        "Gnome Forest Mushroom Toppin": "CRUSH",
        "Gnome Forest Cheese Toppin": "CRUSH",
        "Gnome Forest Tomato Toppin": "BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH",
        "Gnome Forest Sausage Toppin": "BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH",
        "Gnome Forest Pineapple Toppin": "BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH",
        "Gnome Forest Secret 1": "BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH",
        "Gnome Forest Secret 2": "BOUNCE+CRUSH | SJUMP+CRUSH | UPPER+CRUSH",
        "Gnome Forest Secret 3": "BOUNCE+CRUSH | SJUMP+CRUSH",
        "Gnome Forest Treasure": "BOUNCE+CRUSH | SJUMP+CRUSH",
        "Chef Task: Bee Nice": "TAUNT",
        "Chef Task: Bullseye": "TAUNT",
        "Chef Task: Lumberjack": "BOUNCE+CRUSH | SJUMP+CRUSH",
        "Gnome Forest S Rank": "BOUNCE+CRUSH | SJUMP+CRUSH",

    #Deep-Dish 9
        "Deep-Dish 9 Complete": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Mushroom Toppin": "SLAM | CRUSH | TORN",
        "Deep-Dish 9 Cheese Toppin": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Tomato Toppin": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Sausage Toppin": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Pineapple Toppin": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Secret 1": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Secret 2": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Secret 3": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Deep-Dish 9 Treasure": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Chef Task: Blast 'Em Asteroids": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Chef Task: Turbo Tunnel": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "Chef Task: Man Meteor": "SLAM+SJUMP | SLAM+BOUNCE | SLAM+UPPER",
        "Deep-Dish 9 S Rank": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",

    #GOLF
        "GOLF Complete": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Mushroom Toppin": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Cheese Toppin": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Tomato Toppin": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Sausage Toppin": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Pineapple Toppin": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Secret 1": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Secret 2": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Secret 3": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF Treasure": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "Chef Task: Primo Golfer": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "Chef Task: Helpful Burger": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "Chef Task: Nice Shot": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",
        "GOLF S Rank": "SJUMP+GRAB | CRUSH+GRAB | UPPER+GRAB | BOUNCE+GRAB",

    #The Pig City
        "The Pig City Complete": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City Mushroom Toppin": "NONE",
        "The Pig City Cheese Toppin": "SJUMP",
        "The Pig City Tomato Toppin": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City Sausage Toppin": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+CRUSH | BOUNCE+CRUSH",
        "The Pig City Pineapple Toppin": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City Secret 1": "NONE",
        "The Pig City Secret 2": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City Secret 3": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City Treasure": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "Chef Task: Say Oink!": "SJUMP+SLAM+TAUNT | CRUSH+TAUNT | BOUNCE+SLAM+TAUNT | UPPER+SLAM+TAUNT",
        "Chef Task: Pan Fried": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "Chef Task: Strike!": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "The Pig City S Rank": "SJUMP+SLAM | SJUMP+CRUSH",

    #Peppibot Factory
        "Peppibot Factory Complete": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",
        "Peppibot Factory Mushroom Toppin": "SJUMP",
        "Peppibot Factory Cheese Toppin": "SJUMP",
        "Peppibot Factory Tomato Toppin": "SJUMP",
        "Peppibot Factory Sausage Toppin": "SJUMP",
        "Peppibot Factory Pineapple Toppin": "SJUMP",
        "Peppibot Factory Secret 1": "SJUMP",
        "Peppibot Factory Secret 2": "SJUMP",
        "Peppibot Factory Secret 3": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",
        "Peppibot Factory Treasure": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",
        "Chef Task: There Can Be Only One": "LAP2+SJUMP+SLAM | LAP2+SJUMP+TORN | LAP2+SJUMP+CRUSH",
        "Chef Task: Whoop This!": "SJUMP",
        "Chef Task: Unflattening": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",
        "Peppibot Factory S Rank": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",

    #Oh Shit!
        "Oh Shit! Complete": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Mushroom Toppin": "SLAM | TORN | CRUSH",
        "Oh Shit! Cheese Toppin": "SLAM+BOUNCE | TORN+BOUNCE | CRUSH | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER",
        "Oh Shit! Tomato Toppin": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Sausage Toppin": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Pineapple Toppin": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Secret 1": "SLAM | TORN | CRUSH",
        "Oh Shit! Secret 2": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Secret 3": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! Treasure": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Chef Task: Food Clan": "SLAM+BOUNCE+TAUNT | TORN+BOUNCE+TAUNT | CRUSH+TAUNT | SLAM+SJUMP+TAUNT | TORN+SJUMP+TAUNT | SLAM+UPPER+TAUNT | TORN+UPPER+TAUNT",
        "Chef Task: Can't Fool Me": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Chef Task: Penny Pincher": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Oh Shit! S Rank": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",

    #Freezerator
        "Freezerator Complete": "NONE",
        "Freezerator Mushroom Toppin": "NONE",
        "Freezerator Cheese Toppin": "NONE",
        "Freezerator Tomato Toppin": "NONE",
        "Freezerator Sausage Toppin": "NONE",
        "Freezerator Pineapple Toppin": "NONE",
        "Freezerator Secret 1": "NONE",
        "Freezerator Secret 2": "NONE",
        "Freezerator Secret 3": "NONE",
        "Freezerator Treasure": "NONE",
        "Chef Task: Ice Climber": "NONE",
        "Chef Task: Season's Greetings": "GRAB",
        "Chef Task: Frozen Nuggets": "NONE",
        "Freezerator S Rank": "SLAM | CRUSH | TORN | BOUNCE",

    #Pizzascare
        "Pizzascare Complete": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Mushroom Toppin": "SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM | SJUMP+TORN | BOUNCE+TORN | UPPER+TORN",
        "Pizzascare Cheese Toppin": "SJUMP+SLAM | BOUNCE+SLAM | CRUSH | UPPER+SLAM | SJUMP+TORN | BOUNCE+TORN | UPPER+TORN",
        "Pizzascare Tomato Toppin": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Sausage Toppin": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Pineapple Toppin": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Secret 1": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Secret 2": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Secret 3": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare Treasure": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Chef Task: Haunted Playground": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Chef Task: Skullsplitter": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Chef Task: Cross To Bare": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",
        "Pizzascare S Rank": "SJUMP+SLAM | BOUNCE+SLAM | SJUMP+TORN | BOUNCE+TORN | SJUMP+CRUSH | BOUNCE+CRUSH",

    #Don't Make A Sound
        "Don't Make A Sound Complete": "SJUMP+SLAM+GRAB",
        "Don't Make A Sound Mushroom Toppin": "NONE",
        "Don't Make A Sound Cheese Toppin": "SJUMP | CRUSH | BOUNCE | UPPER",
        "Don't Make A Sound Tomato Toppin": "SJUMP+SLAM | SJUMP+TORN | SJUMP+CRUSH",
        "Don't Make A Sound Sausage Toppin": "SJUMP",
        "Don't Make A Sound Pineapple Toppin": "SJUMP+SLAM+GRAB",
        "Don't Make A Sound Secret 1": "NONE",
        "Don't Make A Sound Secret 2": "SJUMP | CRUSH | BOUNCE | UPPER",
        "Don't Make A Sound Secret 3": "SJUMP",
        "Don't Make A Sound Treasure": "SJUMP+SLAM+GRAB",
        "Chef Task: Let Them Sleep": "SJUMP+SLAM+GRAB",
        "Chef Task: Jumpspared": "SJUMP+SLAM+GRAB",
        "Chef Task: And This... Is My Gun On A Stick!": "SJUMP+SLAM+GRAB",
        "Don't Make A Sound S Rank": "SJUMP+SLAM+GRAB",

    #WAR
        "WAR Complete": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Mushroom Toppin": "GRAB+BOUNCE | GRAB+SJUMP",
        "WAR Cheese Toppin": "GRAB+BOUNCE | GRAB+SJUMP",
        "WAR Tomato Toppin": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Sausage Toppin": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Pineapple Toppin": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Secret 1": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Secret 2": "GRAB+BOUNCE+SLAM | GRAB+BOUNCE+CRUSH | GRAB+BOUNCE+TORN | GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Secret 3": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR Treasure": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "Chef Task: Trip to the Warzone": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "Chef Task: Sharpshooter": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "Chef Task: Decorated Veteran": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",
        "WAR S Rank": "GRAB+SJUMP+SLAM | GRAB+SJUMP+CRUSH | GRAB+SJUMP+TORN",

    #Crumbling Tower of Pizza
        "The Crumbling Tower of Pizza Complete": "GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH",
        "The Crumbling Tower of Pizza S Rank": "GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH",
        "The Crumbling Tower of Pizza P Rank": "GRAB+SJUMP+SLAM | GRAB+SJUMP+TORN | GRAB+SJUMP+CRUSH",

    #Pepperman
        "Pepperman Defeated": "BOMB | GRAB",
        "Chef Task: The Critic": "BOMB | GRAB",
        "Pepperman S Rank": "BOMB | GRAB",
        "Pepperman P Rank": "BOMB | GRAB",

    #Vigilante
        "The Vigilante Defeated": "BOMB",
        "Chef Task: The Ugly": "BOMB",
        "The Vigilante S Rank": "BOMB",
        "The Vigilante P Rank": "BOMB",

    #Noise
        "The Doise Defeated": "BOMB | GRAB",
        "Chef Task: Denoise": "BOMB | GRAB",
        "The Doise S Rank": "BOMB | GRAB",
        "The Doise P Rank": "BOMB | GRAB",

    #Fake Pep
        "Fake Peppino Defeated": "BOMB | GRAB",
        "Chef Task: Faker": "BOMB | GRAB",
        "Fake Peppino S Rank": "BOMB | GRAB",
        "Fake Peppino P Rank": "BOMB | GRAB",

    #Pizzaface
        "Pizzaface Defeated": "BOMB",
        "Chef Task: Face Off": "BOMB",

    #Tutorial
        "Tutorial Complete": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",
        "Tutorial Complete in under 2 minutes": "SJUMP+SLAM | SJUMP+CRUSH | SJUMP+TORN",

    #misc
        "Snotty Murdered": "NONE",
    
    #pumpkins
        "John Gutter Pumpkin": "SJUMP | BOUNCE | UPPER | CRUSH",
        "Pizzascape Pumpkin": "GRAB+SJUMP | GRAB+BOUNCE | GRAB+UPPER",
        "Ancient Cheese Pumpkin": "GRAB+SJUMP+SLAM | GRAB+UPPER+SLAM | GRAB+BOUNCE+SLAM | GRAB+SJUMP+TORN | GRAB+UPPER+TORN | GRAB+BOUNCE+TORN | GRAB+SJUMP+CRUSH | GRAB+UPPER+CRUSH | GRAB+BOUNCE+CRUSH",
        "Bloodsauce Dungeon Pumpkin": "SLAM | CRUSH | BOUNCE | TORN",
        "Oregano Desert Pumpkin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Wasteyard Pumpkin": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Fun Farm Pumpkin": "BOUNCE+SLAM | UPPER+SLAM | SJUMP+SLAM | BOUNCE+TORN | UPPER+TORN | SJUMP+TORN | CRUSH",
        "Fastfood Saloon Pumpkin": "SJUMP+GRAB",
        "Crust Cove Pumpkin": "SJUMP+TORN | SJUMP+SLAM | SJUMP+BOUNCE | SJUMP+CRUSH",
        "Gnome Forest Pumpkin": "CRUSH",
        "Deep-Dish 9 Pumpkin": "SLAM+SJUMP | TORN+SJUMP | CRUSH+SJUMP | SLAM+BOUNCE | TORN+BOUNCE | CRUSH+BOUNCE | SLAM+UPPER | TORN+UPPER | CRUSH+UPPER",
        "GOLF Pumpkin": "GRAB+BOUNCE | GRAB+UPPER | GRAB+SJUMP | GRAB+CRUSH",
        "The Pig City Pumpkin": "SJUMP+SLAM | CRUSH | BOUNCE+SLAM | UPPER+SLAM",
        "Peppibot Factory Pumpkin": "SJUMP",
        "Oh Shit! Pumpkin": "SLAM+BOUNCE | TORN+BOUNCE | SLAM+SJUMP | TORN+SJUMP | SLAM+UPPER | TORN+UPPER | CRUSH+SJUMP | CRUSH+BOUNCE | CRUSH+UPPER",
        "Freezerator Pumpkin": "NONE",
        "Pizzascare Pumpkin": "NONE",
        "Don't Make A Sound Pumpkin": "SJUMP",
        "WAR Pumpkin": "GRAB+BOUNCE | GRAB+SJUMP",
        "The Crumbling Tower of Pizza Pumpkin": "GRAB+SLAM | GRAB+TORN | GRAB+CRUSH",
        "Tricky Treat Main Path Pumpkin 1": "NONE",
        "Tricky Treat Main Path Pumpkin 2": "NONE",
        "Tricky Treat Main Path Pumpkin 3": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Main Path Pumpkin 4": "BOUNCE | SJUMP",
        "Tricky Treat Main Path Pumpkin 5": "BOUNCE+UPPER | SJUMP",
        "Tricky Treat Side Path Pumpkin 1": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 2": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 3": "UPPER | BOUNCE | SJUMP | CRUSH",
        "Tricky Treat Side Path Pumpkin 4": "UPPER | BOUNCE | SJUMP",
        "Tricky Treat Side Path Pumpkin 5": "BOUNCE | SJUMP",
        "Chef Task: Tricksy": "BOUNCE+UPPER | SJUMP",
    }

    pt_noise_extra_rules = { #internal rules for rando purposes; do not correspond to real checks
	    "John Gutter Secret 1 Passed": "NONE",
        "John Gutter Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "John Gutter Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "Pizzascape Secret 1 Passed": "NONE",
        "Pizzascape Secret 2 Passed": "GRAB | UPPER",
        "Pizzascape Secret 3 Passed": "NONE",

        "Ancient Cheese Secret 1 Passed": "NONE",
        "Ancient Cheese Secret 2 Passed": "GRAB | UPPER",
        "Ancient Cheese Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "Bloodsauce Dungeon Secret 1 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Bloodsauce Dungeon Secret 2 Passed": "CRUSH | BOUNCE | UPPER",
        "Bloodsauce Dungeon Secret 3 Passed": "NONE",

        "Oregano Desert Secret 1 Passed": "SLAM | CRUSH | BOUNCE | TORN",
        "Oregano Desert Secret 2 Passed": "NONE",
        "Oregano Desert Secret 3 Passed": "CRUSH | SJUMP",

        "Wasteyard Secret 1 Passed": "NONE",
        "Wasteyard Secret 2 Passed": "NONE",
        "Wasteyard Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "Fun Farm Secret 1 Passed": "NONE",
        "Fun Farm Secret 2 Passed": "NONE",
        "Fun Farm Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "Fastfood Saloon Secret 1 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Fastfood Saloon Secret 2 Passed": "CRUSH | BOUNCE | UPPER",
        "Fastfood Saloon Secret 3 Passed": "SLAM | CRUSH | BOUNCE | TORN",

        "Crust Cove Secret 1 Passed": "NONE",
        "Crust Cove Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Crust Cove Secret 3 Passed": "TAUNT",

        "Gnome Forest Secret 1 Passed": "SJUMP | CRUSH | UPPER",
        "Gnome Forest Secret 2 Passed": "SJUMP | CRUSH | UPPER",
        "Gnome Forest Secret 3 Passed": "SJUMP | CRUSH | BOUNCE",

        "Deep-Dish 9 Secret 1 Passed": "NONE",
        "Deep-Dish 9 Secret 2 Passed": "NONE",
        "Deep-Dish 9 Secret 3 Passed": "SLAM | CRUSH",

        "GOLF Secret 1 Passed": "NONE",
        "GOLF Secret 2 Passed": "NONE",
        "GOLF Secret 3 Passed": "NONE",

        "The Pig City Secret 1 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "The Pig City Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "The Pig City Secret 3 Passed": "NONE",

        "Peppibot Factory Secret 1 Passed": "NONE",
        "Peppibot Factory Secret 2 Passed": "GRAB | UPPER",
        "Peppibot Factory Secret 3 Passed": "NONE",

        "Oh Shit! Secret 1 Passed": "NONE",
        "Oh Shit! Secret 2 Passed": "NONE",
        "Oh Shit! Secret 3 Passed": "NONE",

        "Freezerator Secret 1 Passed": "NONE",
        "Freezerator Secret 2 Passed": "NONE",
        "Freezerator Secret 3 Passed": "NONE",

        "Pizzascare Secret 1 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Pizzascare Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Pizzascare Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "Don't Make A Sound Secret 1 Passed": "NONE",
        "Don't Make A Sound Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "Don't Make A Sound Secret 3 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",

        "WAR Secret 1 Passed": "NONE",
        "WAR Secret 2 Passed": "SJUMP | UPPER | CRUSH | BOUNCE",
        "WAR Secret 3 Passed": "NONE",
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

    def interpret_rule(rule_chk: str, mode: int):
        if options.character == 0:
            if mode == 0:
                if options.difficulty == 0: rule_str = pt_peppino_rules_easy[rule_chk]
                else: rule_str = pt_peppino_rules[rule_chk]
            if mode == 1: rule_str = peppino_level_access_rules[rule_chk]
            if mode == 2: rule_str = peppino_boss_access_rules[rule_chk]
            if mode == 3: rule_str = peppino_next_floor_access_rules[rule_chk]
        elif options.character == 1:
            if mode == 0:
                if options.difficulty == 0: rule_str = pt_noise_rules_easy[rule_chk]
                else: rule_str = pt_noise_rules[rule_chk]
            if mode == 1: rule_str = noise_level_access_rules[rule_chk]
            if mode == 2: rule_str = noise_boss_access_rules[rule_chk]
            if mode == 3: rule_str = noise_next_floor_access_rules[rule_chk]
        else:
            if rule_chk in pt_swap_rules: rule_str = pt_swap_rules[rule_chk]
            else:
                if mode == 0:
                    if options.difficulty == 0: rule_str = pt_peppino_rules_easy[rule_chk] + " | " + pt_noise_rules_easy[rule_chk]
                    else: rule_str = pt_peppino_rules[rule_chk] + " | " + pt_noise_rules[rule_chk]
                if mode == 1: rule_str = peppino_level_access_rules[rule_chk] + " | " + noise_level_access_rules[rule_chk]
                if mode == 2: rule_str = peppino_boss_access_rules[rule_chk] + " | " + noise_boss_access_rules[rule_chk]
                if mode == 3: rule_str = peppino_next_floor_access_rules[rule_chk] + " | " + noise_next_floor_access_rules[rule_chk]
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
        set_rule(location, interpret_rule(lvl + " S Rank", 0))
        if options.shuffle_lap2:
            if "P Rank" in location.name or options.difficulty == 0 or not (lvl in lap1_levels):
                add_rule(location, lambda state: state.has("Lap 2 Portals", world.player))
    
    def add_s_ranked_task_rule(lvls: list, location: Location):
        for lvl in lvls:
            add_rule(location, interpret_rule(lvl + " S Rank", 0))
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
                add_rule(location, interpret_rule(lvl + " Pumpkin", 0))
            for i in range(5):
                add_rule(location, interpret_rule(f"Tricky Treat Main Path Pumpkin {i+1}", 0))
                add_rule(location, interpret_rule(f"Tricky Treat Side Path Pumpkin {i+1}", 0))
        else:
            if ("The Critic" in location.name) or ("The Ugly" in location.name) or ("Denoise" in location.name) or ("Faker" in location.name) or ("Face Off" in location.name):
                if not options.prank_checks:
                    location.progress_type = LocationProgressType.EXCLUDED
            set_rule(location, interpret_rule(location.name, 0))

    def get_toppin_prop(perc: int) -> int:
        return floor(toppins * (perc / 100))

    #access rules for floors
    for i in range(4): 
        if options.bonus_ladders < (i+1):
            set_rule(multiworld.get_entrance(floors_list[i] + " to " + floors_list[i+1], world.player), interpret_rule(floors_list[i], 3))

    #access rules for levels
    for i in range(4):
        if options.bonus_ladders < (i+1):
            for ii in range(4):
                level_name = levels_map[levels_list[(4*i)+ii]]
                set_rule(multiworld.get_entrance(floors_list[i] + " to " + level_name, world.player), interpret_rule(levels_list[(4*i)+ii], 1))
    for i in range(3):
        if options.bonus_ladders < 5:
            level_name = levels_map[levels_list[i+16]]
            set_rule(multiworld.get_entrance("Floor 5 Staff Only to " + level_name, world.player), interpret_rule(levels_list[i+16], 1))

    #access rules for bosses
    for i in range(4):
        if options.bonus_ladders < (i+1):
            set_rule(multiworld.get_entrance(floors_list[i] + " to " + bosses_map[bosses_list[i]], world.player), interpret_rule(bosses_list[i], 2))
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