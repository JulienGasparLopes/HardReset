from game_manager.graphic.graphic_manager import BaseGraphicManager
from game_manager.graphic.renderer import Renderer
from game_manager.graphic.window import Window
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse

from hard_reset.editor.editor_menu import EditorMenu


class StandaloneManager: ...


class EditorManager(BaseGraphicManager[StandaloneManager]):

    def __init__(
        self, window: Window, renderer: Renderer, keyboard: Keyboard, mouse: Mouse
    ) -> None:
        super().__init__(window, renderer, keyboard, mouse)
        window.set_on_close_callback(lambda: self.stop())
        self.set_current_menu(EditorMenu(self.mouse, self.keyboard))

    def dispose(self) -> None:
        print("Disposing Editor Manager")
        self.window.close()

    def on_connect(self) -> None: ...

    def on_disconnect(self) -> None: ...
