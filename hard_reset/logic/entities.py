from typing import Protocol

from game_manager.logic.entity.entity import Entity
from game_manager.logic.entity.entity_moveable import EntityMoveable
from game_manager.logic.map.tile import TILE_SIZE
from vertyces.vertex import Vertex2f

from hard_reset.logic.item.item import Item

DEFAULT_DIMENSION = Vertex2f(TILE_SIZE, TILE_SIZE)


class Inventory:
    _items: dict[str, int]

    def __init__(self) -> None:
        self._items = {}

    def add_item(self, item: Item, quantity: int) -> None:
        self._items[item.name] = self._items.get(item.name, 0) + quantity

    def remove_item(self, item: Item, quantity: int) -> None:
        if item.name not in self._items:
            return
        self._items[item.name] -= quantity
        if self._items[item.name] == 0:
            del self._items[item.name]


class WithInventory(Protocol):
    _inventory: Inventory


class Chest(Entity, WithInventory):

    def __init__(self, position: Vertex2f) -> None:
        super().__init__(position, DEFAULT_DIMENSION)
        self._inventory = Inventory()

    def update(self, delta_time: float) -> None: ...


class Player(EntityMoveable, WithInventory):

    def __init__(self, position: Vertex2f) -> None:
        super().__init__(position, Vertex2f(35, 35))
        self.speed = 1.4
        self.direction = Vertex2f(self.speed, 0)
        self._inventory = Inventory()

    def update(self, delta_time: float) -> None: ...
