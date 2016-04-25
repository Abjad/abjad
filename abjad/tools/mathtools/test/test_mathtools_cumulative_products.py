# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_cumulative_products_01():
    r'''Returns list of the cumulative products of the elements in input.
    '''

    assert mathtools.cumulative_products([1, 2, 3]) == [1, 2, 6]
    assert mathtools.cumulative_products([10, -9, -8]) == [10, -90, 720]
    assert mathtools.cumulative_products([0, 0, 0, 5]) == [0, 0, 0, 0]
    assert mathtools.cumulative_products([-10, 10, -10, 10]) == \
        [-10, -100, 1000, 10000]


def test_mathtools_cumulative_products_02():
    r'''Raise TypeError when l is not a list.
    Raise ValueError when l is empty.
    '''

    assert pytest.raises(TypeError, "mathtools.cumulative_products('foo')")
    assert pytest.raises(ValueError, 'mathtools.cumulative_products([])')
