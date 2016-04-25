# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_cumulative_sums_01():
    r'''Returns list of the cumulative sums of the integer elements in input.
    '''

    assert mathtools.cumulative_sums([1, 2, 3], start=None) == [1, 3, 6]
    assert mathtools.cumulative_sums([10, -9, -8], start=None) == [10, 1, -7]
    assert mathtools.cumulative_sums([0, 0, 0, 5], start=None) == [0, 0, 0, 5]
    assert mathtools.cumulative_sums([-10, 10, -10, 10], start=None) == \
        [-10, 0, -10, 0]


def test_mathtools_cumulative_sums_02():
    r'''Raise exception when sequence is neither tuple nor list.
    '''

    assert pytest.raises(Exception, "mathtools.cumulative_sums('foo')")
