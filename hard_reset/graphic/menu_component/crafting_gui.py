from typing import Callable

from game_manager.graphic.component.button import Button
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from game_manager.logic.uid_object import Uid
from vertyces.utils import colors
from vertyces.vertex.vertex2f import Vertex2f

from hard_reset.graphic.menu_component.craft_selector_widget import CraftSelectorWidget
from hard_reset.graphic.menu_component.inventory_widget import InventoryWidget
from hard_reset.messaging.messaging import MessageManagerGraphic


class CraftButton(Button):
    def __init__(self, position: Vertex2f, action_callback: Callable[[], None]) -> None:
        super().__init__(position, Vertex2f(50, 50), action_callback)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.ORANGE)
        renderer.draw_text(Vertex2f(2, 2), "Craft", colors.BLACK)


class CraftingGUI(GraphicalComponent):
    _message_manager: MessageManagerGraphic
    _player_uid: Uid
    _map_uid: Uid

    _selected_recipe: str | None = None

    _craft_selector_widget: CraftSelectorWidget
    _inventory_widget: InventoryWidget

    def __init__(
        self,
        position: Vertex2f,
        message_manager: MessageManagerGraphic,
        player_uid: Uid,
    ) -> None:
        super().__init__(position, Vertex2f(400, 400), z_index=20, visible=False)
        self._message_manager = message_manager
        self._player_uid = player_uid

        crafting_recipes = self._message_manager.get_crafting_recipes()
        self._craft_selector_widget = CraftSelectorWidget(
            Vertex2f(125, 0), crafting_recipes, self._select_recipe
        )
        self.add_component(self._craft_selector_widget)
        self.add_component(CraftButton(Vertex2f(300, 350), self._craft_item))
        self._inventory_widget = InventoryWidget(
            Vertex2f(0, 0), "Player Inventory", lambda _: None
        )
        self.add_component(self._inventory_widget)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.PINK)

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False

    def show_crating_gui(self, map_uid: Uid) -> None:
        self._map_uid = map_uid

        player_inventory = self._message_manager.get_inventory(
            map_uid, self._player_uid
        )
        self._inventory_widget.set_inventory(player_inventory)
        self._craft_selector_widget.update_inventory(player_inventory)

        self.show(True)

    def _select_recipe(self, recipe_name: str) -> None:
        self._selected_recipe = recipe_name

    def _craft_item(self) -> None:
        if self._selected_recipe is not None:
            self._message_manager.craft_item(
                self._map_uid, self._player_uid, self._selected_recipe
            )
            self.show_crating_gui(self._map_uid)
