from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Items import PTItem, pt_items, get_item_from_category, pt_item_groups
from .Locations import PTLocation, pt_locations, pt_location_groups
from .Options import PTOptions, pt_option_groups, pt_option_presets
from .Regions import create_regions
from .Rules import set_rules, PTChars
from math import floor
from typing import Any, TextIO
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="PTClient", args=args)


components.append(Component("Pizza Tower Client", "PTClient", func=launch_client, component_type=Type.CLIENT, icon="pizza"))

icon_paths["pizza"] = f"ap:{__name__}/pizza.png"

levels_to_floors = {
    "John Gutter": "Floor 1 Tower Lobby",
    "Pizzascape": "Floor 1 Tower Lobby",
    "Ancient Cheese": "Floor 1 Tower Lobby",
    "Bloodsauce Dungeon": "Floor 1 Tower Lobby",
    "Oregano Desert": "Floor 2 Western District",
    "Wasteyard": "Floor 2 Western District",
    "Fun Farm": "Floor 2 Western District",
    "Fastfood Saloon": "Floor 2 Western District",
    "Crust Cove": "Floor 3 Vacation Resort",
    "Gnome Forest": "Floor 3 Vacation Resort",
    "Deep-Dish 9": "Floor 3 Vacation Resort",
    "GOLF": "Floor 3 Vacation Resort",
    "The Pig City": "Floor 4 Slum",
    "Peppibot Factory": "Floor 4 Slum",
    "Oh Shit!": "Floor 4 Slum",
    "Freezerator": "Floor 4 Slum",
    "Pizzascare": "Floor 5 Staff Only",
    "Don't Make A Sound": "Floor 5 Staff Only",
    "WAR": "Floor 5 Staff Only"
}

bosses_to_floors = {
    "Pepperman": "Floor 1 Tower Lobby",
    "The Vigilante": "Floor 2 Western District",
    "The Noise": "Floor 3 Vacation Resort",
    "The Doise": "Floor 3 Vacation Resort",
    "Fake Peppino": "Floor 4 Slum"
}



def internal_from_external(name: str):
    aliases = {
        "John Gutter": "entrance",
        "Pizzascape": "medieval",
        "Ancient Cheese": "ruin",
        "Bloodsauce Dungeon": "dungeon",
        "Oregano Desert": "badland",
        "Wasteyard": "graveyard",
        "Fun Farm": "farm",
        "Fastfood Saloon": "saloon",
        "Crust Cove": "plage",
        "Gnome Forest": "forest",
        "Deep-Dish 9": "space",
        "GOLF": "minigolf",
        "The Pig City": "street",
        "Peppibot Factory": "industrial",
        "Oh Shit!": "sewer",
        "Freezerator": "freezer",
        "Pizzascare": "chateau",
        "Don't Make A Sound": "kidsparty",
        "WAR": "war",
        "Pepperman": "boss_pepperman",
        "The Vigilante": "boss_vigilante",
        "The Noise": "boss_noise",
        "The Doise": "boss_noise",
        "Fake Peppino": "boss_fakepep"
    }
    if "Secret 1" in name:
        return aliases[name.replace(" Secret 1", "")] + "1"
    if "Secret 2" in name:
        return aliases[name.replace(" Secret 2", "")] + "2"
    if "Secret 3" in name:
        return aliases[name.replace(" Secret 3", "")] + "3"
    return aliases[name]

def external_from_internal(name: str):
    aliases = {
        "entrance" : "John Gutter",
        "medieval" : "Pizzascape",
        "ruin" : "Ancient Cheese",
        "dungeon" : "Bloodsauce Dungeon",
        "badland" : "Oregano Desert",
        "graveyard" : "Wasteyard",
        "farm" : "Fun Farm",
        "saloon" : "Fastfood Saloon",
        "plage" : "Crust Cove",
        "forest" : "Gnome Forest",
        "space" : "Deep-Dish 9",
        "minigolf" : "GOLF",
        "street" : "The Pig City",
        "industrial" : "Peppibot Factory",
        "sewer" : "Oh Shit!",
        "freezer" : "Freezerator",
        "chateau" : "Pizzascare",
        "kidsparty" : "Don't Make A Sound",
        "war" : "WAR",
        "boss_pepperman" : "Pepperman",
        "boss_vigilante" : "The Vigilante",
        "boss_noise" : "The Noise",
        "boss_fakepep" : "Fake Peppino"
    }
    if "1" in name:
        return aliases[name.replace("1", "")] + " Secret 1"
    if "2" in name:
        return aliases[name.replace("2", "")] + " Secret 2"
    if "3" in name:
        return aliases[name.replace("3", "")] + " Secret 3"
    return aliases[name]

class PizzaTowerWebWorld(WebWorld):
    theme = "stone"
    option_groups = pt_option_groups
    option_presets = pt_option_presets

    setup_en = Tutorial(
        "MultiWorld Setup Guide",
        "A guide to setting up Pizza Tower for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Skizzers"]
    )

class PizzaTowerWorld(World):
    """
    Down-on-his-luck pizza chef Peppino Spaghetti and his restaurant are threatened by a sentient floating pizza... and this time
    all of his abilities are gone, too! Climb up and bring down the Pizza Tower to save your restaurant in this cheesy, saucy,
    Wario Land 4-inspired platformer!
    """
    game = "Pizza Tower"
    topology_present = True
    options_dataclass = PTOptions
    options: PTOptions
    webworld = PizzaTowerWebWorld
    apworld_version = (1, 2, 5)

    toppin_number: int = 0
    pumpkin_number: int = 0

    level_map: dict[str, str]
    boss_map: dict[str, str]
    secret_map: dict[str, str]

    item_name_to_id = {name: data.id for name, data in pt_items.items()}
    location_name_to_id = pt_locations

    item_name_groups = pt_item_groups # not extremely important for this world but it's here for completeness
    location_name_groups = pt_location_groups

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]: #UT support function that causes a re-generation
        return slot_data #we don't need to do any modification to the slot data, so just return it
    
    #Tell universal tracker we don't need a YAML
    ut_can_gen_without_yaml = True

    def generate_early(self):
        if self.options.do_move_rando and self.options.do_transfo_rando:
            if self.options.character != PTChars.PEPPINO:
                early_item_list = ["Superjump", "Wallbounce"]
            else:
                early_item_list = ["Superjump", "Wallclimb"]
            early_item_name = self.random.choice(early_item_list)
            self.multiworld.early_items[self.player][early_item_name] = 1
            if self.options.character != PTChars.PEPPINO:
                early_item_list_1 = ["Bodyslam", "Crusher"]
                early_item_name_1 = self.random.choice(early_item_list_1)
            else:
                early_item_name_1 = "Bodyslam"
            self.multiworld.early_items[self.player][early_item_name_1] = 1
        
        self.level_map = {}
        self.boss_map = {}
        self.secret_map = {}

        #Support for universal tracker
        re_gen_passthrough = getattr(self.multiworld,"re_gen_passthrough",{})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data = re_gen_passthrough[self.game]
            self.level_map = {external_from_internal(level): external_from_internal(slot_data["rando_levels"][level]) for level in slot_data["rando_levels"]}
            self.boss_map = {external_from_internal(boss): external_from_internal(slot_data["rando_bosses"][boss]) for boss in slot_data["rando_bosses"]}
            self.secret_map = {external_from_internal(sec): external_from_internal(slot_data["rando_secrets"][sec]) for sec in slot_data["rando_secrets"]}
            self.options.character = slot_data["character"]
            self.options.difficulty = slot_data["difficulty"]
            self.options.floor_1_cost = slot_data["floor_1_toppins"]
            self.options.floor_2_cost = slot_data["floor_2_toppins"]
            self.options.floor_3_cost = slot_data["floor_3_toppins"]
            self.options.floor_4_cost = slot_data["floor_4_toppins"]
            self.options.floor_5_cost = slot_data["floor_5_toppins"]
            self.options.open_world = slot_data["open_world"]
            self.options.bonus_ladders = slot_data["bonus_ladders"]
            self.options.treasure_checks = slot_data["treasure_checks"]
            self.options.srank_checks = slot_data["srank_checks"]
            self.options.prank_checks = slot_data["prank_checks"]
            self.options.cheftask_checks = slot_data["cheftask_checks"]
            self.options.secret_checks = slot_data["secret_checks"]
            self.options.shuffle_lap2 = slot_data["shuffle_lap2"]
            self.options.pumpkin_checks = slot_data["pumpkin_checks"]
            self.options.pumpkin_count = slot_data["pumpkin_count"]
            self.options.do_move_rando = slot_data["do_move_rando"]
            self.options.do_transfo_rando = slot_data["do_transfo_rando"]
            if self.options.character != PTChars.PEPPINO:
                self.boss_map = {(k if k != "The Noise" else "The Doise"):(v if v != "The Noise" else "The Doise") for k,v in self.boss_map.items()}

    def create_item(self, name: str) -> PTItem:
        return PTItem(name, pt_items[name].classification, pt_items[name].id, self.player)

    def create_regions(self):
        create_regions(self.player, self.multiworld, self.options)

    def create_items(self):
        pizza_itempool = []

        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        #add lap 2 portal
        if self.options.shuffle_lap2:
            pizza_itempool.append(self.create_item("Lap 2 Portals"))
        else:
            self.multiworld.push_precollected(self.create_item("Lap 2 Portals"))
        
        #add moves based on selected character
        total_moves = get_item_from_category("Moves Shared")
        if self.options.character != PTChars.NOISE:
            total_moves += get_item_from_category("Moves Peppino")
        if self.options.character != PTChars.PEPPINO:
            total_moves += get_item_from_category("Moves Noise")
        
        for move in total_moves:
            if self.options.do_move_rando and move in self.options.move_rando_list:
                pizza_itempool.append(self.create_item(move))
            else:
                self.multiworld.push_precollected(self.create_item(move))
        
        #add transformations, Noise doesn't use a Revolver
        transformations = get_item_from_category("Transformation")
        if self.options.character == PTChars.NOISE:
            transformations.remove("Revolver")

        for transfo in transformations:
            if self.options.do_transfo_rando and transfo in self.options.transfo_rando_list:
                pizza_itempool.append(self.create_item(transfo))
            else:
                self.multiworld.push_precollected(self.create_item(transfo))
        
        #add keys
        if not self.options.open_world:
            if self.options.shuffle_boss_keys:
                for i in range(4): pizza_itempool.append(self.create_item("Boss Key"))
            else:
                self.multiworld.get_location("Pepperman Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                self.multiworld.get_location("The Vigilante Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                if self.options.character == PTChars.PEPPINO: self.multiworld.get_location("The Noise Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                else: self.multiworld.get_location("The Doise Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                self.multiworld.get_location("Fake Peppino Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                locations_to_fill -= 4 #manually placed 4 items
        
        #add toppins, if we can
        for i in range(self.options.toppin_count):
            if locations_to_fill <= len(pizza_itempool):
                break
            pizza_itempool.append(self.create_item("Toppin"))
            self.toppin_number = i+1

        #add pumpkins, if we can
        if self.options.pumpkin_checks:
            for i in range(self.options.pumpkin_count):
                if locations_to_fill <= len(pizza_itempool):
                    break
                pizza_itempool.append(self.create_item("Pumpkin"))
                self.pumpkin_number = i+1
        
        #add clothes, if there's room
        if self.options.clothing_filler:
            total_clothes = get_item_from_category("Clothes Shared")
            if self.options.character != PTChars.NOISE:
                total_clothes += get_item_from_category("Clothes Peppino")
            if self.options.character != PTChars.PEPPINO:
                total_clothes += get_item_from_category("Clothes Noise")
            
            for clothing in total_clothes:
                if locations_to_fill <= len(pizza_itempool):
                    break
                pizza_itempool.append(self.create_item(clothing))

        #add traps
        if self.options.trap_percentage > 0:
            one_percent_trap = (locations_to_fill - len(pizza_itempool)) * (int(self.options.trap_percentage) / 100) / 100
            total_trapweights = 0
            for trapweight in self.options.trap_weights:
                total_trapweights += self.options.trap_weights[trapweight]
            if total_trapweights > 0:
                trapweight_mult = 100 / total_trapweights
                for trap in get_item_from_category("Trap"):
                    get_trapweight = trap
                    for i in range(floor(one_percent_trap * (self.options.trap_weights[get_trapweight] * trapweight_mult))):
                        pizza_itempool.append(self.create_item(trap))
            else:
                raise Exception("Traps are enabled, but all trap weights are zero")
        
        #add filler
        one_percent_filler = (locations_to_fill - len(pizza_itempool)) / 100
        total_fillerweights = 0
        for fillerweight in self.options.filler_weights:
            total_fillerweights += self.options.filler_weights[fillerweight]
        if total_fillerweights > 0:
            fillerweight_mult = 100 / total_fillerweights
            for filler in get_item_from_category("Filler"):
                for i in range(floor(one_percent_filler * (self.options.filler_weights[filler] * fillerweight_mult))):
                    pizza_itempool.append(self.create_item(filler))
        else:
            raise Exception("Please set at least one filler weight to be greater than 0")
        
        #if there's still slots left over from rounding fill them with primo burgs
        for i in range(locations_to_fill - len(pizza_itempool)):
            pizza_itempool.append(self.create_item("Primo Burg"))

        self.multiworld.itempool += pizza_itempool

    def set_rules(self):
        set_rules(self.multiworld, self, self.options, self.toppin_number, self.pumpkin_number)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("The Crumbling Tower of Pizza Complete", "Location", self.player)

    def get_filler_item_name(self) -> str:
        weighted_filler = []
        for filler in get_item_from_category("Filler"):
            for i in range(self.options.filler_weights[filler]):
                weighted_filler.append(filler)
        
        return self.random.choice(weighted_filler)
    
    def write_spoiler_header(self, spoiler_handle: TextIO):
        apversion_string = str(self.apworld_version[0]) + "." + str(self.apworld_version[1]) + "." + str(self.apworld_version[2])
        spoiler_handle.write('{:<32} {:0}'.format("APWorld Version: ", apversion_string))

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        if self.topology_present:
            ex_hint_info = dict()
            level_map_inv = {value: key for key, value in self.level_map.items()}
            boss_map_inv = {value: key for key, value in self.boss_map.items()}
            for location in self.multiworld.get_locations(self.player):
                if location.parent_region.name in levels_to_floors:
                    ex_hint_info.update({location.address: levels_to_floors[level_map_inv[location.parent_region.name]]})
                elif location.parent_region.name in bosses_to_floors:
                    ex_hint_info.update({location.address: bosses_to_floors[boss_map_inv[location.parent_region.name]]})
                elif location.parent_region.name == "The Crumbling Tower of Pizza":
                    ex_hint_info.update({location.address: "Floor 5 Staff Only"})
                elif location.parent_region.name == "Tricky Treat":
                    ex_hint_info.update({location.address: "Floor 1 Tower Lobby"})
                elif location.parent_region.name == "Pizzaface":
                    ex_hint_info.update({location.address: "Floor 5 Staff Only"})
                else:
                    ex_hint_info.update({location.address: location.parent_region.name})
            hint_data[self.player] = ex_hint_info


    def fill_slot_data(self):
        return {
            "floor_1_toppins": floor((self.toppin_number / 100) * self.options.floor_1_cost),
            "floor_2_toppins": floor((self.toppin_number / 100) * self.options.floor_2_cost),
            "floor_3_toppins": floor((self.toppin_number / 100) * self.options.floor_3_cost),
            "floor_4_toppins": floor((self.toppin_number / 100) * self.options.floor_4_cost),
            "floor_5_toppins": floor((self.toppin_number / 100) * self.options.floor_5_cost),
            "rando_levels": {internal_from_external(level): internal_from_external(self.level_map[level]) for level in self.level_map},
            "rando_bosses": {internal_from_external(boss): internal_from_external(self.boss_map[boss]) for boss in self.boss_map},
            "rando_secrets": {internal_from_external(sec): internal_from_external(self.secret_map[sec]) for sec in self.secret_map},
            "open_world": bool(self.options.open_world),
            "bonus_ladders": int(self.options.bonus_ladders),
            "character": int(self.options.character.value),
            "death_link": bool(self.options.death_link),
            "treasure_checks": bool(self.options.treasure_checks), #for poptracker
            "srank_checks": bool(self.options.srank_checks), #for poptracker
            "prank_checks": bool(self.options.prank_checks), #for poptracker
            "cheftask_checks": bool(self.options.cheftask_checks), #for poptracker
            "difficulty": bool(self.options.difficulty), #for poptracker
            "palette_filler": bool(self.options.clothing_filler),
            "secret_checks": bool(self.options.secret_checks), #for poptracker
            "shuffle_lap2": bool(self.options.shuffle_lap2),
            "pumpkin_checks": bool(self.options.pumpkin_checks), #for poptracker
            "pumpkin_count": floor(self.pumpkin_number * (self.options.tricky_treat_cost / 100)),
            "ring_link": bool(self.options.ring_link),
            "do_move_rando": bool(self.options.do_move_rando), #for poptracker
            "do_transfo_rando": bool(self.options.do_transfo_rando), #for poptracker
            "apworld_version": tuple(self.apworld_version),
            "randomize_music": bool(self.options.randomize_music)
        }