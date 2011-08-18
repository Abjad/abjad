from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_dotted_integer_01():

    assert not mathtools.is_dotted_integer(0)
    assert not mathtools.is_dotted_integer(1)
    assert not mathtools.is_dotted_integer(2)
    assert mathtools.is_dotted_integer(3)
    assert not mathtools.is_dotted_integer(4)
    assert not mathtools.is_dotted_integer(5)
    assert mathtools.is_dotted_integer(6)
    assert mathtools.is_dotted_integer(7)
    assert not mathtools.is_dotted_integer(8)
    assert not mathtools.is_dotted_integer(9)
    assert not mathtools.is_dotted_integer(10)
    assert not mathtools.is_dotted_integer(11)
    assert mathtools.is_dotted_integer(12)
    assert not mathtools.is_dotted_integer(13)
    assert mathtools.is_dotted_integer(14)
    assert mathtools.is_dotted_integer(15)
