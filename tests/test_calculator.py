import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from calculator import add, subtract, multiply, divide, percentage, square_root


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_percentage_rejects_negative():
    try:
        percentage(200, -10)
        assert False
    except ValueError:
        assert True

def test_square_root_rejects_negative():
    try:
        square_root(-25)
        assert False
    except ValueError:
        assert True