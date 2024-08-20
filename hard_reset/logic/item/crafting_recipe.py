from dataclasses import dataclass

from hard_reset.logic.item.item import (
    CRAFTING_BENCH_ITEM,
    WOODEN_PLANK,
    WOODEN_STICK,
    Item,
)


@dataclass
class CraftingIngredient:
    item: Item
    quantity: int


@dataclass
class SimpleCraftingRecipe:
    _ingredients: list[CraftingIngredient]
    _result: CraftingIngredient

    def __init__(
        self, result: CraftingIngredient, ingredients: list[CraftingIngredient]
    ) -> None:
        self._ingredients = ingredients
        self._result = result

    def can_craft(self, inventory: dict[str, int]) -> bool:
        for ingredient in self._ingredients:
            if inventory.get(ingredient.item.name, 0) < ingredient.quantity:
                return False
        return True


CRAFTING_BENCH_RECIPE = SimpleCraftingRecipe(
    result=CraftingIngredient(CRAFTING_BENCH_ITEM, 1),
    ingredients=[
        CraftingIngredient(WOODEN_PLANK, 1),
        CraftingIngredient(WOODEN_STICK, 4),
    ],
)

WOODEN_STICK_FROM_PLANK = SimpleCraftingRecipe(
    result=CraftingIngredient(WOODEN_STICK, 4),
    ingredients=[CraftingIngredient(WOODEN_PLANK, 1)],
)

CRAFTING_RECIPES = [CRAFTING_BENCH_RECIPE, WOODEN_STICK_FROM_PLANK]
RESULT_NAME_TO_RECIPE = {
    recipe._result.item.name: recipe for recipe in CRAFTING_RECIPES
}
