from dataclasses import dataclass


@dataclass
class Item:
    name: str


BOTTLE = Item("Bottle")
KEY = Item("Key")

WOODEN_PLANK = Item("Wooden Plank")
WOODEN_STICK = Item("Wooden Stick")

CRAFTING_BENCH_ITEM = Item("Crafting Bench")


ITEMS = [
    BOTTLE,
    KEY,
    WOODEN_PLANK,
    WOODEN_STICK,
    CRAFTING_BENCH_ITEM,
]
NAME_TO_ITEM = {item.name: item for item in ITEMS}
