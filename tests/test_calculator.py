import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from calculator import add, subtract, multiply, divide, percentage, square_root, cube, power, factorial


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

def test_cube():
    assert cube(3) == 27

def test_power():
    assert power(2, 3) == 8
    assert power(5, 2) == 25
def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(1) == 1


def test_factorial_rejects_negative():
    try:
        factorial(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_factorial_rejects_decimal():
    try:
        factorial(3.5)
        assert False, "Expected ValueError"
    except ValueError:
        pass