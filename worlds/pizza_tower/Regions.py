from BaseClasses import Region, MultiWorld
from AutoWorld import World
from .Locations import PTLocation
from .Options import PTOptions
from . import PTChars
from typing import List, Dict, Tuple


def create_regions(world: World, multiworld: MultiWorld, player: int):
    class PTRegion(Region):
        """Region constructor pre-filled with redundant data. Only argument is region name"""
        def __init__(self, name: str):
            super().__init__(self, name, player, multiworld)

    pt_regions: Dict[str, PTRegion] = {}

    pt_rooms: List[str] = [
        # "room_name": ((connecting room name, connection name))
        #
        # connections should be named after their in-game door letter, except hub areas
        #
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
        #       ...and others for chef tasks, as needed
        # also don't forget to place "lap 2" event items at wherever lap 2 starts (usually john), not in the lap portal room itself
        # also also don't forget pumpkins cuz they don't show up on the sr wiki

        # hub world floors
        # TODO make tower_1 the starting region in init.py
        # TODO connect these to boss regions whenever
        #"tower_1": (("tower_2", None)),
        #"tower_2": (("tower_1", None), ("tower_3", None)),
        #"tower_3": (("tower_2", None), ("tower_4", None), ("tower_3 Deep Dish 9 Area", None)),
        #"tower_3 Deep Dish 9 Area": (("tower_3", None)),
        #"tower_4": (("tower_3", None), ("tower_5", None)),
        #"tower_5": (("tower_4", None), ("tower_5 WAR Area", None)), 
        #"tower_5 WAR Area": (("tower_5", None)),

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
        "entrance_lap",

        # for spoiler log clarity, name secrets as normal, not by their internal name
        # this will be done through a loop

        # pizzascape
        "medieval_1", # starting room + mushroom
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
        "medieval_10", # john + last priest required for shining armor
        # "medieval" doesnt even look like a real word anymore

        # ancient cheese
        "ruin_1", # start + locked door
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
        "dungeon_1", # start
        "dungeon_2", # mushroom
        "dungeon_3", # secret 1 + cheese
        "dungeon_4", # tomato + gerome
        "dungeon_5", # first dark room + secret 2 + first big bodyslam
        "dungeon_6", # second dark room
        "dungeon_7", # treasure
        "dungeon_8", # second big bodyslam
        "dungeon_9", # sausage + pineapple + secret 3
        "dungeon_10", # john

        # oregano desert
        "badland_1", # start
        "badland_2", # cool highjump room
        "badland_3", # entrance to mart 1 + return from escape
        "badland_mart1", # mushroom
        "badland_4", # secret 1
        "badland_5 1F", # this room is split into 3 parts. this part is the bottom floor
        "badland_5a", # first firemouth room + entrance to mart 2
        "badland_mart2", # cheese
        "badland_5 2F", # middle floor of badland_5
        "badland_5b", # hot wing skip room + gerome
        "badland_5 3F", # top floor of badland_5
        "badland_8", # secret 2
        "badland_8b", # entrance to ufo
        "badland_9", # ufo + entrance to mart 3 + john
        "badland_mart4", # actually mart 3. why are the marts numbered like this. fuck you mcpig. + tomato
        "badland_10", # may not actually be called this but it's not on the sr wiki so idk + treasure + mart 4 entrance
        "badland_mart5", # actually mart 4
        "badland_6", # funny cow escape room
        "badland_7", # entrance to mart 5
        "badland_mart3", # actually mart 5 + secret 3 + pineapple

        # wasteyard
        "graveyard_1", # start
        "graveyard_2", # mushroom + escape leads to graveyard_7
        "graveyard_3", # secret 1
        "graveyard_4", # first ghost room + cheese + secret 3 (escape-only)
        "graveyard_5", # tomato + gerome
        "graveyard_5b", # second ghost room
        "graveyard_5c", # secret 2 + sausage + escape leads to graveyard_3
        "graveyard_6", # treasure + john
        "graveyard_7", # funny hywoost room
        "graveyard_8", # pineapple
        "graveyard_9",
        "graveyard_9b", # last ghost room
        "graveyard_10", # long corpse room

        # fun farm
        "farm_2", # start. yes, farm_2 really is the start room. don't ask
        "farm_1", # treasure
        "farm_3",
        "farm_4", # escape reconnects to main path
        "farm_4b", # secret 1
        "farm_5", # highjump room
        "farm_7", # first mort room
        "farm_8", # mushroom (finally)
        "farm_cube", # mort cube
        "farm_6", # gerome + cheese
        "farm_9", # second mort room
        "farm_10", # tomato
        "farm_9b", # sausage + secret 2
        "farm_11", # john
        "farm_12", # no one is safe
        "farm_13", # pineapple + secret 3

        # fastfood saloon
        "saloon_1", # did you guys know that there are hidden points if you climb the left wall? + start
        "saloon_lap",
        "saloon_2", # mushroom
        "saloon_2b", # secret 3 (escape-only)
        "saloon_3b", # first weenie room
        "saloon_3", # treasure + cheese
        "saloon_4", # tomato
        "saloon_4b", # another weenie room
        "saloon_5b", # secret 1
        "saloon_5", # sausage + secret 2 + key
        "saloon_6b", # pineapple + locked door
        "saloon_6", # gerome + john... waow <3

        # crust cove
        "plage_entrance", # start
        "plage_lap",
        "plage_beach1", # mushroom + treasure
        "plage_shipmain", # locked door that leads to beach2 + escape route to shiptop
        "plage_ship1", # first barrel room
        "plage_ship2", # cheese + secret 1
        "plage_ship3", # key + back to shipmain
        "plage_beach2", # tomato + secret 2
        "plage_cavern1", # there's a treasure guy here but that's kinda it
        "plage_cavern2", # sausage + secret 3 + john
        "plage_cavern3", # leads back to beach2
        "plage_shiptop", # pineapple

        # gnome forest
        "forest_1", # start + secret 3 (escape-only)
        "forest_2", # bothersome lumberjack location
        "forest_lap",
        "forest_3", # treasure + pineapple (escape-only)
        "forest_G1", # switch to gustavo
        "forest_G1b", # gustavo tutorial. the latter part of G1 is considered to be part of G1b just to make things easier on me
        "forest_G2", # secret 1
        "forest_G3", # escape reconnects to main path
        "forest_5",
        "forest_6", # mushroom
        "forest_7",
        "forest_G4", 
        "forest_G5", # cheese
        "forest_8",
        "forest_9",
        "forest_10", # tomato
        "forest_12", # secret 2
        "forest_14",
        "forest_15", # meme room
        "forest_16", # gerome
        "forest_17", # sausage
        "forest_john", # john
        "forest_escape2", # no, i don't know why the escape rooms are switched like this
        "forest_escape1", # leads back to forest_G3

        # deez dish 9
        "space_1", # start + treasure + first rocket room + first bubble room
        "space_lap",
        "space_2",
        "space_3", # mushroom + secret 1
        "space_4", # cheese + leads back to space_3
        "space_5",
        "space_6", # tomato
        "space_7", # gerome + secret 2 + man meteor
        "space_8", # sausage
        "space_9", # pineapple + john
        "space_10", # turbo tunnel
        "space_11",
        "space_11b", # secret 3
        "space_12",

        # golf
        "minigolf_1", # start
        "minigolf_lap",
        "minigolf_2",
        "minigolf_3",
        "minigolf_4", # mushroom + hub area for all following pre-escape rooms
        "minigolf_5", # cheese + secret 1
        "minigolf_6", # tomato + secret 2
        "minigolf_7", # sausage + secret 3
        "minigolf_8", # gerome + pineapple + john. escape can go straight to minigolf_4 in expert logic
        "minigolf_9",
        "minigolf_10",
        "minigolf_11", # back to minigolf_8 but we can skip to minigolf_4 if we need to

        # pig city
        "street_intro", # start
        "street_1",
        "street_house1", # mushroom
        "street_2",
        "street_house2", # cheese + secret 1
        "street_3",
        "street_house3", # tomato
        "Bacon Room", # idk the internal name for this one but it has a regular name anyway
        "street_jail", # treasure + switch to gustavo
        "street_4",
        "street_house4", # sausage + secret 2
        "street_5", # strike! + last pig needed for say oink!
        "street_house5", # pineapple + gerome + secret 3
        "street_john", # john

        # peppibot factory - most of these rooms are split in halves so they'll have weird names
        "industrial_1", # start
        "industrial_lap",
        "Left side of industrial_2", # treasure (escape-only) + mushroom + secret 1
        "Left side of industrial_3", # cheese
        "Left side of industrial_4", # gerome + secret 2 + tomato
        "industrial_5", # sausage + john
        "Right side of industrial_4", # pineapple
        "Right side of industrial_3", # secret 3 + last priest required for unflattening
        "Right side of industrial_2", # last peppibot required for there can only be one (lap 2 only)

        # oh shit!
        "sewer_1", # start. sticky cheese is not actually needed to pass this room
        "sewer_2", # if pieces of a room are connected by pipes, just count them as one room
        "sewer_3", # mushroom + secret 1
        "sewer_4", # cheese
        "sewer_5", # first sticky cheese room (technically)
        "sewer_6", # gerome
        "sewer_7", # tomato + earliest place to get food clan
        "sewer_8", # secret 2 + john
        "sewer_9", # sausage
        "sewer_10", # treasure
        "sewer_11", # pineapple + secret 3
        "sewer_12", # back to sewer_2

        # rrf - noise's route looks way different so be careful
        # peppino is expected to lose satan's choice at lap 2 so we need different rules to account for that
        # ideas:
        #   - make a separate region route for lap 2
        #   - add a stupidly long list of rules (like we did before) to freezerator p rank
        #   - maybe some other archipelago feature i haven't heard of yet?
        "freezer_1", # start + mushroom
        "freezer_lap",
        "freezer_2",
        "freezer_3", # cheese + treasure
        "freezer_4",
        "freezer_5", # secret 3 (escape-only)
        "freezer_6", # tomato + secret 2
        "freezer_7", # escape leads to freezer_4
        "freezer_9", # freezer_11 is considered part of freezer_9 to make things easier
        "freezer_12",
        "freezer_13", # sausage + escape reconnects to main path
        "freezer_15", # pineapple + secret 2
        "freezer_16", # we can ignore freezer_upgrade and just assume the player has satan's choice during escape
        "freezer_17",
        "freezer_escape1", # john + back to freezer_13

        # pizzascare
        "chateau_1", # start + secret 3 (escape-only)
        "chateau_2", # pumpkin
        "chateau_2b", # treasure (escape-only)
        "chateau_3", # mushroom
        "chateau_4",
        "chateau_5", # cheese + secret 2 (escape-only) + gerome (escape-only)
        "chateau_6", # tomato
        "chateau_7", # ignore chateau_6 in escape
        "chateau_8", # sausage + secret 1
        "chateau_9", # john + i think pineapple is here? it's not on the sr wiki though

        # dmas
        "kidsparty_1", # start
        "kidsparty_floor1_1",
        "kidsparty_floor1_2", # mushroom + secret 1. ignore kidsparty_basementsecret
        "kidsparty_floor1_3",
        "kidsparty_floor2_1",
        "kidsparty_floor2_2", # cheese
        "kidsparty_floor2_3", # secret 2 + treasure (escape-only)
        "kidsparty_floor3_1",
        "kidsparty_floor3_2", # tomato
        "kidsparty_floor3_3", # secret 3
        "kidsparty_floor4_1",
        "kidsparty_floor4_2", 
        "kidsparty_floor4_3", # gerome
        "kidsparty_john", # john
        # TODO add unlisted escape rooms

        # war - no john in this level so rules are gonna be easier to write
        "war_1", # start
        "war_2", # mushroom
        "war_3", # cheese + gerome
        "war_6", # tomato
        "war_7", # secret 1
        "war_8", # sausage
        "war_9", # secret 2
        "war_10",
        "war_11",
        "war_12", # secret 3
        "war_12b", # treasure
        "war_13", # pineapple + finish
        "war_lap", # lap portal actually leads here

        # ctop - like war, this level is linear so rules are easy
        "tower_finalhallway", # ignore john. also assume player always starts at the gate
        "tower_5 (Escape)", # make sure to distinguish hub rooms from ctop rooms, since they're functionally different
        "tower_escape1", # shotgun pickup
        "tower_escape2",
        "tower_escape3",
        "tower_4 (Escape)"
        "tower_escape4",
        "tower_escape5", # weenie room
        "tower_escape6", # rocket room
        "tower_3 (Escape)",
        "tower_escape7",
        "tower_escape8",
        "tower_escape9",
        "tower_2 (Escape)",
        "tower_escape10",
        "tower_escape11",
        "tower_escape12",
        "tower_1 (Escape)",
        "tower_johngutterhall",
        "tower_entrancehall" 
    ]

    pt_connections: List[Tuple[str]] = [ # (connecting room, door letter)
        ("entrance_2", "entrance_lap"),
        ("entrance_1", "entrance_3"),
        ("entrance_2", "entrance_4"),
        ("entrance_3", "entrance_5"),
        ("entrance_4", "entrance_6"),
        ("entrance_6c", "entrance_7"),
        ("entrance_6", "entrance_8"),
        ("entrance_7", "entrance_9"),
        ("entrance_8", "entrance_10"),
        ("entrance_9"),
        ("entrance_5")
    ]

    # create regions
    for name in pt_rooms:
        pt_regions[name] = PTRegion(name)

    ########## CONNECTION STARTS HERE ##########

    # name entrances after the in-game door letter they correspond to

    # helper function for fetching regions from the dict
    def get_region(name: str):
        return pt_regions[name]

    # connect john gutter
    