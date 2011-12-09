from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_integer_equivalent_expr_01():

    assert mathtools.is_integer_equivalent_expr(12)
    assert mathtools.is_integer_equivalent_expr('12')
    assert mathtools.is_integer_equivalent_expr(-1)
    assert mathtools.is_integer_equivalent_expr('-1')


def test_mathtools_is_integer_equivalent_expr_02():

    assert not mathtools.is_integer_equivalent_expr('foo')
    assert not mathtools.is_integer_equivalent_expr('12.0')
    assert not mathtools.is_integer_equivalent_expr(1.5)
    assert not mathtools.is_integer_equivalent_expr(-1.5)
