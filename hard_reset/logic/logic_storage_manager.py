from game_manager.fs_storage.fs_storage_manager import FileSystemStorageManager
from vertyces.vertex.vertex2f import Vertex2f

from hard_reset.logic.entities import Player


class LogicStorageManager(FileSystemStorageManager):

    def _unparse_object(self, object_to_unparse: object) -> dict[object, object]:
        if isinstance(object_to_unparse, Vertex2f):
            return {
                "type": "Vertex2f",
                "x": object_to_unparse.x,
                "y": object_to_unparse.y,
            }
        if isinstance(object_to_unparse, Player):
            return {
                "type": "Player",
                "position": self._unparse_object(object_to_unparse.position),
            }
        else:
            raise ValueError(
                f"Object of type {type(object_to_unparse)} is not storable"
            )

    def _parse_object(self, object_data: dict[object, object]) -> object:
        object_type = object_data["type"]
        if object_type == "Vertex2f":
            return Vertex2f(object_data["x"], object_data["y"])  # type: ignore[arg-type]
        elif object_type == "Player":
            return Player(self._parse_object(object_data["position"]))  # type: ignore[arg-type]
        else:
            raise ValueError(f"Object with data {object_data} is not parsable")
