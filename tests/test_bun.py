import pytest

from bun import Bun 


class TestBun:

    # ── __init__ ──────────────────────────────────────────────

    @pytest.mark.parametrize("name, price", [
        ("black bun", 100.0),
        ("white bun", 200.0),
        ("red bun", 300.0),
        ("sesame bun", 50.5),
    ])
    def test_init_stores_name_and_price(self, name, price):
        bun = Bun(name, price)
        # Один assert: проверяем оба поля сразу
        assert (bun.name, bun.price) == (name, price)

    # ── get_name ─────────────────────────────────────────────

    @pytest.mark.parametrize("name", [
        "black bun",
        "white bun",
        "red bun",
        "",
        "очень длинное название булочки с пробелами",
    ])
    def test_get_name_returns_name(self, name):
        bun = Bun(name, 100.0)
        assert bun.get_name() == name

    # ── get_price ─────────────────────────────────────────────

    @pytest.mark.parametrize("price", [
        100.0,
        200.0,
        0.0,
        50.5,
        9999.99,
    ])
    def test_get_price_returns_price(self, price):
        bun = Bun("black bun", price)
        assert bun.get_price() == price

    # ── Негативные сценарии ───────────────────────────────────

    @pytest.mark.parametrize("name, price", [
        ("black bun", -100.0),
        ("white bun", -0.01),
    ])
    def test_init_accepts_negative_price(self, name, price):
        """Bun не валидирует знак цены — отрицательное значение
        сохраняется без ошибки. См. README — «Отрицательные цены»."""
        bun = Bun(name, price)
        assert bun.get_price() == price

    def test_init_accepts_empty_name(self):
        """Bun не валидирует пустое название."""
        bun = Bun("", 100.0)
        assert bun.get_name() == ""

    def test_init_accepts_none_name(self):
        """Bun не валидирует None как название — сохраняется как есть."""
        bun = Bun(None, 100.0)
        assert bun.get_name() is None

