from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from game_manager.logic.entity.entity_moveable import EntityMoveable
from game_manager.logic.uid_object import Uid
from game_manager.messaging.message_manager import (
    MessageManager,
    MessageManagerProtocol,
)
from vertyces.vertex.vertex2f import Vertex2f

from hard_reset.logic.entities import NAME_TO_TIME, Chest, WithInventory

if TYPE_CHECKING:
    from hard_reset.graphic.graphic_manager import GraphicManager
    from hard_reset.logic.logic_manager import TestLogicManager


@dataclass
class EntityInfoPacket:
    type_name: str
    uid: Uid
    position: Vertex2f


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
    def move_inventory_items(
        self, map_uid: Uid, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None: ...

    @abstractmethod
    def get_map_info(self, map_uid: Uid) -> MapInfoPacket: ...

    @abstractmethod
    def set_entity_direction(
        self, map_uid: Uid, entity_uid: Uid, direction: Vertex2f
    ) -> None: ...

    @abstractmethod
    def stop_application(self) -> None: ...


class TestMessageManager(MessageManager, MessageManagerLogic, MessageManagerGraphic):
    logic_manager: "TestLogicManager"
    graphic_manager: "GraphicManager"

    def __init__(
        self, logic_manager: "TestLogicManager", graphic_manager: "GraphicManager"
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
        assert current_map is not None
        tiles_data = {}
        for i, row in enumerate(current_map._tiles):
            for j, tile in enumerate(row):
                tiles_data[(i, j)] = tile.walkable

        entities_data: dict[Uid, EntityInfoPacket] = {}
        for uid, entity in current_map._entities.items():
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

    def get_inventory(self, map_uid: Uid, entity_uid: Uid) -> dict[str, int]:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        entity = map.get_entity(entity_uid)
        assert entity is not None
        chest = cast("Chest", entity)
        return chest._inventory._items

    def move_inventory_items(
        self, map_uid: Uid, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None:
        map = self.logic_manager.get_map(map_uid)
        assert map is not None
        from_entity = cast(WithInventory, map.get_entity(from_uid))
        assert from_entity is not None
        to_entity = cast(WithInventory, map.get_entity(to_uid))
        assert to_entity is not None
        from_entity._inventory.remove_item(NAME_TO_TIME[item_name], quantity)
        to_entity._inventory.add_item(NAME_TO_TIME[item_name], quantity)

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
