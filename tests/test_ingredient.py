import pytest

# ИСПРАВЛЕНО: прямые импорты из корня проекта (вместо praktikum)
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:

    # ── __init__ ──────────────────────────────────────────────

    @pytest.mark.parametrize("ing_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100.0),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100.0),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200.0),
        (INGREDIENT_TYPE_FILLING, "sausage", 300.0),
    ])
    def test_init_stores_type_name_price(self, ing_type, name, price):
        ingredient = Ingredient(ing_type, name, price)
        # ИСПРАВЛЕНО: один assert вместо трёх
        assert (
            ingredient.type == ing_type
            and ingredient.name == name
            and ingredient.price == price
        )

    # ── get_type ─────────────────────────────────────────────

    @pytest.mark.parametrize("ing_type", [
        INGREDIENT_TYPE_SAUCE,
        INGREDIENT_TYPE_FILLING,
        "SAUCE",
        "FILLING",
    ])
    def test_get_type_returns_type(self, ing_type):
        ingredient = Ingredient(ing_type, "test", 100.0)
        assert ingredient.get_type() == ing_type

    # ── get_name ─────────────────────────────────────────────

    @pytest.mark.parametrize("name", [
        "hot sauce",
        "sour cream",
        "chili sauce",
        "cutlet",
        "dinosaur",
        "",
    ])
    def test_get_name_returns_name(self, name):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, name, 100.0)
        assert ingredient.get_name() == name

    # ── get_price ────────────────────────────────────────────

    @pytest.mark.parametrize("price", [
        100.0,
        200.0,
        300.0,
        0.0,
        50.5,
    ])
    def test_get_price_returns_price(self, price):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", price)
        assert ingredient.get_price() == price

    # ── Негативные сценарии ──────────────────────────────────

    @pytest.mark.parametrize("price", [
        -100.0,
        -0.01,
    ])
    def test_init_accepts_negative_price(self, price):
        """Ingredient не валидирует знак цены. См. README — «Отрицательные цены»."""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", price)
        assert ingredient.get_price() == price

    def test_init_accepts_empty_name(self):
        """Ingredient не валидирует пустое название."""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "", 100.0)
        assert ingredient.get_name() == ""

    def test_init_accepts_invalid_type(self):
        """Ingredient не валидирует тип — принимает любую строку."""
        ingredient = Ingredient("UNKNOWN_TYPE", "test", 100.0)
        assert ingredient.get_type() == "UNKNOWN_TYPE"
