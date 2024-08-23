from typing import TypeAlias

from game_manager.logic.uid_object import Uid, UIDObject
from vertyces.vertex import Vertex2f


class SpawnPoint(UIDObject):
    _position: Vertex2f

    def __init__(self, position: Vertex2f, uid: Uid) -> None:
        self._position = position
        self._uid = uid


SpawnPointId: TypeAlias = tuple[Uid, Uid]


class MapTravel(UIDObject):
    _destination: SpawnPointId

    def __init__(self, destination: SpawnPointId) -> None:
        self._destination = destination

    @property
    def destination(self) -> SpawnPointId:
        return self._destination
