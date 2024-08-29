from typing import Callable

import vertyces.utils.colors as colors
from game_manager.graphic.component.button import Button
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from vertyces.vertex import Vertex2f
import vertyces.utils.colors as colors

from hard_reset.editor.tile import TILE_SIZE, Tile

name_to_entity_info = {
    "chest": [Vertex2f(1, 1), colors.CYAN],
}


class EntityButton(Button):
    _tile: Tile

    def __init__(
        self, position: Vertex2f, tile: Tile, on_select_callback: Callable[[Tile], None]
    ) -> None:
        super().__init__(
            position,
            Vertex2f(TILE_SIZE, TILE_SIZE),
            lambda: on_select_callback(self._tile),
        )
        self._tile = tile

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, self._tile.color)


class EntitySelectorGui(GraphicalComponent):
    _selected_entity_name: str

    def __init__(self) -> None:
        super().__init__(
            Vertex2f(420, 20), Vertex2f(120, 500), z_index=10, visible=True
        )
        self._selected_tile = Tile.GROUND
        for idx, tile in enumerate(Tile):
            self.add_component(
                EntityButton(
                    Vertex2f(10, 10 + idx * 50),
                    tile,
                    lambda tile: setattr(self, "_selected_tile", tile),
                )
            )

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), self.bounds.dimensions, colors.LIGHT_GREY)
        renderer.draw_rect(
            Vertex2f(10, 380),
            Vertex2f(10 + TILE_SIZE, 380 + TILE_SIZE),
            self._selected_tile.color,
            z_index=2,
        )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return True
