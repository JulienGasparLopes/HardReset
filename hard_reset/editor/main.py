from game_manager.tk.utils import initialize_tk_context

from hard_reset.editor.editor_manager import EditorManager


def main() -> None:
    window, renderer, mouse, keyboard = initialize_tk_context()
    editor_manager = EditorManager(window, renderer, keyboard, mouse)

    print("Starting editor manager thread")
    editor_manager.start()


if __name__ == "__main__":
    main()
