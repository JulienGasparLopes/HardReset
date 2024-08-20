from typing import TYPE_CHECKING

from game_manager.graphic.menu.menu import Menu
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from game_manager.logic.uid_object import Uid  # TODO: logic leak
from vertyces.vertex import Vertex2f

from hard_reset.graphic.menu_component.inventory_exchange_gui import (
    InventoryExchangeGUI,
)
from hard_reset.graphic.menu_component.map_component import MapComponent

if TYPE_CHECKING:
    from hard_reset.graphic.graphic_manager import GraphicManager


class MenuMap(Menu):
    graphic_manager: "GraphicManager"

    _inventory_widget: InventoryExchangeGUI
    _map_component: MapComponent

    def __init__(self, graphic_manager: "GraphicManager", current_map_uid: Uid) -> None:
        super().__init__()
        self.graphic_manager = graphic_manager
        self.current_map_uid = current_map_uid

        self._inventory_widget = InventoryExchangeGUI(
            Vertex2f(500, 100), self.graphic_manager.message_manager
        )
        self._map_component = MapComponent(self)

        self.add_component(self._inventory_widget)
        self.add_component(self._map_component)

    def show_inventory(self, chest_uid: Uid) -> None:
        self._inventory_widget.set_entities(
            self.current_map_uid, chest_uid, self.graphic_manager.player_uid
        )
        self._inventory_widget.show(visible=True)

    def move_items(
        self, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None:
        self.graphic_manager.message_manager.move_inventory_items(
            self.current_map_uid, from_uid, to_uid, item_name, quantity
        )

    def render(self, delta_ns: float, renderer: Renderer) -> None:
        self.graphic_manager.window.set_title(f"FPS: {self.graphic_manager.fps}")

        current_map_info = self.graphic_manager.message_manager.get_map_info(
            self.current_map_uid
        )
        self._map_component.update_map_info(current_map_info)

        if self.graphic_manager.keyboard.consume_key("a"):
            self._inventory_widget.show(False)

        direction = Vertex2f(0, 0)
        if self.graphic_manager.keyboard.is_pressed("q"):
            direction = direction.translated(Vertex2f(-1, 0))
        if self.graphic_manager.keyboard.is_pressed("d"):
            direction = direction.translated(Vertex2f(1, 0))
        if self.graphic_manager.keyboard.is_pressed("z"):
            direction = direction.translated(Vertex2f(0, -1))
        if self.graphic_manager.keyboard.is_pressed("s"):
            direction = direction.translated(Vertex2f(0, 1))

        self.graphic_manager.message_manager.set_entity_direction(
            self.current_map_uid, self.graphic_manager.player_uid, direction
        )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None: ...
