from typing import Callable

import vertyces.utils.colors as colors
from game_manager.graphic.component.button import Button
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from vertyces.vertex import Vertex2f


class InventoryItemButton(Button):
    _item_name: str
    _item_amount: int
    _move_items_callback: Callable[[str], None]

    def __init__(
        self,
        position: Vertex2f,
        item_name: str,
        item_amount: int,
        _move_items_callback: Callable[[str], None],
    ) -> None:
        super().__init__(position, Vertex2f(90, 20), self._move_items)
        self._item_name = item_name
        self._item_amount = item_amount
        self._move_items_callback = _move_items_callback

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.ORANGE)
        renderer.draw_text(
            Vertex2f(2, 2),
            f"{self._item_name} ({self._item_amount})",
            colors.BLACK,
        )

    def _move_items(self) -> None:
        self._move_items_callback(self._item_name)


class InventoryWidget(GraphicalComponent):
    _name: str
    _item_click_callback: Callable[[str], None]

    def __init__(
        self,
        position: Vertex2f,
        name: str,
        item_click_callback: Callable[[str], None],
    ) -> None:
        super().__init__(position, Vertex2f(125, 400))
        self._name = name
        self._item_click_callback = item_click_callback

    def set_inventory(self, inventory: dict[str, int]) -> None:
        self.clear_components()
        for idx, (item_name, item_count) in enumerate(inventory.items()):
            self.add_component(
                InventoryItemButton(
                    Vertex2f(10, idx * 22 + 30),
                    item_name,
                    item_count,
                    self._item_click_callback,
                )
            )

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.GREEN)
        renderer.draw_text(Vertex2f(10, 10), self._name, colors.BLACK)

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False
