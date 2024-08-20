from typing import Callable

import vertyces.utils.colors as colors
from game_manager.graphic.component.button import Button
from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton
from vertyces.vertex import Vertex2f


class RecipeButton(Button):
    _recipe_name: str
    _may_craft: bool
    _select_recipe: Callable[[str], None]

    def __init__(
        self,
        position: Vertex2f,
        recipe_name: str,
        may_craft: bool,
        select_recipe: Callable[[str], None],
    ) -> None:
        super().__init__(position, Vertex2f(90, 20), self._select_recipe_callback)
        self._recipe_name = recipe_name
        self._may_craft = may_craft
        self._select_recipe = select_recipe

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(0, 0),
            self.bounds.dimensions,
            colors.ORANGE if self._may_craft else colors.LIGHT_GREY,
        )
        renderer.draw_text(Vertex2f(2, 2), self._recipe_name, colors.BLACK)

    def _select_recipe_callback(self) -> None:
        self._select_recipe(self._recipe_name)


class CraftSelectorWidget(GraphicalComponent):
    _crafting_recipes: dict[str, dict[str, int]]
    _selected_recipe: str | None = None
    _on_select_recipe: Callable[[str], None]

    def __init__(
        self,
        position: Vertex2f,
        crafting_recipes: dict[str, dict[str, int]],
        on_select_recipe: Callable[[str], None],
    ) -> None:
        super().__init__(position, Vertex2f(400, 400))
        self._crafting_recipes = crafting_recipes
        self._on_select_recipe = on_select_recipe

    def update_inventory(self, inventory: dict[str, int]) -> None:
        self.clear_components()
        for idx, (recipe_name, recipe) in enumerate(self._crafting_recipes.items()):
            may_craft = True
            for item_name, quantity in recipe.items():
                if item_name not in inventory or inventory[item_name] < quantity:
                    may_craft = False
                    break

            self.add_component(
                RecipeButton(
                    Vertex2f(10, 10 + idx * 22),
                    recipe_name,
                    may_craft,
                    lambda recipe_name: self._select_recipe(recipe_name),
                )
            )

    def _select_recipe(self, recipe_name: str) -> None:
        self._selected_recipe = recipe_name
        self._on_select_recipe(recipe_name)

    def render(self, renderer: Renderer) -> None:
        if self._selected_recipe:
            renderer.draw_text(
                Vertex2f(100, 2),
                f"Selected Recipe: {self._selected_recipe}",
                colors.BLACK,
            )

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        return False
