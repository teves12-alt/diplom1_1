import pytest
from database import Database
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestDatabase:

    def test_initializes_with_three_buns(self):
        db = Database()
        assert len(db.available_buns()) == 3

    def test_buns_are_correct_instances(self):
        db = Database()
        buns = db.available_buns()
        # Один assert: проверяем, что все элементы — экземпляры Bun
        assert all(isinstance(b, Bun) for b in buns)

    def test_initializes_with_six_ingredients(self):
        db = Database()
        assert len(db.available_ingredients()) == 6

    def test_ingredients_are_correct_instances(self):
        db = Database()
        ings = db.available_ingredients()
        assert all(isinstance(i, Ingredient) for i in ings)

    def test_bun_names_and_prices_are_set(self):
        db = Database()
        buns = db.available_buns()
        # Проверяем, что в списке есть булочка с именем "black bun" и ценой 100
        assert any(b.get_name() == "black bun" and b.get_price() == 100 for b in buns)

    def test_ingredient_types_are_present(self):
        db = Database()
        ings = db.available_ingredients()
        # Проверяем наличие хотя бы одного соуса и одной начинки
        has_sauce = any(i.get_type() == INGREDIENT_TYPE_SAUCE for i in ings)
        has_filling = any(i.get_type() == INGREDIENT_TYPE_FILLING for i in ings)
        assert has_sauce and has_filling
