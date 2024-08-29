from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import Mouse, MouseButton
from vertyces.matrix.matrix import Matrix
from vertyces.vertex import Vertex2f, Vertex3f

from hard_reset.editor.tile import TILE_SIZE, Tile
from hard_reset.editor.tile_selector_gui import TileSelectorGui


class MapGui(GraphicalComponent):
    _tiles: Matrix[Tile]

    _tile_selector: TileSelectorGui
    _mouse: Mouse

    def __init__(self, tile_selector_gui: TileSelectorGui, mouse: Mouse) -> None:
        # Dimensions are larger to ensure that on_click event is catched
        super().__init__(
            Vertex2f(100, 100),
            Vertex2f(1000, 1000),
            z_index=2,
            visible=True,
            allow_click_out_of_bounds=True,
        )
        self._tiles = Matrix.from_size(10, 14, Tile.GROUND)
        self._tile_selector = tile_selector_gui
        self._mouse = mouse

    def render(self, renderer: Renderer) -> None:
        # Draw Tiles
        for tile, _position in self._tiles.get_entries():
            position = _position.multiplied(TILE_SIZE)
            renderer.draw_rect(
                position,
                position.translated(Vertex2f(TILE_SIZE, TILE_SIZE)),
                tile.color,
            )

        # Draw Phantom Tiles
        if self._mouse.is_dragging:
            assert self._mouse.drag_origin
            start_tile = self._mouse.drag_origin.translated(
                self.bounds.position.multiplied(-1)
            ).divided(TILE_SIZE, floor=True)
            end_tile = self._mouse.position.translated(
                self.bounds.position.multiplied(-1)
            ).divided(TILE_SIZE, floor=True)
            for x in range(
                int(min(start_tile.x, end_tile.x)),
                int(max(start_tile.x, end_tile.x)) + 1,
            ):
                for y in range(
                    int(min(start_tile.y, end_tile.y)),
                    int(max(start_tile.y, end_tile.y)) + 1,
                ):
                    renderer.draw_rect(
                        Vertex2f(x * TILE_SIZE, y * TILE_SIZE),
                        Vertex2f((x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE),
                        self._tile_selector._selected_tile.color,
                    )

        # Draw Grid
        dimensions = self._tiles.get_dimensions()
        width_in_tiles, height_in_tiles = int(dimensions.x), int(dimensions.y)
        for x in range(width_in_tiles):
            renderer.draw_line(
                Vertex2f(x * TILE_SIZE, 0),
                Vertex2f(x * TILE_SIZE, height_in_tiles * TILE_SIZE),
                Vertex3f(255, 255, 255),
            )
        for y in range(height_in_tiles):
            renderer.draw_line(
                Vertex2f(0, y * TILE_SIZE),
                Vertex2f(width_in_tiles * TILE_SIZE, y * TILE_SIZE),
                Vertex3f(255, 255, 255),
            )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        start_tile_position = start_position.divided(TILE_SIZE, floor=True)
        end_tile_position = position.divided(TILE_SIZE, floor=True)

        offset = self.manage_resize(start_tile_position, end_tile_position)
        start_tile_position = start_tile_position.translated(offset)
        end_tile_position = end_tile_position.translated(offset)

        for x in range(
            int(min(start_tile_position.x, end_tile_position.x)),
            int(max(start_tile_position.x, end_tile_position.x)) + 1,
        ):
            for y in range(
                int(min(start_tile_position.y, end_tile_position.y)),
                int(max(start_tile_position.y, end_tile_position.y)) + 1,
            ):
                try:
                    if x >= 0 and y >= 0:
                        self._tiles.set(
                            Vertex2f(x, y),
                            self._tile_selector._selected_tile,
                        )
                except IndexError:
                    ...

        self.manage_downsize()
        return True

    def manage_resize(
        self, start_tile_position: Vertex2f, end_tile_position: Vertex2f
    ) -> Vertex2f:
        dimensions = self._tiles.get_dimensions()
        current_width, current_height = int(dimensions.x), int(dimensions.y)

        # Check if click was in bounds
        if (
            start_tile_position.x < 0
            or start_tile_position.y < 0
            or start_tile_position.x >= current_width
            or start_tile_position.y >= current_height
        ):
            return Vertex2f(0, 0)

        min_x = int(min(start_tile_position.x, end_tile_position.x, 0))
        min_y = int(min(start_tile_position.y, end_tile_position.y, 0))
        max_x = int(
            max(start_tile_position.x + 1, end_tile_position.x + 1, current_width)
        )
        max_y = int(
            max(start_tile_position.y + 1, end_tile_position.y + 1, current_height)
        )

        new_width = max_x - min_x
        new_height = max_y - min_y

        # Check if resize is necessary
        if current_width == new_width and current_height == new_height:
            return Vertex2f(0, 0)

        new_tiles = Matrix.from_size(new_width, new_height, Tile.GROUND)

        for tile, position in self._tiles.get_entries():
            new_tiles.set(position.translated(Vertex2f(-min_x, -min_y)), tile)
        self._tiles = new_tiles

        return Vertex2f(-min_x, -min_y)

    def manage_downsize(self) -> None:
        while True:
            dimensions = self._tiles.get_dimensions()
            current_width, current_height = int(dimensions.x), int(dimensions.y)

            if current_height > 1:
                for x in range(current_width):
                    if self._tiles.get(Vertex2f(x, 0)) != Tile.VOID:
                        break
                else:
                    self._tiles = self._tiles.sub_matrix(
                        Vertex2f(0, 1), Vertex2f(current_width - 1, current_height - 1)
                    )
                    continue

                for x in range(current_width):
                    if self._tiles.get(Vertex2f(x, current_height - 1)) != Tile.VOID:
                        break
                else:
                    self._tiles = self._tiles.sub_matrix(
                        Vertex2f(0, 0), Vertex2f(current_width - 1, current_height - 2)
                    )
                    continue

            if current_width > 1:
                for y in range(current_height):
                    if self._tiles.get(Vertex2f(0, y)) != Tile.VOID:
                        break
                else:
                    self._tiles = self._tiles.sub_matrix(
                        Vertex2f(1, 0), Vertex2f(current_width - 1, current_height - 1)
                    )
                    continue

                for y in range(current_height):
                    if self._tiles.get(Vertex2f(current_width - 1, y)) != Tile.VOID:
                        break
                else:
                    self._tiles = self._tiles.sub_matrix(
                        Vertex2f(0, 0), Vertex2f(current_width - 2, current_height - 1)
                    )
                    continue

            break
