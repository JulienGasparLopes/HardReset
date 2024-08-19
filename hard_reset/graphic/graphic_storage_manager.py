from dataclasses import dataclass
from uuid import UUID

from game_manager.fs_storage.fs_storage_manager import FileSystemStorageManager
from game_manager.logic.uid_object import Uid


@dataclass
class PlayerInfoStore:
    player_uid: Uid

    _uid: Uid = UUID("00000000-0000-0000-0000-000000000000")


class GraphicStorageManager(FileSystemStorageManager):

    def _unparse_object(self, object_to_unparse: object) -> dict[object, object]:
        if isinstance(object_to_unparse, PlayerInfoStore):
            return {
                "type": "PlayerInfoStore",
                "player_uid": str(object_to_unparse.player_uid),
            }
        else:
            raise ValueError(
                f"Object of type {type(object_to_unparse)} is not storable"
            )

    def _parse_object(self, object_data: dict[object, object]) -> object:
        object_type = object_data["type"]
        if object_type == "PlayerInfoStore":
            return PlayerInfoStore(UUID(object_data["player_uid"]))  # type: ignore[arg-type]
        else:
            raise ValueError(f"Object with data {object_data} is not parsable")
