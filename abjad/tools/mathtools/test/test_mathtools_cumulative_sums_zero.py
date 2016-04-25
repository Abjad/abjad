# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_cumulative_sums_zero_01():
    r'''Returns list of the cumulative sums of the integer elements in input.
    '''

    assert mathtools.cumulative_sums([1, 2, 3]) == [0, 1, 3, 6]
    assert mathtools.cumulative_sums([10, -9, -8]) == [0, 10, 1, -7]
    assert mathtools.cumulative_sums([0, 0, 0, 5]) == [0, 0, 0, 0, 5]
    assert mathtools.cumulative_sums([-10, 10, -10, 10]) == \
        [0, -10, 0, -10, 0]
