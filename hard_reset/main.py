from game_manager.tk.utils import initialize_tk_context

from hard_reset.graphic.graphic_manager import GraphicManager
from hard_reset.logic.logic_manager import LogicManager
from hard_reset.messaging.messaging import TestMessageManager


def main() -> None:
    logic_manager = LogicManager()

    window, renderer, mouse, keyboard = initialize_tk_context()
    graphic_manager = GraphicManager(window, renderer, keyboard, mouse)

    TestMessageManager(logic_manager, graphic_manager)

    print("Starting logic manager thread")
    logic_manager.start()

    print("Starting graphic manager thread")
    graphic_manager.start()


if __name__ == "__main__":
    main()


"""
TODO List:
- Save inventories (and map)
- Add player stats and crafting requirements
- Add Xp and leveling ? 

- Improve abstraction of keyboard.py
- Map switch logic (portal ?)
- Create common folder for shared code (such as Uid)
"""
