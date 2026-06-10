from BaseClasses import Region, MultiWorld
from AutoWorld import World
from .Locations import PTLocation
from .Options import PTOptions
from . import PTChars
from typing import List

def create_regions(world: World, multiworld: MultiWorld, player: int):
    class PTRegion(Region):
        """Region constructor pre-filled with redundant data. Only argument is region name"""
        def __init__(self, name: str):
            super().__init__(self, name, player, multiworld)

    pt_regions: List[str] = [ # each of these will become a region later
        # generally, and for completeness, individual rooms will be separate regions
        # we can split really big rooms into pieces if it makes sense
        # we can also ignore rooms that don't make sense to individualize like the pizzaface hall
        # use internal room names by convention, since these rooms don't have any other recognizable names
        #       (unless you really want to call half the rooms "PIZZA TOWER ISLAND" for some reason)
        # let's try using event items for level progression:
        #       "[level] Pillar John"
        #       "[level] Gerome"
        #       "[level] Key"
        #       "[level] Lap 2 Portal"

        # hub world floors
        # TODO make tower_1 the starting region in init.py
        "tower_1",
        "tower_2",
        "tower_3",
        "tower_3 Deep Dish 9 Area",
        "tower_4",
        "tower_5", 
        "tower_5 WAR Area",

        # john gutter
        "entrance_1", # starting room
        "entrance_2", # mushroom
        "entrance_3", # forknight swing room
        "entrance_4", # "how do i do this without bodyslam?"
        "entrance_5", # cheese
        "entrance_6", # secret 1
        "entrance_7", # superjump room + tomato + treasure
        "entrance_8", # sausage
        "entrance_9", # pineapple + secret 2 + gerome
        "entrance_10", # john
        "entrance_6c", # escape + secret 3
        "entrance_lap", # lap portal

        # for spoiler log clarity, name secrets as normal, not by their internal name
        # this will be done through a loop

        # pizzascape
        "medieval_1", # starting room and lap portal and mushroom
        "medieval_2", # the insta isn't THAT hard, guys
        "medieval_3", # first knight room + cheese
        "medieval_3b", # secret 3
        "medieval_4", # secret 1 + tomato
        "medieval_5", # treasure
        "medieval_6", # sausage + secret 2
        "medieval_7", # pineapple + locked door
        "medieval_8", # key
        "medieval_9", # weird ass updoor room
        "medieval_9b", # pineapple + gerome
        "medieval_10", # john
        # "medieval" doesnt even look like a real word anymore

        # ancient cheese
        "ruin_1", # start + locked door + lap portal
        "ruin_2", # mushroom + secret 1 + delicacy
        "ruin_3", # fork room
        "ruin_3b", # gerome
        "ruin_4", # key
        "ruin_5", # cheese
        "ruin_6", # tomato
        "ruin_7", # secret 2 + volleybomb
        "ruin_8", # treasure + path reconvenes from escape
        "ruin_10" # room where you run in a straight line. room order gets weird here so pay attention
        "Top of ruin_11", # room with a bunch of bomb goblins that is actually half of a larger room for some reason
        "ruin_9", # sausage
        "Bottom of ruin_11", # john + secret 3
        "ruin_12", # escape + pineapple
        "ruin_13", # escape + superjump room

        # bloodsauce dungeon
        "dungeon_1", # start + lap portal
        "dungeon_2", # mushroom
        "dungeon_3", # secret 1 + cheese
        "dungeon_4", # tomato + gerome
        "dungeon_5", # first dark room + secret 2 + first big bodyslam
        "dungeon_6", # second dark room
        "dungeon_7", # treasure
        "dungeon_8", # second big bodyslam
        "dungeon_9", # sausage + pineapple + secret 3
        "dungeon_10", # john
    ]