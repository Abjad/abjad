from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_integer_equivalent_number_01():

    assert mathtools.is_integer_equivalent_number(2)
    assert mathtools.is_integer_equivalent_number(2.0)
    assert mathtools.is_integer_equivalent_number(Duration(2, 1))


def test_mathtools_is_integer_equivalent_number_02():

    assert not mathtools.is_integer_equivalent_number(2.1)
    assert not mathtools.is_integer_equivalent_number(Duration(2, 3))
    assert not mathtools.is_integer_equivalent_number('foo')
