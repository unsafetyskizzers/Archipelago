from BaseClasses import Item, ItemClassification

class PTItem(Item):
    game: str = "Pizza Tower"

def get_item_from_category(category: str) -> list:
    itemlist = []
    for item in pt_items:
        if pt_items.get(item)[0] == category:
            itemlist.append(item)
    
    return itemlist


pt_items = {
    "Toppin":                   ("Progression", 101, ItemClassification.progression_skip_balancing),
    "Boss Key":                 ("Progression", 102, ItemClassification.progression),
    "Lap 2 Portals":            ("Progression", 149, ItemClassification.progression),
    "Pumpkin":                  ("Progression", 150, ItemClassification.progression_skip_balancing),

    "Mach 4":                   ("Moves Shared", 103, ItemClassification.progression),
    "Uppercut":                 ("Moves Shared", 104, ItemClassification.progression),
    "Superjump":                ("Moves Shared", 105, ItemClassification.progression),
    "Grab":                     ("Moves Shared", 106, ItemClassification.progression),
    #ID 107 has been reassigned to "Bomb"
    "Taunt":                    ("Moves Shared", 108, ItemClassification.progression),
    "Supertaunt":               ("Moves Shared", 109, ItemClassification.progression),
    "Bodyslam":                 ("Moves Shared", 110, ItemClassification.progression),
    "Breakdance":               ("Moves Shared", 111, ItemClassification.filler),

    "Wallclimb":                ("Moves Peppino", 112, ItemClassification.progression),
    #"Dive": (113, ItemClassification.useful),
    "Double Jump":              ("Moves Peppino", 114, ItemClassification.progression),
    "Rat Kick":                 ("Moves Peppino", 115, ItemClassification.progression),
    #"Wall Jump": (116, ItemClassification.progression),
    "Spin Attack":              ("Moves Peppino", 117, ItemClassification.useful),

    "Wallbounce":               ("Moves Noise", 118, ItemClassification.progression),
    "Tornado":                  ("Moves Noise", 119, ItemClassification.progression),
    "Crusher":                  ("Moves Noise", 120, ItemClassification.progression),
    "Bomb":                     ("Moves Noise", 107, ItemClassification.progression),

    "Clown Trap":               ("Trap", 121, ItemClassification.trap),
    "Timer Trap":               ("Trap", 122, ItemClassification.trap),
    "Ghost Trap":               ("Trap", 123, ItemClassification.trap),
    "Fake Santa Trap":          ("Trap", 124, ItemClassification.trap),
    "Oktoberfest!":             ("Trap", 125, ItemClassification.trap),
    "Granny Trap":              ("Trap", 147, ItemClassification.trap),

    "Permanent 10 Points":      ("Filler", 126, ItemClassification.filler),
    "Permanent 50 Points":      ("Filler", 127, ItemClassification.filler),
    "Permanent 100 Points":     ("Filler", 128, ItemClassification.filler),
    "Primo Burg":               ("Filler", 129, ItemClassification.filler),
    "Cross Buff":               ("Filler", 130, ItemClassification.filler),
    "Pizza Shield":             ("Filler", 131, ItemClassification.filler),

    #transfo items;     get used                 right now
    "Ball":                     ("Transformation", 132, ItemClassification.progression),
    "Knight":                   ("Transformation", 133, ItemClassification.progression),
    "Firemouth":                ("Transformation", 134, ItemClassification.progression),
    "Ghost":                    ("Transformation", 135, ItemClassification.progression),
    "Mort":                     ("Transformation", 136, ItemClassification.progression),
    "Weenie":                   ("Transformation", 137, ItemClassification.progression),
    "Barrel":                   ("Transformation", 138, ItemClassification.progression),
    "Olive Bubble":             ("Transformation", 139, ItemClassification.progression),
    "Rocket":                   ("Transformation", 140, ItemClassification.progression),
    "Pizzabox":                 ("Transformation", 141, ItemClassification.progression),
    "Sticky Cheese":            ("Transformation", 142, ItemClassification.progression),
    "Satan's Choice":           ("Transformation", 143, ItemClassification.progression),
    "Shotgun":                  ("Transformation", 144, ItemClassification.progression),
    "Revolver":                 ("Transformation", 145, ItemClassification.progression),

    "Nothing":                  ("Filler", 146, ItemClassification.filler),

    "Jumpscare":                ("Trap", 148, ItemClassification.trap), #replaces oktoberfest if options.jumpscare == true

    #clothes
    "Clothes: Classic Cook":    ("Clothes Peppino", 300, ItemClassification.filler), #unused
    "Clothes: Unfunny Cook":    ("Clothes Peppino", 301, ItemClassification.filler),
    "Clothes: Money Green":     ("Clothes Peppino", 302, ItemClassification.filler),
    "Clothes: SAGE Blue":       ("Clothes Peppino", 303, ItemClassification.filler),
    "Clothes: Blood Red":       ("Clothes Peppino", 304, ItemClassification.filler),
    "Clothes: TV Purple":       ("Clothes Peppino", 305, ItemClassification.filler),
    "Clothes: Dark Cook":       ("Clothes Peppino", 306, ItemClassification.filler),
    "Clothes: Shitty Cook":     ("Clothes Peppino", 307, ItemClassification.filler),
    "Clothes: Golden God":      ("Clothes Peppino", 308, ItemClassification.filler),
    "Clothes: Garish Cook":     ("Clothes Peppino", 309, ItemClassification.filler),
    "Clothes: Mooney Orange":   ("Clothes Peppino", 310, ItemClassification.filler),
    "Clothes: Funny Polka":     ("Clothes Peppino", 311, ItemClassification.filler),
    "Clothes: Itchy Sweater":   ("Clothes Peppino", 312, ItemClassification.filler),
    "Clothes: Pizza Man":       ("Clothes Peppino", 313, ItemClassification.filler),
    "Clothes: Bowling Stripes": ("Clothes Peppino", 314, ItemClassification.filler),
    "Clothes: Goldemanne":      ("Clothes Peppino", 315, ItemClassification.filler),
    "Clothes: Bad Bones":       ("Clothes Peppino", 316, ItemClassification.filler),
    "Clothes: PP Shirt":        ("Clothes Peppino", 317, ItemClassification.filler),
    "Clothes: War Camo":        ("Clothes Peppino", 318, ItemClassification.filler),
    "Clothes: John Suit":       ("Clothes Peppino", 319, ItemClassification.filler),
    "Clothes: Noise":           ("Clothes Noise", 320, ItemClassification.filler), #unused
    "Clothes: Boise":           ("Clothes Noise", 321, ItemClassification.filler),
    "Clothes: Roise":           ("Clothes Noise", 322, ItemClassification.filler),
    "Clothes: Poise":           ("Clothes Noise", 323, ItemClassification.filler),
    "Clothes: Reverse":         ("Clothes Noise", 324, ItemClassification.filler),
    "Clothes: Critic":          ("Clothes Noise", 325, ItemClassification.filler),
    "Clothes: Outlaw":          ("Clothes Noise", 326, ItemClassification.filler),
    "Clothes: Anti-Doise":      ("Clothes Noise", 327, ItemClassification.filler),
    "Clothes: Flesh Eater":     ("Clothes Noise", 328, ItemClassification.filler),
    "Clothes: Super":           ("Clothes Noise", 329, ItemClassification.filler),
    "Clothes: Fast Porcupine":  ("Clothes Noise", 330, ItemClassification.filler),
    "Clothes: Feminine Side":   ("Clothes Noise", 331, ItemClassification.filler),
    "Clothes: The Real Doise":  ("Clothes Noise", 332, ItemClassification.filler),
    "Clothes: Forest Goblin":   ("Clothes Noise", 333, ItemClassification.filler),
    "Clothes: Racer":           ("Clothes Noise", 334, ItemClassification.filler),
    "Clothes: Comedian":        ("Clothes Noise", 335, ItemClassification.filler),
    "Clothes: Banana":          ("Clothes Noise", 336, ItemClassification.filler),
    "Clothes: Noise TV":        ("Clothes Noise", 337, ItemClassification.filler),
    "Clothes: Madman":          ("Clothes Noise", 338, ItemClassification.filler),
    "Clothes: Bubbly":          ("Clothes Noise", 339, ItemClassification.filler),
    "Clothes: Well Done":       ("Clothes Noise", 340, ItemClassification.filler),
    "Clothes: Granny Kisses":   ("Clothes Noise", 341, ItemClassification.filler),
    "Clothes: Tower Guy":       ("Clothes Noise", 342, ItemClassification.filler),
    "Clothes: Candy Wrapper":   ("Clothes Shared", 343, ItemClassification.filler),
    "Clothes: Bloodstained":    ("Clothes Shared", 344, ItemClassification.filler),
    "Clothes: Autumn":          ("Clothes Shared", 345, ItemClassification.filler),
    "Clothes: Pumpkin":         ("Clothes Shared", 346, ItemClassification.filler),
    "Clothes: Fur":             ("Clothes Shared", 347, ItemClassification.filler),
    "Clothes: Eyes":            ("Clothes Shared", 348, ItemClassification.filler),
}

item_categories = [
    "Progression",
    "Moves Shared",
    "Moves Peppino",
    "Moves Noise",
    "Trap",
    "Filler",
    "Transformation",
    "Clothes Shared",
    "Clothes Peppino",
    "Clothes Noise"
]

pt_item_groups = { cat: set(get_item_from_category(cat)) for cat in item_categories }