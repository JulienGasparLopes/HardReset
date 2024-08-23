from typing import TYPE_CHECKING, Callable, cast

import vertyces.utils.colors as colors
from game_manager.graphic.component.button import Button
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from game_manager.logic.uid_object import Uid  # TODO: logic leak
from vertyces.vertex import Vertex2f, Vertex3f

from hard_reset.messaging.messaging import EntityDoorInfoPacket, MapInfoPacket

if TYPE_CHECKING:
    from hard_reset.graphic.menu_map import MenuMap

TILE_SIZE = 40


class Chest(Button):
    uid: Uid
    _on_click_callback: Callable[[Uid], None]

    def __init__(
        self,
        uid: Uid,
        position: Vertex2f,
        action_callback: Callable[[Uid], None],
    ) -> None:
        super().__init__(position, Vertex2f(TILE_SIZE, TILE_SIZE), self._on_chest_click)
        self._on_click_callback = action_callback
        self.uid = uid

    def _on_chest_click(self) -> None:
        print(f"Opening chest {self.uid}")
        self._on_click_callback(self.uid)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(0, 0), self.bounds.dimensions, colors.CYAN, z_index=12
        )


class Player(GraphicalComponent):
    uid: Uid

    def __init__(self, uid: Uid, position: Vertex2f) -> None:
        super().__init__(position, Vertex2f(35, 35))
        self.uid = uid

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(0, 0), self.bounds.dimensions, colors.PURPLE, z_index=12
        )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False


class Door(GraphicalComponent):
    uid: Uid
    map_travel_uid: Uid
    on_use: Callable[[Uid], None]

    def __init__(
        self,
        uid: Uid,
        position: Vertex2f,
        map_travel_uid: Uid,
        on_use: Callable[[Uid], None],
    ) -> None:
        super().__init__(position, Vertex2f(TILE_SIZE, TILE_SIZE * 2))
        self.uid = uid
        self.map_travel_uid = map_travel_uid
        self.on_use = on_use

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(0, 0), self.bounds.dimensions, colors.YELLOW, z_index=12
        )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        self.on_use(self.map_travel_uid)
        return True


class MapComponent(GraphicalComponent):
    _current_map_info: MapInfoPacket
    _menu_map: "MenuMap"

    _graphical_entities: dict[Uid, GraphicalComponent]

    def __init__(self, menu_map: "MenuMap") -> None:
        self._menu_map = menu_map
        self._current_map_info = (
            self._menu_map.graphic_manager.message_manager.get_map_info(
                self._menu_map.current_map_uid
            )
        )
        super().__init__(
            Vertex2f(0, 0),
            Vertex2f(self._current_map_info.width, self._current_map_info.height),
        )
        self._graphical_entities = {}

    def _get_map_dimensions(self) -> Vertex2f:
        return Vertex2f(self._current_map_info.width, self._current_map_info.height)

    def change_map(self, map_info: MapInfoPacket) -> None:
        self._current_map_info = map_info
        self._graphical_entities.clear()
        self.clear_components()

    def update_map_info(self, map_info: MapInfoPacket) -> None:
        self._current_map_info = map_info

        for entity_uid, entity_info in self._current_map_info.entities.items():
            entity_component = self._graphical_entities.get(entity_uid)
            if entity_component is not None:
                entity_component.bounds = entity_component.bounds.at_position(
                    entity_info.position
                )
            else:
                if entity_info.type_name == "Chest":
                    entity_uid = entity_info.uid

                    entity_component = Chest(
                        entity_uid, entity_info.position, self._menu_map.show_inventory
                    )

                elif entity_info.type_name == "Player":
                    if entity_component is None:
                        entity_component = Player(entity_uid, entity_info.position)
                elif entity_info.type_name == "Door":
                    entity_info = cast(EntityDoorInfoPacket, entity_info)
                    entity_component = Door(
                        entity_uid,
                        entity_info.position,
                        map_travel_uid=entity_info.map_travel_uid,
                        on_use=self._menu_map.use_map_travel,
                    )
                else:
                    print(f"Unknown entity type: {entity_info.type_name}")
                    continue

                self.add_component(entity_component)
                self._graphical_entities[entity_uid] = entity_component

        # Calculate map offset
        player = self._graphical_entities.get(self._menu_map.graphic_manager.player_uid)
        assert player
        map_dimensions = self._get_map_dimensions()
        offset = self._menu_map.graphic_manager.window.get_center
        offset = offset.translated(
            map_dimensions.translated(player.bounds.dimensions.divided(-2))
        )
        player_offset = map_dimensions.translated(player.bounds.position)
        offset = offset.translated(player_offset.divided(-1))
        self.bounds = self.bounds.at_position(offset)

    def render(self, renderer: Renderer) -> None:
        # Draw tiles
        for pos, walkable in self._current_map_info.tiles.items():
            p1 = Vertex2f(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
            p2 = p1.translated(Vertex2f(TILE_SIZE, TILE_SIZE))
            renderer.draw_rect(
                p1, p2, Vertex3f(255, 0, 0) if not walkable else Vertex3f(0, 0, 255)
            )

        # Draw grid
        max_width = self._current_map_info.width
        max_height = self._current_map_info.height
        for i in range(0, max_height, TILE_SIZE):
            renderer.draw_line(
                Vertex2f(0, i), Vertex2f(max_width, i), Vertex3f(0, 0, 0), z_index=1
            )
        for j in range(0, max_width, TILE_SIZE):
            renderer.draw_line(
                Vertex2f(j, 0), Vertex2f(j, max_height), Vertex3f(0, 0, 0), z_index=1
            )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False
