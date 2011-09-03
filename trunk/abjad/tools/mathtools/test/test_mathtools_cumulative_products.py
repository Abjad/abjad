from abjad import *
from abjad.tools import mathtools
import py.test


def test_mathtools_cumulative_products_01():
    '''Return list of the cumulative products of the elements in input.'''

    assert mathtools.cumulative_products([1, 2, 3]) == [1, 2, 6]
    assert mathtools.cumulative_products([10, -9, -8]) == [10, -90, 720]
    assert mathtools.cumulative_products([0, 0, 0, 5]) == [0, 0, 0, 0]
    assert mathtools.cumulative_products([-10, 10, -10, 10]) == \
        [-10, -100, 1000, 10000]


def test_mathtools_cumulative_products_02():
    '''Raise TypeError when l is not a list.
        Raise ValueError when l is empty.'''

    assert py.test.raises(TypeError, "mathtools.cumulative_products('foo')")
    assert py.test.raises(ValueError, 'mathtools.cumulative_products([])')
