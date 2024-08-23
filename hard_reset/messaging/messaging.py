from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from game_manager.logic.entity.entity_moveable import EntityMoveable
from game_manager.logic.uid_object import Uid
from game_manager.messaging.message_manager import (
    MessageManager,
    MessageManagerProtocol,
)
from vertyces.vertex import Vertex2f

from hard_reset.logic.entities import Chest, Door, WithInventory
from hard_reset.logic.item.crafting_recipe import (
    CRAFTING_RECIPES,
    RESULT_NAME_TO_RECIPE,
)
from hard_reset.logic.item.item import NAME_TO_ITEM
from hard_reset.logic.map.maps import BaseMap

if TYPE_CHECKING:
    from hard_reset.graphic.graphic_manager import GraphicManager
    from hard_reset.logic.logic_manager import LogicManager


@dataclass
class EntityInfoPacket:
    type_name: str
    uid: Uid
    position: Vertex2f


@dataclass
class EntityDoorInfoPacket(EntityInfoPacket):
    # TODO: may be removed when direction is added to EntityInfoPacket
    dimensions: Vertex2f
    map_travel_uid: Uid


@dataclass
class PlayerInfoPacket(EntityInfoPacket):
    current_map_uid: Uid


@dataclass
class MapInfoPacket:
    width_in_tiles: int
    height_in_tiles: int
    width: int
    height: int
    tiles: dict[tuple[int, int], bool]
    entities: dict[Uid, EntityInfoPacket]


class MessageManagerLogic(ABC, MessageManagerProtocol):
    @abstractmethod
    def application_stopped(self) -> None: ...


class MessageManagerGraphic(ABC, MessageManagerProtocol):
    @abstractmethod
    def connect_as_player(self, player_uid: Uid | None) -> PlayerInfoPacket: ...

    @abstractmethod
    def get_inventory(self, map_uid: Uid, entity_uid: Uid) -> dict[str, int]: ...

    @abstractmethod
    def get_crafting_recipes(self) -> dict[str, dict[str, int]]: ...

    @abstractmethod
    def craft_item(
        self, map_uid: Uid, entity_uid: Uid, recipe_name: str
    ) -> dict[str, int]: ...

    @abstractmethod
    def move_inventory_items(
        self, map_uid: Uid, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None: ...

    @abstractmethod
    def get_map_info(self, map_uid: Uid) -> MapInfoPacket: ...

    @abstractmethod
    def use_map_travel(
        self, entity_uid: Uid, map_uid: Uid, map_travel_uid: Uid
    ) -> Uid: ...

    @abstractmethod
    def set_entity_direction(
        self, map_uid: Uid, entity_uid: Uid, direction: Vertex2f
    ) -> None: ...

    @abstractmethod
    def stop_application(self) -> None: ...


class TestMessageManager(MessageManager, MessageManagerLogic, MessageManagerGraphic):
    logic_manager: "LogicManager"
    graphic_manager: "GraphicManager"

    def __init__(
        self, logic_manager: "LogicManager", graphic_manager: "GraphicManager"
    ) -> None:
        self.logic_manager = logic_manager
        self.graphic_manager = graphic_manager
        super().__init__(logic_manager, graphic_manager)

    def connect_as_player(self, player_uid: Uid | None) -> PlayerInfoPacket:
        player, map_uid = self.logic_manager.on_player_connect(player_uid)

        return PlayerInfoPacket(
            type_name="Player",
            uid=player.uid,
            position=player.position,
            current_map_uid=map_uid,
        )

    def get_map_info(self, map_uid: Uid) -> MapInfoPacket:
        current_map = self.logic_manager.get_map(map_uid)
        current_map = cast(BaseMap, current_map)
        assert current_map is not None
        tiles_data = {}
        for i, row in enumerate(current_map._tiles):
            for j, tile in enumerate(row):
                tiles_data[(j, i)] = tile.walkable

        entities_data: dict[Uid, EntityInfoPacket] = {}
        for uid, entity in current_map._entities.items():
            if isinstance(entity, Door):
                entities_data[uid] = EntityDoorInfoPacket(
                    type_name=entity.__class__.__name__,
                    uid=entity.uid,
                    position=entity.bounds.position,
                    dimensions=entity.bounds.dimensions,
                    map_travel_uid=entity._map_travel_uid,
                )
            else:
                entities_data[uid] = EntityInfoPacket(
                    type_name=entity.__class__.__name__,
                    uid=entity.uid,
                    position=entity.bounds.position,
                )

        return MapInfoPacket(
            width_in_tiles=current_map.width_in_tiles,
            height_in_tiles=current_map.height_in_tiles,
            width=current_map.width,
            height=current_map.height,
            tiles=tiles_data,
            entities=entities_data,
        )

    def use_map_travel(self, entity_uid: Uid, map_uid: Uid, map_travel_uid: Uid) -> Uid:
        current_map = self.logic_manager.get_map(map_uid)
        assert current_map is not None

        entity = current_map.get_entity(entity_uid)
        assert entity is not None

        current_map = cast(BaseMap, current_map)
        map_travel = current_map.get_map_travel(map_travel_uid)
        next_map_uid, spawn_point_uid = map_travel.destination
        next_map = self.logic_manager.get_map(next_map_uid)
        assert next_map is not None

        next_map = cast(BaseMap, next_map)
        spawn_point = next_map.get_spawn_point(spawn_point_uid)

        current_map.remove_entity(entity_uid)
        entity.bounds = entity.bounds.at_position(spawn_point._position)
        next_map.add_entity(entity)

        return next_map.uid

    def get_inventory(self, map_uid: Uid, entity_uid: Uid) -> dict[str, int]:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        entity = map.get_entity(entity_uid)
        assert entity is not None
        chest = cast("Chest", entity)
        return chest._inventory._items

    def get_crafting_recipes(self) -> dict[str, dict[str, int]]:
        recipes = {}
        for recipe in CRAFTING_RECIPES:
            recipes[recipe._result.item.name] = {
                ingredient.item.name: ingredient.quantity
                for ingredient in recipe._ingredients
            }
        return recipes

    def craft_item(
        self, map_uid: Uid, entity_uid: Uid, recipe_name: str
    ) -> dict[str, int]:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        entity = map.get_entity(entity_uid)
        assert entity is not None
        entity_with_inventory = cast(WithInventory, entity)

        recipe = RESULT_NAME_TO_RECIPE[recipe_name]
        may_craft = recipe.can_craft(entity_with_inventory._inventory._items)
        if may_craft:
            for ingredient in recipe._ingredients:
                entity_with_inventory._inventory.remove_item(
                    ingredient.item, ingredient.quantity
                )
            entity_with_inventory._inventory.add_item(
                recipe._result.item, recipe._result.quantity
            )

        return entity_with_inventory._inventory._items

    def move_inventory_items(
        self, map_uid: Uid, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        from_entity = cast(WithInventory, map.get_entity(from_uid))
        assert from_entity is not None
        to_entity = cast(WithInventory, map.get_entity(to_uid))
        assert to_entity is not None
        from_entity._inventory.remove_item(NAME_TO_ITEM[item_name], quantity)
        to_entity._inventory.add_item(NAME_TO_ITEM[item_name], quantity)

    def set_entity_direction(
        self, map_uid: Uid, entity_uid: Uid, direction: Vertex2f
    ) -> None:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        entity = map.get_entity(entity_uid)
        assert entity is not None and isinstance(entity, EntityMoveable), entity
        entity.direction = direction.unit_vertex.multiplied(entity.speed)

    def application_stopped(self) -> None:
        self.graphic_manager.stop()

    def stop_application(self) -> None:
        self.logic_manager.stop()
