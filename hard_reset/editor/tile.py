from enum import Enum

from vertyces.vertex import Vertex3f

TILE_SIZE = 40


class Tile(Enum):
    VOID = "void", Vertex3f(0, 0, 0)
    WALL = "wall", Vertex3f(255, 0, 0)
    GROUND = "ground", Vertex3f(0, 0, 255)
    CARPET = "carpet", Vertex3f(0, 255, 255)

    def __init__(self, name: str, color: Vertex3f) -> None:
        self._name = name
        self._color = color
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> Vertex3f:
        return self._color
