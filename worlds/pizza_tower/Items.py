from BaseClasses import Item, ItemClassification
from typing import NamedTuple

class PTItem(Item):
    game: str = "Pizza Tower"

class PTItemData(NamedTuple):
    category: str
    id: int
    classification: ItemClassification

def get_item_from_category(category: str) -> list:
    itemlist = []
    for item in pt_items:
        if pt_items[item].category == category:
            itemlist.append(item)
    
    return itemlist


pt_items: dict[str, PTItemData] = {
    "Toppin":                   PTItemData("Progression", 101, ItemClassification.progression_deprioritized_skip_balancing),
    "Boss Key":                 PTItemData("Progression", 102, ItemClassification.progression),
    "Lap 2 Portals":            PTItemData("Progression", 149, ItemClassification.progression),
    "Pumpkin":                  PTItemData("Progression", 150, ItemClassification.progression_deprioritized_skip_balancing),

    "Mach 4":                   PTItemData("Moves Shared", 103, ItemClassification.progression),
    "Uppercut":                 PTItemData("Moves Shared", 104, ItemClassification.progression),
    "Superjump":                PTItemData("Moves Shared", 105, ItemClassification.progression),
    "Grab":                     PTItemData("Moves Shared", 106, ItemClassification.progression),
    #ID 107 has been reassigned to "Bomb"
    "Taunt":                    PTItemData("Moves Shared", 108, ItemClassification.progression),
    "Supertaunt":               PTItemData("Moves Shared", 109, ItemClassification.progression),
    "Bodyslam":                 PTItemData("Moves Shared", 110, ItemClassification.progression),
    "Breakdance":               PTItemData("Moves Shared", 111, ItemClassification.filler),

    "Wallclimb":                PTItemData("Moves Peppino", 112, ItemClassification.progression),
    #"Dive": (113, ItemClassification.useful),
    "Double Jump":              PTItemData("Moves Peppino", 114, ItemClassification.progression),
    "Rat Kick":                 PTItemData("Moves Peppino", 115, ItemClassification.progression),
    #"Wall Jump": (116, ItemClassification.progression),
    "Spin Attack":              PTItemData("Moves Peppino", 117, ItemClassification.progression),

    "Wallbounce":               PTItemData("Moves Noise", 118, ItemClassification.progression),
    "Tornado":                  PTItemData("Moves Noise", 119, ItemClassification.progression),
    "Crusher":                  PTItemData("Moves Noise", 120, ItemClassification.progression),
    "Bomb":                     PTItemData("Moves Noise", 107, ItemClassification.progression),

    "Clown Trap":               PTItemData("Trap", 121, ItemClassification.trap),
    "Timer Trap":               PTItemData("Trap", 122, ItemClassification.trap),
    "Ghost Trap":               PTItemData("Trap", 123, ItemClassification.trap),
    "Fake Santa Trap":          PTItemData("Trap", 124, ItemClassification.trap),
    "Oktoberfest!":             PTItemData("Trap", 125, ItemClassification.trap),
    "Granny Trap":              PTItemData("Trap", 147, ItemClassification.trap),

    "Permanent 10 Points":      PTItemData("Filler", 126, ItemClassification.filler),
    "Permanent 50 Points":      PTItemData("Filler", 127, ItemClassification.filler),
    "Permanent 100 Points":     PTItemData("Filler", 128, ItemClassification.filler),
    "Primo Burg":               PTItemData("Filler", 129, ItemClassification.filler),
    "Cross Buff":               PTItemData("Filler", 130, ItemClassification.filler),
    "Pizza Shield":             PTItemData("Filler", 131, ItemClassification.filler),

    #transfo items;     get used                 right now
    "Ball":                     PTItemData("Transformation", 132, ItemClassification.progression),
    "Knight":                   PTItemData("Transformation", 133, ItemClassification.progression),
    "Firemouth":                PTItemData("Transformation", 134, ItemClassification.progression),
    "Ghost":                    PTItemData("Transformation", 135, ItemClassification.progression),
    "Mort":                     PTItemData("Transformation", 136, ItemClassification.progression),
    "Weenie":                   PTItemData("Transformation", 137, ItemClassification.progression),
    "Barrel":                   PTItemData("Transformation", 138, ItemClassification.progression),
    "Olive Bubble":             PTItemData("Transformation", 139, ItemClassification.progression),
    "Rocket":                   PTItemData("Transformation", 140, ItemClassification.progression),
    "Pizzabox":                 PTItemData("Transformation", 141, ItemClassification.progression),
    "Sticky Cheese":            PTItemData("Transformation", 142, ItemClassification.progression),
    "Satan's Choice":           PTItemData("Transformation", 143, ItemClassification.progression),
    "Shotgun":                  PTItemData("Transformation", 144, ItemClassification.progression),
    "Revolver":                 PTItemData("Transformation", 145, ItemClassification.progression),

    "Nothing":                  PTItemData("Filler", 146, ItemClassification.filler),

    "Jumpscare":                PTItemData("Trap", 148, ItemClassification.trap), #replaces oktoberfest if options.jumpscare == true

    #clothes
    "Clothes: Classic Cook":    PTItemData("Clothes Peppino", 300, ItemClassification.filler), #unused
    "Clothes: Unfunny Cook":    PTItemData("Clothes Peppino", 301, ItemClassification.filler),
    "Clothes: Money Green":     PTItemData("Clothes Peppino", 302, ItemClassification.filler),
    "Clothes: SAGE Blue":       PTItemData("Clothes Peppino", 303, ItemClassification.filler),
    "Clothes: Blood Red":       PTItemData("Clothes Peppino", 304, ItemClassification.filler),
    "Clothes: TV Purple":       PTItemData("Clothes Peppino", 305, ItemClassification.filler),
    "Clothes: Dark Cook":       PTItemData("Clothes Peppino", 306, ItemClassification.filler),
    "Clothes: Shitty Cook":     PTItemData("Clothes Peppino", 307, ItemClassification.filler),
    "Clothes: Golden God":      PTItemData("Clothes Peppino", 308, ItemClassification.filler),
    "Clothes: Garish Cook":     PTItemData("Clothes Peppino", 309, ItemClassification.filler),
    "Clothes: Mooney Orange":   PTItemData("Clothes Peppino", 310, ItemClassification.filler),
    "Clothes: Funny Polka":     PTItemData("Clothes Peppino", 311, ItemClassification.filler),
    "Clothes: Itchy Sweater":   PTItemData("Clothes Peppino", 312, ItemClassification.filler),
    "Clothes: Pizza Man":       PTItemData("Clothes Peppino", 313, ItemClassification.filler),
    "Clothes: Bowling Stripes": PTItemData("Clothes Peppino", 314, ItemClassification.filler),
    "Clothes: Goldemanne":      PTItemData("Clothes Peppino", 315, ItemClassification.filler),
    "Clothes: Bad Bones":       PTItemData("Clothes Peppino", 316, ItemClassification.filler),
    "Clothes: PP Shirt":        PTItemData("Clothes Peppino", 317, ItemClassification.filler),
    "Clothes: War Camo":        PTItemData("Clothes Peppino", 318, ItemClassification.filler),
    "Clothes: John Suit":       PTItemData("Clothes Peppino", 319, ItemClassification.filler),
    "Clothes: Noise":           PTItemData("Clothes Noise", 320, ItemClassification.filler), #unused
    "Clothes: Boise":           PTItemData("Clothes Noise", 321, ItemClassification.filler),
    "Clothes: Roise":           PTItemData("Clothes Noise", 322, ItemClassification.filler),
    "Clothes: Poise":           PTItemData("Clothes Noise", 323, ItemClassification.filler),
    "Clothes: Reverse":         PTItemData("Clothes Noise", 324, ItemClassification.filler),
    "Clothes: Critic":          PTItemData("Clothes Noise", 325, ItemClassification.filler),
    "Clothes: Outlaw":          PTItemData("Clothes Noise", 326, ItemClassification.filler),
    "Clothes: Anti-Doise":      PTItemData("Clothes Noise", 327, ItemClassification.filler),
    "Clothes: Flesh Eater":     PTItemData("Clothes Noise", 328, ItemClassification.filler),
    "Clothes: Super":           PTItemData("Clothes Noise", 329, ItemClassification.filler),
    "Clothes: Fast Porcupine":  PTItemData("Clothes Noise", 330, ItemClassification.filler),
    "Clothes: Feminine Side":   PTItemData("Clothes Noise", 331, ItemClassification.filler),
    "Clothes: The Real Doise":  PTItemData("Clothes Noise", 332, ItemClassification.filler),
    "Clothes: Forest Goblin":   PTItemData("Clothes Noise", 333, ItemClassification.filler),
    "Clothes: Racer":           PTItemData("Clothes Noise", 334, ItemClassification.filler),
    "Clothes: Comedian":        PTItemData("Clothes Noise", 335, ItemClassification.filler),
    "Clothes: Banana":          PTItemData("Clothes Noise", 336, ItemClassification.filler),
    "Clothes: Noise TV":        PTItemData("Clothes Noise", 337, ItemClassification.filler),
    "Clothes: Madman":          PTItemData("Clothes Noise", 338, ItemClassification.filler),
    "Clothes: Bubbly":          PTItemData("Clothes Noise", 339, ItemClassification.filler),
    "Clothes: Well Done":       PTItemData("Clothes Noise", 340, ItemClassification.filler),
    "Clothes: Granny Kisses":   PTItemData("Clothes Noise", 341, ItemClassification.filler),
    "Clothes: Tower Guy":       PTItemData("Clothes Noise", 342, ItemClassification.filler),
    "Clothes: Candy Wrapper":   PTItemData("Clothes Shared", 343, ItemClassification.filler),
    "Clothes: Bloodstained":    PTItemData("Clothes Shared", 344, ItemClassification.filler),
    "Clothes: Autumn":          PTItemData("Clothes Shared", 345, ItemClassification.filler),
    "Clothes: Pumpkin":         PTItemData("Clothes Shared", 346, ItemClassification.filler),
    "Clothes: Fur":             PTItemData("Clothes Shared", 347, ItemClassification.filler),
    "Clothes: Eyes":            PTItemData("Clothes Shared", 348, ItemClassification.filler),
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