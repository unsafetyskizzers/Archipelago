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
        # we have to duplicate rooms accessible in both pre-escape and escape, due to generator quirks
        #       place items wherever they are first accessible
        #       for example, place john gutter secret 2 in pre-escape even though it's accessible in the escape
        # use internal room names by convention, since these rooms don't have any other recognizable names
        #       (unless you really want to call half the rooms "PIZZA TOWER ISLAND" for some reason)
        # don't forget pumpkins cuz they don't show up on the sr wiki
        # procedure for lap 2 for each level:
        #       - make a lap region (even if the level doesn't have a lap room)
        #       - give it a one-way transition into the escape start room
        #       - place a lap 2 event item at the lap region

        # hub world floors
        # TODO make tower_1 the starting region in init.py
        # TODO connect these to boss regions whenever
        "tower_1",
        "tower_2",
        "tower_3",
        "tower_3 Deep Dish 9 Area",
        "tower_4",
        "tower_5",
        "tower_5 WAR Area",

        # john gutter
        "entrance_1",
        "entrance_2",
        "entrance_3",
        "entrance_4",
        "entrance_5",
        "entrance_6",
        "entrance_7",
        "entrance_8",
        "entrance_9",
        "entrance_10", # start escape
        "entrance_9 ESC",
        "entrance_8 ESC",
        "entrance_7 ESC",
        "entrance_6 ESC",
        "entrance_6c",
        "entrance_5 ESC",
        "entrance_4 ESC",
        "entrance_3 ESC",
        "entrance_2 ESC",
        "entrance_1 ESC",
        "entrance LAP",

        # for spoiler log clarity, name secrets as normal, not by their internal name
        # this will be done through a loop

        # pizzascape
        "medieval_1",
        "medieval_2",
        "medieval_3",
        "medieval_3b",
        "medieval_4",
        "medieval_5",
        "medieval_6",
        "medieval_7",
        "medieval_8",
        "medieval_9",
        "medieval_9b",
        "medieval_10", # start escape
        "medieval_9b ESC",
        "medieval_9 ESC",
        "medieval_8 ESC",
        "medieval_7 ESC",
        "medieval_6 ESC",
        "medieval_5 ESC",
        "medieval_4 ESC",
        "medieval_3b ESC",
        "medieval_2 ESC",
        "medieval_1 ESC",
        "medieval LAP",
        # "medieval" doesnt even look like a real word anymore

        # ancient cheese
        "ruin_1",
        "ruin_2",
        "ruin_3",
        "ruin_3b",
        "ruin_4",
        "ruin_5",
        "ruin_6",
        "ruin_7",
        "ruin_8",
        "ruin_10", # room where you run in a straight line. room order gets weird here so pay attention
        "Top of ruin_11",
        "ruin_9",
        "Bottom of ruin_11", # start escape
        "ruin_12",
        "ruin_13",
        "ruin_8 ESC",
        "ruin_7 ESC",
        "ruin_6 ESC",
        "ruin_5 ESC",
        "ruin_1 ESC",
        "ruin LAP",

        # bloodsauce dungeon
        "dungeon_1",
        "dungeon_2",
        "dungeon_3",
        "dungeon_4",
        "dungeon_5",
        "dungeon_6",
        "dungeon_7",
        "dungeon_8",
        "dungeon_9",
        "dungeon_10", # start escape
        "dungeon_9 ESC",
        "dungeon_8 ESC",
        "dungeon_7 ESC",
        "dungeon_6 ESC",
        "dungeon_5 ESC",
        "dungeon_4 ESC",
        "dungeon_3 ESC",
        "dungeon_2 ESC",
        "dungeon_1 ESC",
        "dungeon LAP",

        # oregano desert
        "badland_1",
        "badland_2",
        "badland_3",
        "badland_4",
        "badland_5 1F",
        "badland_5a",
        "badland_5 2F",
        "badland_5b",
        "badland_5 3F",
        "badland_8",
        "badland_8b",
        "badland_9", # start escape
        "badland_10",
        "badland_6",
        "badland_7",
        "badland_3 ESC",
        "badland_2 ESC",
        "badland_1 ESC",
        "badland LAP",

        # wasteyard
        "graveyard_1",
        "graveyard_2",
        "graveyard_3",
        "graveyard_4",
        "graveyard_5",
        "graveyard_5b",
        "graveyard_5c",
        "graveyard_6", # start escape
        "graveyard_5c ESC",
        "graveyard_3 ESC",
        "graveyard_2 ESC",
        "graveyard_7",
        "graveyard_8",
        "graveyard_9",
        "graveyard_9b",
        "graveyard_10",
        "graveyard_1 ESC",
        "graveyard LAP",

        # fun farm
        "farm_2",
        "farm_1",
        "farm_3",
        "farm_4",
        "farm_4b",
        "farm_5",
        "farm_7",
        "farm_8",
        "farm_6",
        "farm_9",
        "farm_10",
        "farm_9b",
        "farm_11", # start escape
        "farm_12",
        "farm_12b",
        "farm_13",
        "farm_4 ESC",
        "farm_1 ESC",
        "farm_2 ESC",
        "farm LAP",

        # fastfood saloon
        "saloon_1",
        "saloon_2",
        "saloon_2b",
        "saloon_3b",
        "saloon_3",
        "saloon_4",
        "saloon_4b",
        "saloon_5b",
        "saloon_5",
        "saloon_6b",
        "saloon_6", # start escape
        "saloon_5 ESC",
        "saloon_4 ESC",
        "saloon_3 ESC",
        "saloon_2 ESC",
        "saloon_1 ESC",
        "saloon LAP",

        # crust cove
        "plage_entrance",
        "plage_lap",
        "plage_beach1",
        "plage_shipmain",
        "plage_ship1",
        "plage_ship2",
        "plage_ship3",
        "plage_beach2",
        "plage_cavern1",
        "plage_cavern2", # start escape
        "plage_cavern3",
        "plage_beach2 ESC",
        "plage_shipmain ESC",
        "plage_shiptop",
        "plage_beach1 ESC",
        "plage_entrance ESC",
        "plage LAP",

        # gnome forest
        "forest_1",
        "forest_2",
        "forest_3",
        "forest_G1",
        "forest_G1b",
        "forest_G2",
        "forest_G3",
        "forest_5",
        "forest_6",
        "forest_7",
        "forest_G4", 
        "forest_G5",
        "forest_8",
        "forest_9",
        "forest_10",
        "forest_12",
        "forest_14",
        "forest_15",
        "forest_16",
        "forest_17",
        "forest_john", # start escape
        "forest_escape2",
        "forest_G5 ESC",
        "forest_escape1",
        "forest_G3 ESC",
        "forest_G2 ESC",
        "forest_G1 ESC",
        "forest_3 ESC",
        "forest_2 ESC",
        "forest_1 ESC",
        "forest LAP",

        # deez dish 9
        "space_1",
        "space_2",
        "space_3",
        "space_4",
        "space_5",
        "space_6",
        "space_7",
        "space_8",
        "space_9", # start escape
        "space_10",
        "space_11",
        "space_11b",
        "space_12",
        "space_1 ESC",
        "space LAP",

        # golf
        "minigolf_1",
        "minigolf_2",
        "minigolf_3",
        "minigolf_4",
        "minigolf_5",
        "minigolf_6",
        "minigolf_7",
        "minigolf_8", # start escape; if expert logic and conditions are met, link directly to "minigolf_4 ESC"
        "minigolf_9",
        "minigolf_10",
        "minigolf_11", # minigolf_8 ESC is included here
        "minigolf_4 ESC",
        "minigolf_3 ESC",
        "minigolf_2 ESC",
        "minigolf_1 ESC",
        "minigolf LAP",

        # pig city
        "street_intro",
        "street_1",
        "street_house1",
        "street_2",
        "street_house2",
        "street_3",
        "street_house3",
        "street_bacon",
        "street_jail",
        "street_4",
        "street_house4",
        "street_5",
        "street_house5",
        "street_john", # start escape
        "street_5 ESC",
        "street_4 ESC",
        "street_jail ESC",
        "street_3 ESC",
        "street_2 ESC",
        "street_1 ESC",
        "street_intro ESC",
        "street LAP",

        # peppibot factory - most of these rooms are split in halves so they'll have weird names
        "industrial_1",
        "Left side of industrial_2",
        "Left side of industrial_3",
        "Left side of industrial_4",
        "industrial_5", # start escape
        "Right side of industrial_4",
        "Right side of industrial_3",
        "Right side of industrial_2",
        "industrial_1 ESC",
        "industrial LAP",

        # oh shit!
        "sewer_1",
        "sewer_2",
        "sewer_3",
        "sewer_4",
        "sewer_5",
        "sewer_6",
        "sewer_7",
        "sewer_8", # start escape
        "sewer_9",
        "sewer_10",
        "sewer_11",
        "sewer_12",
        "sewer_2 ESC",
        "sewer_1 ESC",
        "sewer LAP",

        # rrf - noise's route looks way different so be careful
        # peppino is expected to lose satan's choice at lap 2 so we need different rules to account for that
        # we can achieve this by placing level complete, treasure, and secret 3 at pillar john and treating
        #       the normal escape route as lap 2 only
        "freezer_1",
        "freezer_2",
        "freezer_3",
        "freezer_4",
        "freezer_5",
        "freezer_6",
        "freezer_6 Unfrozen",
        "freezer_7",
        "freezer_9",
        "freezer_9 Unfrozen"
        "freezer_12",
        "freezer_13",
        "freezer_15",
        "freezer_16",
        "freezer_16 Unfrozen"
        "freezer_17",
        "freezer_escape1", # start escape; place level completion here since peppino should have satan's by now
        "freezer_13 ESC", # this room and below should be lap 2 only
        "freezer_12 ESC",
        "freezer_9 ESC",
        "freezer_7 ESC",
        "freezer_4 ESC",
        "freezer_3 ESC",
        "freezer_2 ESC",
        "freezer_1 ESC",

        # pizzascare
        "chateau_1",
        "chateau_2",
        "chateau_3",
        "chateau_4",
        "chateau_5",
        "chateau_6",
        "chateau_7",
        "chateau_8",
        "chateau_9", # start escape
        "chateau_8 ESC",
        "chateau_7 ESC", # also includes chateau_6 ESC
        "chateau_5 ESC",
        "chateau_2 ESC",
        "chateau_2b",
        "chateau_1 ESC",
        "chateau LAP",

        # dmas
        "kidsparty_1",
        "kidsparty_floor1_1",
        "kidsparty_floor1_2",
        "kidsparty_floor1_3",
        "kidsparty_floor2_1",
        "kidsparty_floor2_2",
        "kidsparty_floor2_3",
        "kidsparty_floor3_1",
        "kidsparty_floor3_2",
        "kidsparty_floor3_3",
        "kidsparty_floor4_1",
        "kidsparty_floor4_2", 
        "kidsparty_floor4_3",
        "kidsparty_john", # start escape
        "kidsparty_floor4_3 ESC",
        "kidsparty_escape1",
        "kidsparty_floor2_3 ESC",
        "kidsparty_escape2",
        "kidsparty_floor1_3 ESC",
        "kidsparty_floor1_2 ESC",
        "kidsparty_floor1_1 ESC",
        "kidsparty_1 ESC",
        "kidsparty LAP",

        # war - no john in this level so rules are gonna be easier to write
        "war_1",
        "war_2",
        "war_3",
        "war_6",
        "war_7",
        "war_8",
        "war_9",
        "war_10",
        "war_11",
        "war_12",
        "war_12b",
        "war_13",
        "war LAP",

        # ctop - like war, this level is linear so rules are easy
        "tower_finalhallway",
        "tower_5 ESC",
        "tower_escape1",
        "tower_escape2",
        "tower_escape3",
        "tower_4 ESC"
        "tower_escape4",
        "tower_escape5",
        "tower_escape6",
        "tower_3 ESC",
        "tower_escape7",
        "tower_escape8",
        "tower_escape9",
        "tower_2 ESC",
        "tower_escape10",
        "tower_escape11",
        "tower_escape12",
        "tower_1 ESC",
        "tower_johngutterhall",
        "tower_entrancehall",

        "pepperman",
        "vigilante",
        "noise",
        "fakepeppino",
        "pizzaface",

        "trickytreat_1",
        "trickytreat_2",
        "trickytreat_2b",
        "trickytreat_3",
        "trickytreat_3b",
        "trickytreat_4",
        "trickytreat_4b",
        "trickytreat_5",
        "trickytreat_6",
        "trickytreat_6b",
        "trickytreat_7",
    ]

    # this is serious now!
    class PTLevel():
        name: str
        start_region: str
        end_region: str
        lap_region: str
        lap2_end_region: str | None
        toppins: Tuple[str]
        secrets: Tuple[str]
        gerome: str
        treasure: str
        pumpkin: str
        cheftasks: Dict[str, str]

        def __init__(self, start_region: str, end_region: str, lap_region: str, toppins: Tuple[str], secrets: Tuple[str], gerome: str, treasure: str, pumpkin: str, cheftasks: Dict[str, str], lap2_end_region: str | None = None) -> PTLevel:
            self.start_region = start_region
            self.end_region = end_region
            self.lap_region = lap_region
            self.toppins = toppins
            self.secrets = secrets
            self.gerome = gerome
            self.treasure = treasure
            self.pumpkin = pumpkin
            self.cheftasks = cheftasks
            self.lap2_end_region = lap2_end_region

        def set_name(self, name: str) -> None:
            self.name = name

        def get_name(self) -> str:
            return self.name

        def set_toppins(self, mushroom: str, cheese: str, tomato: str, sausage: str, pineapple: str) -> None:
            self.toppins = (
                mushroom,
                cheese,
                tomato,
                sausage,
                pineapple
            )

        def get_toppins(self) -> Tuple[str]:
            return self.toppins
        
        def set_secrets(self, secret1: str, secret2: str, secret3: str) -> None:
            self.secrets = (
                secret1,
                secret2,
                secret3
            )

        def get_secrets(self) -> Tuple[str]:
            return self.secrets
        
        def set_gerome(self, gerome: str) -> None:
            self.gerome = gerome

        def get_gerome(self) -> str:
            return self.gerome
        
        def set_treasure(self, treasure: str) -> None:
            self.treasure = treasure

        def get_treasure(self) -> str:
            return self.treasure
        
        def set_pumpkin(self, pumpkin: str) -> None:
            self.pumpkin = pumpkin

        def get_pumpkin(self) -> str:
            return self.pumpkin
        
        def set_cheftasks(self, cheftasks: Dict[str, str]) -> None:
            self.cheftasks = cheftasks

        def set_cheftask(self, cheftask: str, location: str) -> None:
            self.cheftasks[cheftask] = location

        def get_cheftasks(self) -> List[str]:
            return self.cheftasks.keys()

        def get_cheftask_location(self, cheftask: str) -> str:
            return self.cheftasks[cheftask]

    # initialize levels
    levels: Dict[str, PTLevel] = {
        "John Gutter": PTLevel(
            start_region="entrance_1",
            end_region="entrance_1 ESC",
            lap_region="entrance LAP",
            toppins=(
                "entrance_2",
                "entrance_5",
                "entrance_6",
                "entrance_8",
                "entrance_9"
            ),
            secrets=(
                "entrance_5",
                "entrance_9",
                "entrance_6c"
            ),
            gerome="entrance_9",
            treasure="entrance_7 ESC",
            pumpkin="entrance_7",
            cheftasks={
                "John Gutted": "entrance_6c",
                "Let's Make This Quick": "entrance_1 ESC",
                "Primate Rage": "entrance_1 ESC"
            }
        ),
        "Pizzascape": PTLevel(
            start_region="medieval_1",
            end_region="medieval_1 ESC",
            lap_region="medieval LAP",
            toppins=(
                "medieval_1",
                "medieval_3",
                "medieval_4",
                "medieval_6",
                "medieval_7"
            ),
            secrets=(
                "medieval_4",
                "medieval_6",
                "medieval_3b ESC"
            ),
            gerome="medieval_9b",
            treasure="medieval_5 ESC",
            pumpkin="medieval_5",
            cheftasks={
                "Spoonknight": "medieval_6",
                "Spherical": "medieval_3b",
                "Shining Armor": "medieval_10"
            }
        ),
        "Ancient Cheese": PTLevel(
            start_region="ruin_1",
            end_region="ruin_1 ESC",
            lap_region="ruin LAP",
            toppins=(
                "ruin_2",
                "ruin_5",
                "ruin_6",
                "ruin_9",
                "ruin_12"
            ),
            secrets=(
                "ruin_2",
                "ruin_7",
                "Bottom of ruin_11"
            ),
            gerome="ruin_3",
            treasure="ruin_8",
            pumpkin="ruin_12",
            cheftasks={
                "Delicacy": "ruin_2",
                "Volleybomb": "ruin_7",
                "Thrill Seeker": "ruin_1 ESC"
            }
        ),
        "Bloodsauce Dungeon": PTLevel(
            start_region="dungeon_1",
            end_region="dungeon_1 ESC",
            lap_region="dungeon LAP",
            toppins=(
                "dungeon_2",
                "dungeon_3",
                "dungeon_4",
                "dungeon_9",
                "dungeon_9"
            ),
            secrets=(
                "dungeon_3",
                "dungeon_5",
                "dungeon_9"
            ),
            gerome="dungeon_4",
            treasure="dungeon_7",
            pumpkin="dungeon_9",
            cheftasks={
                "Eruption Man": "dungeon_9 ESC",
                "Very Very Hot Sauce": "dungeon_1 ESC",
                "Unsliced Pizzaman": "dungeon_1 ESC"
            }
        ),
        "Oregano Desert": PTLevel(
            start_region="badland_1",
            end_region="badland_1 ESC",
            lap_region="badland LAP",
            toppins=(
                "badland_3",
                "badland_5a",
                "badland_9",
                "badland_10",
                "badland_7"
            ),
            secrets=(
                "badland_4",
                "badland_8",
                "badland_7"
            ),
            gerome="badland_5b",
            treasure="badland_10",
            pumpkin="badland_7",
            cheftasks={
                "Peppino's Rain Dance": "badland_2",
                "Unnecessary Violence": "badland_7",
                "Alien Cow": "badland_1 ESC"
            }
        ),
        "Wasteyard": PTLevel(
            start_region="graveyard_1",
            end_region="graveyard_1 ESC",
            lap_region="graveyard LAP",
            toppins=(
                "graveyard_2",
                "graveyard_4",
                "graveyard_5",
                "graveyard_5c",
                "graveyard_8"
            ),
            secrets=(
                "graveyard_3",
                "graveyard_5c",
                "graveyard_3 ESC"
            ),
            gerome="graveyard_5",
            treasure="graveyard_6",
            pumpkin="graveyard_5c",
            cheftasks={
                "Alive and Well": "graveyard_10",
                "Pretend Ghost": "graveyard_9b",
                "Ghosted": "graveyard_1 ESC"
            }
        ),
        "Fun Farm": PTLevel(
            start_region="farm_2",
            end_region="farm_2 ESC",
            lap_region="farm LAP",
            toppins=(
                "farm_8",
                "farm_6",
                "farm_10",
                "farm_9b",
                "farm_13"
            ),
            secrets=(
                "farm_4b",
                "farm_9b",
                "farm_13"
            ),
            gerome="farm_6",
            treasure="farm_1 ESC",
            pumpkin="farm_12",
            cheftasks={
                "Good Egg": "farm_2 ESC",
                "Cube Menace": "farm_8",
                "No One Is Safe": "farm_12"
            }
        ),
        "Fastfood Saloon": PTLevel(
            start_region="saloon_1",
            end_region="saloon_1 ESC",
            lap_region="saloon LAP",
            toppins=(
                "saloon_2",
                "saloon_3",
                "saloon_4",
                "saloon_5",
                "saloon_6b"
            ),
            secrets=(
                "saloon_5b",
                "saloon_5",
                "saloon_2 ESC"
            ),
            gerome="saloon_6",
            treasure="saloon_3 ESC",
            pumpkin="saloon_4",
            cheftasks={
                "Royal Flush": "saloon_1 ESC",
                "Non-Alcoholic": "saloon_1 ESC",
                "Already Pressed": "saloon_1 ESC"
            }
        ),
        "Crust Cove": PTLevel(
            start_region="plage_entrance",
            end_region="plage_entrance ESC",
            lap_region="plage LAP",
            toppins=(
                "plage_beach1",
                "plage_ship2",
                "plage_beach2",
                "plage_cavern2",
                "plage_shiptop"
            ),
            secrets=(
                "plage_ship2",
                "plage_beach2",
                "plage_cavern2"
            ),
            gerome="plage_shipmain",
            treasure="plage_beach1",
            pumpkin="plage_cavern1",
            cheftasks={
                # X will be placed depending on difficulty
                "Blowback": "plage_shipmain",
                "Demolition Expert": "plage_entrance ESC"
            }
        ),
        "Gnome Forest": PTLevel(
            start_region="forest_1",
            end_region="forest_1 ESC",
            lap_region="forest LAP",
            toppins=( # keeping track of gnome pizzas is unnecessary since they're all on the main path
                "forest_6",
                "forest_G5",
                "forest_10",
                "forest_17",
                "forest_3 ESC"
            ),
            secrets=(
                "forest_G2",
                "forest_12",
                "forest_1 ESC"
            ),
            gerome="forest_16",
            treasure="forest_3 ESC",
            pumpkin="forest_7",
            cheftasks={
                "Bee Nice": "forest_1",
                "Bullseye": "forest_2",
                "Lumberjack": "forest_2 ESC"
            }
        ),
        "Deep Dish 9": PTLevel(
            start_region="space_1", # the one place that hasn't been touched by capitalism
            end_region="space_1 ESC",
            lap_region="space LAP",
            toppins=(
                "space_3",
                "space_4",
                "space_6", # oh fuck is that a space pizzamart??? damn nevermind then
                "space_8",
                "space_9"
            ),
            secrets=(
                "space_3",
                "space_7",
                "space_11b"
            ),
            gerome="space_7",
            treasure="space_1 ESC",
            pumpkin="space_5",
            cheftasks={
                "Man Meteor": "space_7",
                "Turbo Tunnel": "space_10",
                "Blast 'Em Asteroids": "space_11b"
            }
        ),
        "GOLF": PTLevel(
            start_region="minigolf_1",
            end_region="minigolf_1 ESC",
            lap_region="minigolf LAP",
            toppins=(
                "minigolf_4",
                "minigolf_5",
                "minigolf_6",
                "minigolf_7",
                "minigolf_8"
            ),
            secrets=(
                "minigolf_5",
                "minigolf_6",
                "minigolf_7"
            ),
            gerome="minigolf_8",
            treasure="minigolf_4 ESC",
            pumpkin="minigolf_6",
            cheftasks={
                "Helpful Burger": "minigolf_6",
                "Nice Shot": "minigolf_8",
                "Primo Golfer": "minigolf_11"
            }
        ),
        "The Pig City": PTLevel(
            start_region="street_intro",
            end_region="street_intro ESC",
            lap_region="street LAP",
            toppins=(
                "street_house1",
                "street_house2",
                "street_house3",
                "street_house4",
                "street_house5"
            ),
            secrets=(
                "street_house2",
                "street_house4",
                "street_house5"
            ),
            gerome="street_house5",
            treasure="street_jail ESC",
            pumpkin="street_4",
            cheftasks={
                "Say Oink!": "street_5",
                "Strike!": "street_5",
                "Pan Fried": "street_3"
            }
        ),
        "Peppibot Factory": PTLevel(
            start_region="industrial_1",
            end_region="industrial_1 ESC",
            lap_region="industrial LAP",
            toppins=(
                "Left side of industrial_2",
                "Left side of industrial_3",
                "Left side of industrial_4",
                "industrial_5",
                "Right side of industrial_4"
            ),
            secrets=(
                "Left side of industrial_2",
                "Left side of industrial_4",
                "Right side of industrial_3"
            ),
            gerome="Left side of industrial_4",
            treasure="industrial_1 ESC",
            pumpkin="industrial_5",
            cheftasks={
                # Whoop This! goes wherever peppibot secret 1 ends up
                "There Can Be Only One": "industrial_1 ESC",
                "Unflattening": "Right side of industrial_3"
            }
        ),
        "Oh Shit!": PTLevel(
            start_region="sewer_1",
            end_region="sewer_1 ESC",
            lap_region="sewer LAP",
            toppins=(
                "sewer_3",
                "sewer_4",
                "sewer_7",
                "sewer_9",
                "sewer_11"
            ),
            secrets=(
                "sewer_3",
                "sewer_8",
                "sewer_11"
            ),
            gerome="sewer_6",
            treasure="sewer_10",
            pumpkin="sewer_8",
            cheftasks={
                "Food Clan": "sewer_7",
                "Can't Fool Me": "sewer_1 ESC",
                "Penny Pincher": "sewer_1 ESC"
            }
        ),
        "Freezerator": PTLevel( # satan's choice opens everything up so the escape regions are reserved for lap 2
            start_region="freezer_1",
            end_region="freezer_escape1",
            lap_region="freezer_13 ESC",
            toppins=(
                "freezer_1",
                "freezer_3",
                "freezer_6 Unfrozen",
                "freezer_13",
                "freezer_15"
            ),
            secrets=(
                "freezer_6 Unfrozen",
                "freezer_15",
                "freezer_escape1"
            ),
            gerome="freezer_escape1",
            treasure="freezer_escape1",
            pumpkin="freezer_6 Unfrozen",
            cheftasks={
                # place two of Season's Greetings:
                # one at freezer_escape1 that requires staunt (meaning it can be done in lap 1),
                # and one at freezer_1 ESC that requires grab (meaning it must be done in lap 2)
                "Frozen Nuggets": "freezer_escape1",
                "Ice Climber": "freezer_escape1"
            }
        ),
        "Pizzascare": PTLevel(
            start_region="chateau_1",
            end_region="chateau_1 ESC",
            lap_region="chateau LAP",
            toppins=(
                "chateau_3",
                "chateau_5",
                "chateau_6",
                "chateau_8",
                "chateau_7 ESC"
            ),
            secrets=(
                "chateau_8",
                "chateau_5 ESC",
                "chateau_1 ESC"
            ),
            gerome="chateau_5 ESC",
            treasure="chateau_2 ESC",
            pumpkin="chateau_2",
            cheftasks={
                "Haunted Playground": "chateau_1 ESC",
                "Skullsplitter": "chateau_7 ESC",
                "Cross To Bare": "chateau_2 ESC"
            }
        ),
        "Don't Make A Sound": PTLevel(
            start_region="kidsparty_1",
            end_region="kidsparty_1 ESC",
            lap_region="kidsparty LAP",
            toppins=(
                "kidsparty_floor1_2",
                "kidsparty_floor2_2",
                "kidsparty_floor3_2",
                "kidsparty_floor4_2",
                "kidsparty_escape1"
            ),
            secrets=(
                "kidsparty_floor1_2",
                "kidsparty_floor2_3",
                "kidsparty_floor3_3"
            ),
            gerome="kidsparty_floor4_3",
            treasure="kidsparty_floor2_3 ESC",
            pumpkin="kidsparty_floor4_2",
            cheftasks={
                "Let Them Sleep": "kidsparty_john",
                "And This... Is My Gun On A Stick!": "kidsparty_floor1_2 ESC",
                "Jumpspared": "kidsparty_1 ESC"
            }
        ),
        "WAR": PTLevel(
            start_region="war_1",
            end_region="war_13",
            lap_region="war LAP",
            toppins=(
                "war_2",
                "war_3",
                "war_6",
                "war_8",
                "war_13"
            ),
            secrets=(
                "war_7",
                "war_9",
                "war_12"
            ),
            gerome="war_2",
            treasure="war_12b",
            pumpkin="war_2",
            cheftasks={
                "Trip to the Warzone": "war_13",
                "Sharpshooter": "war_13",
                "Decorated Veteran": "war_13"
            }
        ),
        "The Crumbling Tower of Pizza": PTLevel(
            start_region="tower_finalhallway",
            end_region="tower_entrancehall ESC",
            lap_region=None,
            toppins=None,
            secrets=None,
            gerome=None,
            treasure=None,
            pumpkin="tower_escape4",
            cheftasks=None
        ),
    }

    # create regions
    for name in pt_rooms:
        pt_regions[name] = PTRegion(name)

    ########## CONNECTION STARTS HERE ##########

    # name entrances after the in-game door letter they correspond to

    # helper function for fetching regions from the dict
    def get_region(name: str):
        return pt_regions[name]

    # connect john gutter
    