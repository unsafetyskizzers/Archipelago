from BaseClasses import Region, MultiWorld
from .Locations import PTLocation, pt_locations
from .Options import PTOptions
from . import PTChars

def create_regions(player: int, world: MultiWorld, options: PTOptions, level_map: dict, boss_map: dict, floors_list: list):
    levels_checks = [
        "Mushroom Toppin",
        "Cheese Toppin",
        "Tomato Toppin",
        "Sausage Toppin",
        "Pineapple Toppin",
        "Complete"
    ]

    bosses_checks = [
        "Defeated"
    ]

    tutorial_checks = [
        "Complete",
        "Complete in under 2 minutes"
    ]

    cheftasks_checks = {
        "John Gutter": [
            "Chef Task: John Gutted",
            "Chef Task: Primate Rage",
            "Chef Task: Let's Make This Quick"
        ],
        "Pizzascape": [
            "Chef Task: Shining Armor",
            "Chef Task: Spoonknight",
            "Chef Task: Spherical"
        ],
        "Ancient Cheese": [
            "Chef Task: Thrill Seeker",
            "Chef Task: Volleybomb",
            "Chef Task: Delicacy",
        ],
        "Bloodsauce Dungeon": [
            "Chef Task: Eruption Man",
            "Chef Task: Very Very Hot Sauce",
            "Chef Task: Unsliced Pizzaman"
        ],
        "Oregano Desert": [
            "Chef Task: Peppino's Rain Dance",
            "Chef Task: Unnecessary Violence",
            "Chef Task: Alien Cow"
        ],
        "Wasteyard": [
            "Chef Task: Alive and Well",
            "Chef Task: Pretend Ghost",
            "Chef Task: Ghosted"
        ],
        "Fun Farm": [
            "Chef Task: Good Egg",
            "Chef Task: No One Is Safe",
            "Chef Task: Cube Menace"
        ],
        "Fastfood Saloon": [
            "Chef Task: Royal Flush",
            "Chef Task: Non-Alcoholic",
            "Chef Task: Already Pressed"
        ],
        "Crust Cove": [
            "Chef Task: Demolition Expert",
            "Chef Task: Blowback",
            "Chef Task: X"
        ],
        "Gnome Forest": [
            "Chef Task: Bee Nice",
            "Chef Task: Bullseye",
            "Chef Task: Lumberjack"
        ],
        "Deep-Dish 9": [
            "Chef Task: Blast 'Em Asteroids",
            "Chef Task: Turbo Tunnel",
            "Chef Task: Man Meteor"
        ],
        "GOLF": [
            "Chef Task: Primo Golfer",
            "Chef Task: Helpful Burger",
            "Chef Task: Nice Shot"
        ],
        "The Pig City": [
            "Chef Task: Say Oink!",
            "Chef Task: Pan Fried",
            "Chef Task: Strike!"
        ],
        "Peppibot Factory": [
            "Chef Task: There Can Be Only One",
            "Chef Task: Whoop This!",
            "Chef Task: Unflattening"
        ],
        "Oh Shit!": [
            "Chef Task: Food Clan",
            "Chef Task: Can't Fool Me",
            "Chef Task: Penny Pincher"
        ],
        "Freezerator": [
            "Chef Task: Ice Climber",
            "Chef Task: Season's Greetings",
            "Chef Task: Frozen Nuggets"
        ],
        "Pizzascare": [
            "Chef Task: Haunted Playground",
            "Chef Task: Skullsplitter",
            "Chef Task: Cross To Bare",
        ],
        "Don't Make A Sound": [
            "Chef Task: Let Them Sleep",
            "Chef Task: Jumpspared",
            "Chef Task: And This... Is My Gun On A Stick!",
        ],
        "WAR": [
            "Chef Task: Trip to the Warzone",
            "Chef Task: Sharpshooter",
            "Chef Task: Decorated Veteran",
        ],
        "Pepperman": [
            "Chef Task: The Critic"
        ],
        "The Vigilante": [
            "Chef Task: The Ugly"
        ],
        "The Noise": [
            "Chef Task: Denoise"
        ],
        "The Doise": [
            "Chef Task: Denoise"
        ],
        "Fake Peppino": [
            "Chef Task: Faker"
        ],
        "Pizzaface": [
            "Chef Task: Face Off"
        ],
        "Floor Tasks": [
            "Chef Task: S Ranked #1",
            "Chef Task: P Ranked #1",
            "Chef Task: S Ranked #2",
            "Chef Task: P Ranked #2",
            "Chef Task: S Ranked #3",
            "Chef Task: P Ranked #3",
            "Chef Task: S Ranked #4",
            "Chef Task: P Ranked #4",
            "Chef Task: S Ranked #5",
            "Chef Task: P Ranked #5",
        ]
    }

    tower_regions: list[Region] = []

    tower_regions.append(Region("Menu", player, world, None))

    #extra mf checks!!!!!
    if options.secret_checks:
        levels_checks += ["Secret 1", "Secret 2", "Secret 3"]
    if options.treasure_checks:
        levels_checks.append("Treasure")
    if options.srank_checks:
        levels_checks.append("S Rank")
        bosses_checks.append("S Rank")
    if options.prank_checks:
        levels_checks.append("P Rank")
        bosses_checks.append("P Rank")
    if options.pumpkin_checks:
        levels_checks.append("Pumpkin")
    if options.character == PTChars.PEPPINO:
        tutorial_checks += [
            "Mushroom Toppin",
            "Cheese Toppin",
            "Tomato Toppin",
            "Sausage Toppin",
            "Pineapple Toppin",
        ]
    elif options.character == PTChars.SWAP:
        tutorial_checks = []

    #create regions and add locations
    floor_index = 1
    for flr in floors_list:
        floor_region = Region(flr, player, world, flr)
        #add s/p ranked chef tasks for each floor, if 
        if options.cheftask_checks:
            if options.completion_goal != options.completion_goal.option_Snotty or (options.completion_goal == options.completion_goal.option_Snotty and floor_index != (options.snotty_floor.value)):
                floor_region.locations.append(PTLocation(player, "Chef Task: S Ranked #" + str(floor_index), pt_locations["Chef Task: S Ranked #" + str(floor_index)], floor_region))
                floor_region.locations.append(PTLocation(player, "Chef Task: P Ranked #" + str(floor_index), pt_locations["Chef Task: P Ranked #" + str(floor_index)], floor_region))
        tower_regions.append(floor_region)
        floor_index += 1

    if options.character != PTChars.SWAP:
        region_tut = Region("Tutorial", player, world, None)
        for chk in tutorial_checks:
            check_name = "Tutorial " + chk
            new_location = PTLocation(player, check_name, pt_locations[check_name], region_tut)
            region_tut.locations.append(new_location)
        tower_regions.append(region_tut)

    for lvl in level_map.values():
        check_region = Region(lvl, player, world, None)
        for chk in levels_checks:
            check_name = lvl + " " + chk
            new_location = PTLocation(player, check_name, pt_locations[check_name], check_region)
            check_region.locations.append(new_location)
        if options.cheftask_checks:
            add_cheftasks(lvl, player, check_region, cheftasks_checks)

        tower_regions.append(check_region)

    for boss in boss_map.values():
        check_region = Region(boss, player, world, None)
        for chk in bosses_checks:
            if boss == "Pizzaface" and chk != "Defeated":
                continue
            
            check_name = boss + " " + chk
            new_location = PTLocation(player, check_name, pt_locations[check_name], check_region)
            check_region.locations.append(new_location)
        if options.cheftask_checks:
            add_cheftasks(boss, player, check_region, cheftasks_checks)
        
        tower_regions.append(check_region)

    #odd regions
    if options.completion_goal == options.completion_goal.option_CTOP:
        region_ctop = Region("The Crumbling Tower of Pizza", player, world, None)

        region_ctop.locations.append(PTLocation(player, "The Crumbling Tower of Pizza Complete", 214, region_ctop))
        if options.srank_checks:
            region_ctop.locations.append(PTLocation(player, "The Crumbling Tower of Pizza S Rank", 247, region_ctop))
        if options.prank_checks:
            region_ctop.locations.append(PTLocation(player, "The Crumbling Tower of Pizza P Rank", 328, region_ctop))
        
        tower_regions.append(region_ctop)
    
    tower_regions[options.snotty_floor].locations.append(PTLocation(player, "Snotty Murdered", 220, tower_regions[options.snotty_floor]))

    if options.pumpkin_checks:
        region_trickytreat = Region("Tricky Treat", player, world, None)

        if options.completion_goal == options.completion_goal.option_CTOP:
            region_ctop.locations.append(PTLocation(player, "The Crumbling Tower of Pizza Pumpkin", 446, region_ctop))

        for i in range(5):
            loc = f"Tricky Treat Main Path Pumpkin {i+1}"
            region_trickytreat.locations.append(PTLocation(player, loc, pt_locations[loc], region_trickytreat))
            loc = f"Tricky Treat Side Path Pumpkin {i+1}"
            region_trickytreat.locations.append(PTLocation(player, loc, pt_locations[loc], region_trickytreat))
        if options.cheftask_checks:
            region_trickytreat.locations.append(PTLocation(player, "Chef Task: Tricksy", 458, region_trickytreat))
            #only enable pumpkin munchkin if your goal has you reach CTOP
            if options.completion_goal == options.completion_goal.option_CTOP:
                region_trickytreat.locations.append(PTLocation(player, "Chef Task: Pumpkin Munchkin", 457, region_trickytreat))
        tower_regions.append(region_trickytreat)

    world.regions += tower_regions

def add_cheftasks(lvl: str, player: int, check_region: Region, cheftasks_checks: dict):
    for chk in cheftasks_checks[lvl]:
        new_location = PTLocation(player, chk, pt_locations[chk], check_region)
        check_region.locations.append(new_location)