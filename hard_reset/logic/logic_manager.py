from uuid import UUID

from game_manager.logic.logic_manager import BaseLogicManager
from game_manager.logic.map.tile import TILE_SIZE
from game_manager.logic.map.tiled_map import TiledMap
from game_manager.logic.uid_object import Uid
from game_manager.storage.storage_manager import StorageManager
from vertyces.vertex import Vertex2f

from hard_reset.logic.entities import Player
from hard_reset.logic.item.item import WOODEN_PLANK
from hard_reset.logic.logic_storage_manager import LogicStorageManager
from hard_reset.logic.map.maps import Map1, Map2
from hard_reset.messaging.messaging import MessageManagerLogic


class LogicManager(BaseLogicManager[MessageManagerLogic, TiledMap]):
    _storage_manager: StorageManager

    def __init__(self) -> None:
        super().__init__()
        self._storage_manager = LogicStorageManager("save/logic")

        self.add_map(Map1())
        self.add_map(Map2())

    def update(self, delta_ns: float) -> None: ...

    def save(self) -> None:
        for map in self._maps.values():
            for entity in map._entities.values():
                if isinstance(entity, Player):
                    self._storage_manager.store_object(entity)

    def dispose(self) -> None:
        print("Saving")
        self.save()
        print("Disposing Logic Manager")
        self.message_manager.application_stopped()

    def on_connect(self) -> None:
        pass

    def on_disconnect(self) -> None: ...

    def on_player_connect(self, player_uid: UUID | None) -> tuple[Player, Uid]:
        if player_uid:
            player = self._storage_manager.retrieve_object(Player, player_uid)
            assert player
        else:
            player = Player(Vertex2f(1 * TILE_SIZE, 1 * TILE_SIZE))

        current_map = list(self._maps.values())[0]
        current_map.add_entity(player)
        player._inventory.add_item(WOODEN_PLANK, 5)

        return player, current_map.uid
