from abjad import Fraction
from abjad.tools.quantizationtools import is_valid_beatspan


def test_quantizationtools_is_valid_beatspan_01():

    assert is_valid_beatspan(2)
    assert is_valid_beatspan(1)
    assert is_valid_beatspan(Fraction(1, 2))
    assert is_valid_beatspan(Fraction(1, 4))

    assert not is_valid_beatspan(0)
    assert not is_valid_beatspan(-1)
    assert not is_valid_beatspan(Fraction(-1, 2))
    assert not is_valid_beatspan(Fraction(1, 3))
    assert not is_valid_beatspan(3)
