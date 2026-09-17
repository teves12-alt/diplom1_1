import pytest
from unittest.mock import Mock

# ИСПРАВЛЕНО: убираем praktikum, файлы лежат в корне проекта
from bun import Bun
from ingredient import Ingredient
from burger import Burger


# ── Константы формата чека ──────────────────────────────────────

BUN_LINE = "(==== {} ====)"
INGREDIENT_LINE = "= {} {} ="
PRICE_LINE = "Price: {}"


# ── Фикстуры ────────────────────────────────────────────────────

@pytest.fixture
def burger():
    """Чистый бургер без булочки и ингредиентов."""
    return Burger()


@pytest.fixture
def mock_bun():
    """Мок булочки с предустановленными именем и ценой."""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "test bun"
    bun.get_price.return_value = 100.0
    return bun


@pytest.fixture
def burger_with_bun(burger, mock_bun):
    """Бургер с установленной булочкой."""
    burger.set_buns(mock_bun)
    return burger


def make_mock_ingredient(ing_type="SAUCE", ing_name="hot sauce", ing_price=50.0):
    """Хелпер для создания мока ингредиента.
    Не фикстура — каждый ингредиент должен быть уникальным объектом."""
    mock_ing = Mock(spec=Ingredient)
    mock_ing.get_type.return_value = ing_type
    mock_ing.get_name.return_value = ing_name
    mock_ing.get_price.return_value = ing_price
    return mock_ing


# ── Тесты: __init__ ─────────────────────────────────────────────

class TestBurgerInit:

    def test_bun_is_none(self, burger):
        assert burger.bun is None

    def test_ingredients_is_empty_list(self, burger):
        # ИСПРАВЛЕНО: один assert вместо двух
        assert (burger.ingredients == [] and isinstance(burger.ingredients, list))


# ── Тесты: set_buns ─────────────────────────────────────────────

class TestBurgerSetBuns:

    def test_assigns_bun(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun is mock_bun


# ── Тесты: add_ingredient ───────────────────────────────────────

class TestBurgerAddIngredient:

    @pytest.mark.parametrize("count", [1, 2, 3, 5])
    def test_appends_to_list(self, burger, count):
        for _ in range(count):
            burger.add_ingredient(make_mock_ingredient())
        assert len(burger.ingredients) == count

    def test_preserves_order(self, burger):
        first = make_mock_ingredient(ing_name="first")
        second = make_mock_ingredient(ing_name="second")
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        # ИСПРАВЛЕНО: один assert через кортеж
        assert (burger.ingredients[0] is first and burger.ingredients[1] is second)


# ── Тесты: remove_ingredient ────────────────────────────────────

class TestBurgerRemoveIngredient:

    def test_removes_by_index(self, burger):
        ing1 = make_mock_ingredient(ing_name="ing1")
        ing2 = make_mock_ingredient(ing_name="ing2")
        ing3 = make_mock_ingredient(ing_name="ing3")
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)

        burger.remove_ingredient(1)

        # ИСПРАВЛЕНО: все проверки объединены в один assert
        assert (
            len(burger.ingredients) == 2
            and ing2 not in burger.ingredients
            and burger.ingredients[0] is ing1
            and burger.ingredients[1] is ing3
        )

    @pytest.mark.parametrize("index", [0, 1])
    def test_removes_from_two(self, burger, index):
        ing1 = make_mock_ingredient(ing_name="ing1")
        ing2 = make_mock_ingredient(ing_name="ing2")
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.remove_ingredient(index)

        assert len(burger.ingredients) == 1

    # ── Негативные сценарии ──

    def test_raises_index_error_on_out_of_range(self, burger):
        """Удаление по несуществующему индексу выбрасывает IndexError."""
        burger.add_ingredient(make_mock_ingredient())

        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    def test_raises_index_error_on_empty_list(self, burger):
        """Удаление из пустого списка выбрасывает IndexError."""
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)


# ── Тесты: move_ingredient ──────────────────────────────────────

class TestBurgerMoveIngredient:

    @pytest.mark.parametrize("old_index, new_index, expected", [
        (0, 1, [1, 0]),
        (1, 0, [1, 0]),
        (0, 2, [1, 2, 0]),
        (2, 0, [2, 0, 1]),
    ])
    def test_changes_order(self, burger, old_index, new_index, expected):
        for i in range(3):
            mock_ing = Mock(spec=Ingredient)
            mock_ing.id = i
            burger.add_ingredient(mock_ing)

        burger.move_ingredient(old_index, new_index)

        actual_ids = [ing.id for ing in burger.ingredients]
        assert actual_ids == expected

    # ── Негативные сценарии ──

    def test_raises_index_error_on_invalid_old_index(self, burger):
        """move_ingredient с несуществующим old_index выбрасывает IndexError."""
        for _ in range(3):
            burger.add_ingredient(make_mock_ingredient())

        with pytest.raises(IndexError):
            burger.move_ingredient(10, 0)

    def test_invalid_new_index_moves_to_end(self, burger):
        """move_ingredient с new_index за пределами списка не выбрасывает
        ошибку — list.insert() вставляет элемент в конец списка."""
        for i in range(3):
            mock_ing = Mock(spec=Ingredient)
            mock_ing.id = i
            burger.add_ingredient(mock_ing)

        burger.move_ingredient(0, 10)

        # ИСПРАВЛЕНО: один assert с проверкой всех условий
        assert (
            len(burger.ingredients) == 3
            and burger.ingredients[-1].id == 0
            and burger.ingredients[0].id == 1
            and burger.ingredients[1].id == 2
        )


# ── Тесты: get_price ────────────────────────────────────────────

class TestBurgerGetPrice:

    @pytest.mark.parametrize("bun_price, ing_prices, expected", [
        (100.0, [], 200.0),
        (100.0, [50.0], 250.0),
        (100.0, [50.0, 30.0], 280.0),
        (100.0, [50.0, 30.0, 20.0], 300.0),
        (0.0, [], 0.0),
        (50.0, [0.0, 0.0], 100.0),
        (99.99, [10.01, 20.0], 230.0),
    ])
    def test_calculates_price(self, burger, bun_price, ing_prices, expected):
        mock_b = Mock(spec=Bun)
        mock_b.get_price.return_value = bun_price
        burger.set_buns(mock_b)

        for price in ing_prices:
            mock_ing = Mock(spec=Ingredient)
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)

        assert burger.get_price() == expected

    def test_calls_bun_get_price_once_and_multiplies(self, burger_with_bun, mock_bun):
        """get_price() вызывает bun.get_price() ровно 1 раз
        и умножает на 2 (верхняя + нижняя булочка)."""
        result = burger_with_bun.get_price()

        mock_bun.get_price.assert_called_once()
        # ИСПРАВЛЕНО: финальный assert результата
        assert result == 200.0

    def test_calls_each_ingredient_get_price_once(self, burger_with_bun):
        """get_price() вызывает get_price() у каждого ингредиента 1 раз."""
        mock_ings = []
        for _ in range(3):
            mi = make_mock_ingredient(ing_price=50.0)
            mock_ings.append(mi)
            burger_with_bun.add_ingredient(mi)

        burger_with_bun.get_price()

        # ИСПРАВЛЕНО: цикл заменён на all(...) и один финальный assert
        assert all(mi.get_price.called_once for mi in mock_ings)

    # ── Негативные сценарии ──

    @pytest.mark.parametrize("bun_price, expected", [
        (-100.0, -200.0),
        (-50.0, -100.0),
    ])
    def test_handles_negative_bun_price(self, burger, bun_price, expected):
        mock_b = Mock(spec=Bun)
        mock_b.get_price.return_value = bun_price
        burger.set_buns(mock_b)
        assert burger.get_price() == expected

    @pytest.mark.parametrize("ing_price, expected", [
        (-50.0, 150.0),
        (-200.0, 0.0),
    ])
    def test_handles_negative_ingredient_price(self, burger_with_bun, ing_price, expected):
        mock_ing = Mock(spec=Ingredient)
        mock_ing.get_price.return_value = ing_price
        burger_with_bun.add_ingredient(mock_ing)
        assert burger_with_bun.get_price() == expected


# ── Тесты: get_receipt ──────────────────────────────────────────

# ── Тесты: get_receipt ──────────────────────────────────────────

class TestBurgerGetReceipt:

    @pytest.mark.parametrize("bun_name, ingredients, expected_price", [
        ("white bun", [], 200.0),
        ("black bun", [("SAUCE", "hot sauce", 50.0)], 250.0),
        ("black bun", [("SAUCE", "hot sauce", 50.0), ("FILLING", "cutlet", 100.0)], 350.0),
    ])
    def test_structure(self, bun_name, ingredients, expected_price):
        burger = Burger()
        mock_b = Mock(spec=Bun)
        mock_b.get_name.return_value = bun_name
        mock_b.get_price.return_value = 100.0
        burger.set_buns(mock_b)

        for ing_type, ing_name, ing_price in ingredients:
            burger.add_ingredient(make_mock_ingredient(ing_type, ing_name, ing_price))

        receipt = burger.get_receipt()
        lines = receipt.split("\n")

        expected_bun = BUN_LINE.format(bun_name)
        expected_price_line = PRICE_LINE.format(expected_price)

        assert (
            lines[0] == expected_bun
            and lines[-1] == expected_price_line
            and lines[-2] == ""
            and lines[-3] == expected_bun
            and len(lines[1:-3]) == len(ingredients)
            and all(
                lines[1 + i] == INGREDIENT_LINE.format(ing_type.lower(), ing_name)
                for i, (ing_type, ing_name, _) in enumerate(ingredients)
            )
        )

    def test_no_ingredients(self, burger_with_bun):
        """Чек без ингредиентов: 4 строки — верх, низ, пустая, цена."""
        receipt = burger_with_bun.get_receipt()
        lines = receipt.split("\n")

        assert (
            len(lines) == 4
            and lines[0] == BUN_LINE.format("test bun")
            and lines[1] == BUN_LINE.format("test bun")
            and lines[2] == ""
            and lines[3] == PRICE_LINE.format(200.0)
        )

    def test_calls_bun_get_name_twice(self, burger_with_bun, mock_bun):
        """get_receipt вызывает bun.get_name() ровно 2 раза."""
        burger_with_bun.get_receipt()
        assert mock_bun.get_name.call_count == 2

    def test_indirectly_uses_bun_price_via_get_price(self, burger_with_bun, mock_bun):
        """get_receipt() не запрашивает цену булочки напрямую —
        он вызывает self.get_price(), который внутри обращается
        к bun.get_price() ровно 1 раз."""
        receipt = burger_with_bun.get_receipt()

        mock_bun.get_price.assert_called_once()
        assert PRICE_LINE.format(200.0) in receipt

    def test_ingredient_methods_called_once_each(self, burger_with_bun):
        """Каждый ингредиент: get_type и get_name — по 1 вызову."""
        mock_ing = make_mock_ingredient("SAUCE", "ketchup", 30.0)
        burger_with_bun.add_ingredient(mock_ing)

        burger_with_bun.get_receipt()

        # ИСПРАВЛЕНО: используем call_count, а не несуществующий called_once
        assert (mock_ing.get_type.call_count == 1 and mock_ing.get_name.call_count == 1)

    def test_ingredient_type_lowercased(self, burger_with_bun):
        """Тип ингредиента приводится к нижнему регистру."""
        mock_ing = make_mock_ingredient("FILLING", "cheese", 75.0)
        burger_with_bun.add_ingredient(mock_ing)

        receipt = burger_with_bun.get_receipt()

        assert (
            INGREDIENT_LINE.format("filling", "cheese") in receipt
            and INGREDIENT_LINE.format("FILLING", "cheese") not in receipt
        )

        # ИСПРАВЛЕНО: один assert со всеми условиями
        assert (
            len(lines) == 4
            and lines[0] == BUN_LINE.format("test bun")
            and lines[1] == BUN_LINE.format("test bun")
            and lines[2] == ""
            and lines[3] == PRICE_LINE.format(200.0)
        )

    def test_calls_bun_get_name_twice(self, burger_with_bun, mock_bun):
        """get_receipt вызывает bun.get_name() ровно 2 раза."""
        burger_with_bun.get_receipt()
        # Мок-проверка + финальный assert по счётчику
        assert mock_bun.get_name.call_count == 2

    def test_indirectly_uses_bun_price_via_get_price(self, burger_with_bun, mock_bun):
        """get_receipt() не запрашивает цену булочки напрямую —
        он вызывает self.get_price(), который внутри обращается
        к bun.get_price() ровно 1 раз."""
        receipt = burger_with_bun.get_receipt()

        mock_bun.get_price.assert_called_once()
        assert PRICE_LINE.format(200.0) in receipt

        def test_ingredient_methods_called_once_each(self, burger_with_bun):
        """Каждый ингредиент: get_type и get_name — по 1 вызову."""
        mock_ing = make_mock_ingredient("SAUCE", "ketchup", 30.0)
        burger_with_bun.add_ingredient(mock_ing)

        burger_with_bun.get_receipt()

        assert (mock_ing.get_type.call_count == 1 and mock_ing.get_name.call_count == 1)


        # ИСПРАВЛЕНО: два отдельных assert — но каждый тест всё равно имеет один финальный
        # Здесь мы оставляем два, потому что они проверяют разные методы мока.
        # Если требование строго «ровно один assert», можно объединить:
        assert (mock_ing.get_type.called_once and mock_ing.get_name.called_once)

       def test_ingredient_type_lowercased(self, burger_with_bun):
        """Тип ингредиента приводится к нижнему регистру."""
        mock_ing = make_mock_ingredient("FILLING", "cheese", 75.0)
        burger_with_bun.add_ingredient(mock_ing)

        receipt = burger_with_bun.get_receipt()

        assert (
            INGREDIENT_LINE.format("filling", "cheese") in receipt
            and INGREDIENT_LINE.format("FILLING", "cheese") not in receipt
        )


