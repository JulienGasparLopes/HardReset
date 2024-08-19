from uuid import UUID

from game_manager.graphic.graphic_manager import GraphicManager as BaseGraphicManager
from game_manager.graphic.renderer import Renderer
from game_manager.graphic.window import Window
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse
from game_manager.logic.uid_object import Uid  # TODO: logic leak
from game_manager.storage.storage_manager import StorageManager

from hard_reset.graphic.graphic_storage_manager import (
    GraphicStorageManager,
    PlayerInfoStore,
)
from hard_reset.graphic.menu_map import MenuMap
from hard_reset.messaging.messaging import MessageManagerGraphic

TILE_SIZE = 40


class GraphicManager(BaseGraphicManager[MessageManagerGraphic]):
    player_uid: Uid

    _storage_manager: StorageManager

    def __init__(
        self, window: Window, renderer: Renderer, keyboard: Keyboard, mouse: Mouse
    ):
        super().__init__(window, renderer, keyboard, mouse)
        window.set_on_close_callback(lambda: self.message_manager.stop_application())
        self._storage_manager = GraphicStorageManager("save/graphic")

    def dispose(self) -> None:
        print("Disposing Graphic Manager")
        self._storage_manager.store_object(PlayerInfoStore(self.player_uid))
        self.window.close()

    def on_connect(self) -> None:
        stored_player_info = self._storage_manager.retrieve_object(
            PlayerInfoStore, UUID("00000000-0000-0000-0000-000000000000")
        )
        player_info = self.message_manager.connect_as_player(
            stored_player_info.player_uid if stored_player_info else None
        )
        self.player_uid = player_info.uid

        self.set_current_menu(MenuMap(self, player_info.current_map_uid))

    def on_disconnect(self) -> None: ...
