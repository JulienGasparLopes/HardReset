import vertyces.utils.colors as colors
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from game_manager.logic.uid_object import Uid  # TODO: logic leak
from vertyces.vertex.vertex2f import Vertex2f

from hard_reset.graphic.menu_component.inventory_widget import InventoryWidget
from hard_reset.messaging.messaging import MessageManagerGraphic


class InventoryExchangeGUI(GraphicalComponent):
    _message_manager: MessageManagerGraphic

    _map_uid: Uid
    _left_entity_uid: Uid
    _right_entity_uid: Uid

    def __init__(
        self, position: Vertex2f, message_manager: MessageManagerGraphic
    ) -> None:
        super().__init__(position, Vertex2f(250, 400), visible=False, z_index=10)
        self._message_manager = message_manager

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.YELLOW)

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False

    def set_entities(
        self, map_uid: Uid, left_entity_uid: Uid, right_entity_uid: Uid
    ) -> None:
        self._map_uid = map_uid
        self._left_entity_uid = left_entity_uid
        self._right_entity_uid = right_entity_uid
        self._update_components()

    def _update_components(self) -> None:
        self.clear_components()
        items_left = self._message_manager.get_inventory(
            self._map_uid, self._left_entity_uid
        )
        items_right = self._message_manager.get_inventory(
            self._map_uid, self._right_entity_uid
        )
        self.add_component(
            InventoryWidget(
                Vertex2f(0, 0),
                "Left",
                items_left,
                lambda name: self._move_items(
                    self._left_entity_uid, self._right_entity_uid, name, 1
                ),
            )
        )
        self.add_component(
            InventoryWidget(
                Vertex2f(125, 0),
                "Right",
                items_right,
                lambda name: self._move_items(
                    self._right_entity_uid, self._left_entity_uid, name, 1
                ),
            )
        )

    def _move_items(
        self, from_uid: Uid, to_uid: Uid, item_name: str, quantity: int
    ) -> None:
        self._message_manager.move_inventory_items(
            self._map_uid, from_uid, to_uid, item_name, quantity
        )
        self._update_components()
