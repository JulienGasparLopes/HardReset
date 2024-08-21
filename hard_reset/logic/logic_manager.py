from uuid import UUID

from game_manager.logic.logic_manager import BaseLogicManager
from game_manager.logic.map.tile import TILE_SIZE, Tile
from game_manager.logic.map.tiled_map import TiledMap
from game_manager.logic.uid_object import Uid
from game_manager.storage.storage_manager import StorageManager
from vertyces.vertex import Vertex2f

from hard_reset.logic.entities import Chest, Player
from hard_reset.logic.item.item import BOTTLE, KEY, WOODEN_PLANK
from hard_reset.logic.logic_storage_manager import LogicStorageManager
from hard_reset.messaging.messaging import MessageManagerLogic

GROUND_TILE = Tile(walkable=True)
WALL_TILE = Tile(walkable=False)


class DefaultTiledMap(TiledMap):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, default_tile=GROUND_TILE)
        for y in range(height):
            self._tiles[y][0] = WALL_TILE
            self._tiles[y][width - 1] = WALL_TILE
        for x in range(width):
            self._tiles[0][x] = WALL_TILE
            self._tiles[height - 1][x] = WALL_TILE

    def update(self, delta_time: float) -> None: ...


class LogicManager(BaseLogicManager[MessageManagerLogic, TiledMap]):
    _storage_manager: StorageManager

    def __init__(self) -> None:
        super().__init__()
        self._storage_manager = LogicStorageManager("save/logic")

        map1 = DefaultTiledMap(11, 11)
        map1._tiles[5][5] = WALL_TILE

        chest1 = Chest(Vertex2f(1 * TILE_SIZE, 4 * TILE_SIZE))
        chest1._inventory.add_item(BOTTLE, 1)
        chest1._inventory.add_item(KEY, 3)
        chest1._inventory.add_item(WOODEN_PLANK, 3)
        map1.add_entity(chest1)

        chest2 = Chest(Vertex2f(2 * TILE_SIZE, 6 * TILE_SIZE))
        chest2._inventory.add_item(KEY, 7)
        map1.add_entity(chest2)

        map2 = DefaultTiledMap(10, 12)
        map2._tiles[3][4] = WALL_TILE

        self.add_map(map1)
        self.add_map(map2)

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
