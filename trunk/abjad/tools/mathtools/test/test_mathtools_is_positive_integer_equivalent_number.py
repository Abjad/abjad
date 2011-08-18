from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_positive_integer_equivalent_number_01():

    assert mathtools.is_positive_integer_equivalent_number(Duration(4, 2))
    assert mathtools.is_positive_integer_equivalent_number(2.0)
    assert mathtools.is_positive_integer_equivalent_number(2)


def test_mathtools_is_positive_integer_equivalent_number_02():

    assert not mathtools.is_positive_integer_equivalent_number(0)
    assert not mathtools.is_positive_integer_equivalent_number(-2)
    assert not mathtools.is_positive_integer_equivalent_number(Duration(5, 2))
    assert not mathtools.is_positive_integer_equivalent_number(2.5)
    assert not mathtools.is_positive_integer_equivalent_number('foo')
