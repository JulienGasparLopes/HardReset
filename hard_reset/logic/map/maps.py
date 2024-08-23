from abc import ABC
from uuid import UUID

from game_manager.logic.map.tiled_map import TILE_SIZE, TiledMap
from game_manager.logic.uid_object import Uid
from vertyces.vertex import Vertex2f

from hard_reset.logic.entities import Chest, Door
from hard_reset.logic.item.item import BOTTLE, KEY, WOODEN_PLANK
from hard_reset.logic.map.map_travel import MapTravel, SpawnPoint
from hard_reset.logic.map.tiles import GROUND_TILE, WALL_TILE


class BaseMap(TiledMap, ABC):
    _spawn_points: dict[Uid, SpawnPoint]
    _map_travels: dict[Uid, MapTravel]

    def __init__(self, width_in_tiles: int, height_in_tiles: int) -> None:
        super().__init__(width_in_tiles, height_in_tiles, default_tile=GROUND_TILE)
        self._spawn_points = {}
        self._map_travels = {}

        for y in range(self.height_in_tiles):
            self.set_tile(0, y, WALL_TILE)
            self.set_tile(self.width_in_tiles - 1, y, WALL_TILE)
        for x in range(self.width_in_tiles):
            self.set_tile(x, 0, WALL_TILE)
            self.set_tile(x, self.height_in_tiles - 1, WALL_TILE)

    def update(self, delta_time: float) -> None: ...

    def add_spawn_point(self, spawn_point: SpawnPoint) -> None:
        self._spawn_points[spawn_point.uid] = spawn_point

    def remove_spawn_point(self, spawn_point: SpawnPoint) -> SpawnPoint:
        return self._spawn_points.pop(spawn_point.uid)

    def get_spawn_point(self, uid: Uid) -> SpawnPoint:
        return self._spawn_points[uid]

    def add_map_travel(self, map_travel: MapTravel) -> None:
        self._map_travels[map_travel.uid] = map_travel

    def remove_map_travel(self, map_travel: MapTravel) -> MapTravel:
        return self._map_travels.pop(map_travel.uid)

    def get_map_travel(self, uid: Uid) -> MapTravel:
        return self._map_travels[uid]


class Map1(BaseMap):
    def __init__(self) -> None:
        super().__init__(11, 12)
        self._uid = UUID("10000000-0000-0000-0000-000000000001")

        chest1 = Chest(Vertex2f(1 * TILE_SIZE, 4 * TILE_SIZE))
        chest1._inventory.add_item(BOTTLE, 1)
        chest1._inventory.add_item(KEY, 3)
        chest1._inventory.add_item(WOODEN_PLANK, 3)
        self.add_entity(chest1)

        chest2 = Chest(Vertex2f(2 * TILE_SIZE, 6 * TILE_SIZE))
        chest2._inventory.add_item(KEY, 7)
        self.add_entity(chest2)

        spawn_point = SpawnPoint(
            Vertex2f(6 * TILE_SIZE, 1 * TILE_SIZE),
            UUID("12000000-0000-0000-0000-000000000001"),
        )
        self.add_spawn_point(spawn_point)
        map_travel = MapTravel(
            (
                UUID("10000000-0000-0000-0000-000000000002"),
                UUID("12000000-0000-0000-0000-000000000002"),
            ),
        )
        self.add_map_travel(map_travel)
        door = Door(Vertex2f(0, 6 * TILE_SIZE), map_travel.uid)
        self.add_entity(door)


class Map2(BaseMap):
    def __init__(self) -> None:
        super().__init__(8, 15)
        self._uid = UUID("10000000-0000-0000-0000-000000000002")

        spawn_point = SpawnPoint(
            Vertex2f(1 * TILE_SIZE, 5 * TILE_SIZE),
            UUID("12000000-0000-0000-0000-000000000002"),
        )
        self.add_spawn_point(spawn_point)
        map_travel = MapTravel(
            (
                UUID("10000000-0000-0000-0000-000000000001"),
                UUID("12000000-0000-0000-0000-000000000001"),
            ),
        )
        self.add_map_travel(map_travel)

        door = Door(Vertex2f(0, 6 * TILE_SIZE), map_travel.uid)
        self.add_entity(door)

        chest1 = Chest(Vertex2f(3 * TILE_SIZE, 4 * TILE_SIZE))
        chest1._inventory.add_item(KEY, 66)
        self.add_entity(chest1)
