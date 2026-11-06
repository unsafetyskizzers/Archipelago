from enum import IntEnum
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, LocationProgressType
from .Items import PTItem, pt_items, get_item_from_category, pt_item_groups
from .Locations import pt_locations, pt_location_groups
from math import floor
from typing import Any, TextIO, NamedTuple
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from Options import OptionError
from logging import info

class PTChars(IntEnum):
    PEPPINO = 0
    NOISE = 1
    SWAP = 2

class PTLevelData(NamedTuple):
    internal_name: str
    floor: str
    is_boss: bool = False

level_data: dict[str, PTLevelData] = {
    "Tutorial":             PTLevelData("tutorial", "Floor 1 Tower Lobby"),
    "John Gutter":          PTLevelData("entrance", "Floor 1 Tower Lobby"),
    "Pizzascape":           PTLevelData("medieval", "Floor 1 Tower Lobby"),
    "Ancient Cheese":       PTLevelData("ruin", "Floor 1 Tower Lobby"),
    "Bloodsauce Dungeon":   PTLevelData("dungeon", "Floor 1 Tower Lobby"),
    "Pepperman":            PTLevelData("boss_pepperman", "Floor 1 Tower Lobby", True),
    "Oregano Desert":       PTLevelData("badland", "Floor 2 Western District"),
    "Wasteyard":            PTLevelData("graveyard", "Floor 2 Western District"),
    "Fun Farm":             PTLevelData("farm", "Floor 2 Western District"),
    "Fastfood Saloon":      PTLevelData("saloon", "Floor 2 Western District"),
    "The Vigilante":        PTLevelData("boss_vigilante", "Floor 2 Western District", True),
    "Crust Cove":           PTLevelData("plage", "Floor 3 Vacation Resort"),
    "Gnome Forest":         PTLevelData("forest", "Floor 3 Vacation Resort"),
    "Deep-Dish 9":          PTLevelData("space", "Floor 3 Vacation Resort"),
    "GOLF":                 PTLevelData("minigolf", "Floor 3 Vacation Resort"),
    "The Noise":            PTLevelData("boss_noise", "Floor 3 Vacation Resort", True),
    "The Doise":            PTLevelData("boss_noise", "Floor 3 Vacation Resort", True),
    "The Pig City":         PTLevelData("street", "Floor 4 Slum"),
    "Peppibot Factory":     PTLevelData("industrial", "Floor 4 Slum"),
    "Oh Shit!":             PTLevelData("sewer", "Floor 4 Slum"),
    "Freezerator":          PTLevelData("freezer", "Floor 4 Slum"),
    "Fake Peppino":         PTLevelData("boss_fakepep", "Floor 4 Slum", True),
    "Pizzascare":           PTLevelData("chateau", "Floor 5 Staff Only"),
    "Don't Make A Sound":   PTLevelData("kidsparty", "Floor 5 Staff Only"),
    "WAR":                  PTLevelData("war", "Floor 5 Staff Only"),
    "Pizzaface":            PTLevelData("boss_pizzaface", "Floor 5 Staff Only", True),
}

from .Options import PTOptions, pt_option_groups, pt_option_presets

def internal_from_external(name: str):
    if "Secret 1" in name:
        return level_data[name.replace(" Secret 1", "")].internal_name + "1"
    if "Secret 2" in name:
        return level_data[name.replace(" Secret 2", "")].internal_name + "2"
    if "Secret 3" in name:
        return level_data[name.replace(" Secret 3", "")].internal_name + "3"
    return level_data[name].internal_name

def external_from_internal_secrets(name: str, aliases: dict):
    if "1" in name:
        return aliases[name.replace("1", "")] + " Secret 1"
    if "2" in name:
        return aliases[name.replace("2", "")] + " Secret 2"
    if "3" in name:
        return aliases[name.replace("3", "")] + " Secret 3"

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="PTClient", args=args)


components.append(Component("Pizza Tower Client", "PTClient", func=launch_client, component_type=Type.CLIENT, icon="pizza"))

icon_paths["pizza"] = f"ap:{__name__}/pizza.png"

class PizzaTowerWebWorld(WebWorld):
    theme = "stone"
    option_groups = pt_option_groups
    options_presets = pt_option_presets

    tutorials = [Tutorial(
            "MultiWorld Setup Guide",
            "A guide to setting up Pizza Tower for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Skizzers"]
        )
    ]

class PizzaTowerWorld(World):
    """
    Down-on-his-luck pizza chef Peppino Spaghetti and his restaurant are threatened by a sentient floating pizza... and this time
    all of his abilities are gone, too! Climb up and bring down the Pizza Tower to save your restaurant in this cheesy, saucy,
    Wario Land 4-inspired platformer!
    """
    game = "Pizza Tower"
    web = PizzaTowerWebWorld()
    topology_present = False

    options_dataclass = PTOptions
    options: PTOptions

    toppin_number: int = 0
    pumpkin_number: int = 0

    floors_list: list[str] = [
        "Floor 1 Tower Lobby",
        "Floor 2 Western District",
        "Floor 3 Vacation Resort",
        "Floor 4 Slum",
        "Floor 5 Staff Only"
    ]
    gates_map: dict[str, str]
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

    def hub_gate_rando(self):
        level_order: dict[str, str] = {}
        place_locked: dict[str, str] = {}
        level_queue: list[str] = []
        boss_queue: list[str] = []

        #fill up level order and randomization queue
        for gate in level_data:
            if ((gate == "The Doise" and self.options.character.value == PTChars.PEPPINO) or
                (gate == "The Noise" and self.options.character.value != PTChars.PEPPINO) or
                (gate == "Tutorial" and self.options.character.value == PTChars.SWAP)):
                continue
            level_order[gate] = None
            boss_queue.append(gate) if level_data[gate].is_boss else level_queue.append(gate)

        if self.options.randomize_gates.value != self.options.randomize_gates.option_vanilla:
            #grab starting levels
            place_locked.update(self.get_starting_levels())
            #load plando settings
            place_locked.update(self.options.gate_plando)

        #add un-randomized levels to plando
        for lvl in level_order:
            if ((self.options.randomize_gates.value == self.options.randomize_gates.option_vanilla) or
                (not level_data[lvl].is_boss and self.options.randomize_gates.value == self.options.randomize_gates.option_bosses) or
                (level_data[lvl].is_boss and self.options.randomize_gates.value == self.options.randomize_gates.option_levels)):
                place_locked.update({lvl: lvl})

        #always place pizzaface at pizzaface
        place_locked.update({"Pizzaface": "Pizzaface"})

        #place locked levels
        for gate in place_locked:
            lvl = place_locked[gate]
            level_order[gate] = lvl
            boss_queue.remove(lvl) if level_data[lvl].is_boss else level_queue.remove(lvl)

        if not self.options.shuffle_boss_keys.value and self.options.randomize_gates.value == self.options.randomize_gates.option_full_shuffle:
            self.options.randomize_gates.value = self.options.randomize_gates.option_levels_and_bosses
            info(f"{self.player_name} set Randomize Hub Gates to Full Shuffle which requires Shuffle Boss Keys to be enabled, changing shuffle mode to Levels and Bosses")

        #full shuffle
        if self.options.randomize_gates.value == self.options.randomize_gates.option_full_shuffle:
            gates_queue = level_queue + boss_queue
            self.random.shuffle(gates_queue)
            for gate in level_order:
                if level_order[gate] == None:
                    level_order[gate] = gates_queue.pop()
        #typed shuffle
        elif self.options.randomize_gates.value != self.options.randomize_gates.option_vanilla:
            for gate in level_order:
                if level_order[gate] == None:
                    if level_data[gate].is_boss:
                        level_order[gate] = boss_queue.pop()
                    else:
                        level_order[gate] = level_queue.pop()

        return level_order

    def get_starting_levels(self) -> dict[str, str]:
        ok_start_levels = []
        locked_starting_levels: dict[str, str] = {}
        #selection of non-restrictive levels for move rando
        if self.options.do_move_rando.value:
            ok_start_levels = [ 
                "Pizzascape",
                "Ancient Cheese",
                "Bloodsauce Dungeon",
                "The Pig City",
                "Don't Make A Sound"
            ]

            if self.options.character != PTChars.PEPPINO:
                ok_start_levels.append("Freezerator")
            if self.options.difficulty.value > 0 and not self.options.do_transfo_rando.value:
                ok_start_levels.append("Wasteyard")
                ok_start_levels.append("GOLF")
            
        #selection of non-restrictive levels for transfo rando
        elif self.options.do_transfo_rando.value:
            ok_start_levels = [
                "John Gutter",
                "Pizzascape",
                "Ancient Cheese",
                "Bloodsauce Dungeon",
                "Oregano Desert",
                "Crust Cove",
                "Gnome Forest",
                "The Pig City",
                "Don't Make A Sound",
                "Peppibot Factory",
                "Oh Shit!",
                "Freezerator",
                "Pizzascare"
            ]
        
        starting_gates = [
            "John Gutter",
            "Pizzascape"
        ]
        #manually place start levels
        if ok_start_levels:
            self.random.shuffle(ok_start_levels)
            for gate in starting_gates:
                locked_starting_levels.update({gate: ok_start_levels.pop()})

        return locked_starting_levels

    def prepare_ut(self, re_gen_passthrough):
        external_from_internal = {}
        for level in level_data.keys():
            external_from_internal.update({level_data[level].internal_name: level})

        slot_data = re_gen_passthrough[self.game]
        self.gates_map = {external_from_internal[gate]: external_from_internal[slot_data["rando_gates"][gate]] for gate in slot_data["rando_gates"]}
        self.secret_map = {external_from_internal_secrets(sec, external_from_internal): external_from_internal_secrets(slot_data["rando_secrets"][sec], external_from_internal) for sec in slot_data["rando_secrets"]}
        self.options.character.value = slot_data["character"]
        self.options.difficulty.value = slot_data["difficulty"]
        self.options.floor_1_cost.value = slot_data["floor_1_toppins"]
        self.options.floor_2_cost.value = slot_data["floor_2_toppins"]
        self.options.floor_3_cost.value = slot_data["floor_3_toppins"]
        self.options.floor_4_cost.value = slot_data["floor_4_toppins"]
        self.options.floor_5_cost.value = slot_data["floor_5_toppins"]
        self.options.open_world.value = slot_data["open_world"]
        self.options.bonus_ladders.value = slot_data["bonus_ladders"]
        self.options.treasure_checks.value = slot_data["treasure_checks"]
        self.options.srank_checks.value = slot_data["srank_checks"]
        self.options.prank_checks.value = slot_data["prank_checks"]
        self.options.cheftask_checks.value = slot_data["cheftask_checks"]
        self.options.secret_checks.value = slot_data["secret_checks"]
        self.options.shuffle_lap2.value = slot_data["shuffle_lap2"]
        self.options.pumpkin_checks.value = slot_data["pumpkin_checks"]
        self.options.pumpkin_count.value = slot_data["pumpkin_count"]
        self.options.do_move_rando.value = slot_data["do_move_rando"]
        self.options.do_transfo_rando.value = slot_data["do_transfo_rando"]
        self.options.completion_goal.value = slot_data["completion_goal"]
        self.options.snotty_floor.value = slot_data["snotty_floor"]
        self.options.secret_complete_checks.value = slot_data["secret_complete_checks"]

    def generate_early(self):
        if self.options.do_move_rando and self.options.do_transfo_rando:
            if self.options.character == PTChars.PEPPINO:
                early_item_list = ["Superjump", "Wallclimb"]
            elif self.options.character == PTChars.NOISE:
                early_item_list = ["Superjump", "Wallbounce"]
            else:
                early_item_list = ["Superjump", "Wallclimb", "Wallbounce"]
            early_item_name = self.random.choice(early_item_list)
            self.multiworld.early_items[self.player][early_item_name] = 1
            if self.options.character != PTChars.PEPPINO:
                early_item_list_1 = ["Bodyslam", "Crusher", "Tornado"]
                early_item_name_1 = self.random.choice(early_item_list_1)
            else:
                early_item_name_1 = "Bodyslam"
            self.multiworld.early_items[self.player][early_item_name_1] = 1

        self.gates_map: dict[str, str] = {}
        self.secret_map = {}
        
        #Raise error if snotty goal while snotty is on floor 1
        if self.options.snotty_floor.value == 1 and self.options.completion_goal.value == self.options.completion_goal.option_Snotty:
            raise OptionError(f"Pizza Tower - {self.player_name}: Combination of floor 1 Snotty and Snotty completion goal doesn't create enough locations for playable world")

        #Support for universal tracker
        re_gen_passthrough = getattr(self.multiworld,"re_gen_passthrough",{})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            self.prepare_ut(re_gen_passthrough)
        else:
            self.gates_map = self.hub_gate_rando()

        #slice floors/levels/bosses list if snotty goal
        if self.options.completion_goal == self.options.completion_goal.option_Snotty:
            self.floors_list = self.floors_list[0 : self.options.snotty_floor.value]

    def create_item(self, name: str) -> PTItem:
        return PTItem(name, pt_items[name].classification, pt_items[name].id, self.player)
    
    def create_regions(self):
        from .Regions import create_regions
        create_regions(self.player, self.multiworld, self.options, self.gates_map, self.floors_list)

    def create_items(self):
        pizza_itempool = []

        unfilled_locations = self.multiworld.get_unfilled_locations(self.player)
        locations_to_fill = len(unfilled_locations)
        excluded_locations = 0
        for location in unfilled_locations:
            if location.progress_type == LocationProgressType.EXCLUDED:
                excluded_locations += 1

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
                for i in range(len(self.floors_list)-1):
                    pizza_itempool.append(self.create_item("Boss Key"))
            else:
                for lvl in self.gates_map.values():
                    if level_data[lvl].is_boss and lvl != "Pizzaface":
                        self.multiworld.get_location(lvl+" Defeated", self.player).place_locked_item(self.create_item("Boss Key"))
                        locations_to_fill -= 1 #manually placed 4 items
        
        #add toppins, if we can
        for i in range(self.options.toppin_count):
            if locations_to_fill - excluded_locations <= len(pizza_itempool):
                break
            pizza_itempool.append(self.create_item("Toppin"))
            self.toppin_number = i+1

        #add pumpkins, if we can
        if self.options.pumpkin_checks:
            for i in range(self.options.pumpkin_count):
                if locations_to_fill - excluded_locations <= len(pizza_itempool):
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
                info(f"{self.player_name} set traps to enabled, but all trap weights are set to zero")
        
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
            info(f"{self.player_name} set all filler weights to 0,, filling left over spaces with Primo Burg instead")
        
        #if there's still slots left over from rounding fill them with primo burgs
        for i in range(locations_to_fill - len(pizza_itempool)):
            pizza_itempool.append(self.create_item("Primo Burg"))

        self.multiworld.itempool += pizza_itempool

    def set_rules(self):
        from .Rules import set_rules
        set_rules(self.multiworld, self, self.options, self.toppin_number, self.pumpkin_number, self.gates_map)
        if self.options.completion_goal == self.options.completion_goal.option_CTOP:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("The Crumbling Tower of Pizza Complete", "Location", self.player)
        elif self.options.completion_goal == self.options.completion_goal.option_Snotty:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Snotty Murdered", "Location", self.player)

    def get_filler_item_name(self) -> str:
        weighted_filler = []
        for filler in get_item_from_category("Filler"):
            for i in range(self.options.filler_weights[filler]):
                weighted_filler.append(filler)
        
        return self.random.choice(weighted_filler)
    
    def write_spoiler_header(self, spoiler_handle: TextIO):
        apversion_string = str(self.world_version[0]) + "." + str(self.world_version[1]) + "." + str(self.world_version[2])
        spoiler_handle.write('{:<32} {:0}'.format("APWorld Version: ", apversion_string))
        spoiler_handle.write("\n")

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        ex_hint_info = dict()
        gates_map_inv = {value: key for key, value in self.gates_map.items()}
        for location in self.multiworld.get_locations(self.player):
            if location.parent_region.name in list(level_data.values()):
                ex_hint_info.update({location.address: level_data[gates_map_inv[location.parent_region.name]].floor})
            elif location.parent_region.name == "The Crumbling Tower of Pizza":
                ex_hint_info.update({location.address: "Floor 5 Staff Only"})
            elif location.parent_region.name == "Tricky Treat":
                ex_hint_info.update({location.address: "Floor 1 Tower Lobby"})
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
            "rando_gates": {internal_from_external(gate): internal_from_external(self.gates_map[gate]) for gate in self.gates_map},
            "rando_secrets": {internal_from_external(sec): internal_from_external(self.secret_map[sec]) for sec in self.secret_map},
            "open_world": bool(self.options.open_world),
            "bonus_ladders": int(self.options.bonus_ladders),
            "character": int(self.options.character.value),
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
            "do_move_rando": bool(self.options.do_move_rando), #for poptracker
            "do_transfo_rando": bool(self.options.do_transfo_rando), #for poptracker
            "apworld_version": list(self.world_version),
            "completion_goal": int(self.options.completion_goal),
            "snotty_floor": int(self.options.snotty_floor),
            "secret_complete_checks": bool(self.options.secret_complete_checks),
            "rando_seed": int(self.random.randint(0, pow(2, 32) - 1)) #random unsigned 32 bit int
        }