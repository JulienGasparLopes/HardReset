from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.menu.menu import Menu
from game_manager.graphic.renderer import Renderer
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse, MouseButton
from vertyces.vertex import Vertex2f

from hard_reset.editor.map_gui import MapGui
from hard_reset.editor.tile_selector_gui import TileSelectorGui


class TileComponent(GraphicalComponent):

    def render(self, renderer: Renderer) -> None: ...

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False


class EditorMenu(Menu):
    _tile_selector: TileSelectorGui
    _map_gui: MapGui

    _keyboard: Keyboard

    def __init__(self, mouse: Mouse, keyboard: Keyboard) -> None:
        super().__init__()
        self._keyboard = keyboard

        self._tile_selector = TileSelectorGui()
        self.add_component(self._tile_selector)

        self._map_gui = MapGui(self._tile_selector, mouse)
        self.add_component(self._map_gui)

    def render(self, delta_ns: float, renderer: Renderer) -> None:
        direction = Vertex2f(0, 0)
        if self._keyboard.is_pressed("q"):
            direction = direction.translated(Vertex2f(1, 0))
        if self._keyboard.is_pressed("d"):
            direction = direction.translated(Vertex2f(-1, 0))
        if self._keyboard.is_pressed("z"):
            direction = direction.translated(Vertex2f(0, 1))
        if self._keyboard.is_pressed("s"):
            direction = direction.translated(Vertex2f(0, -1))

        self._map_gui.bounds = self._map_gui.bounds.translated(
            direction.multiplied(delta_ns / 1e9 * 200)
        )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None: ...
