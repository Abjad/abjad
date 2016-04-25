# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_divide_number_by_ratio_01():
    r'''Divide int by ratio.
    '''

    duration = mathtools.divide_number_by_ratio(1, [1, 1, 2])

    assert len(duration) == 3
    assert duration[0] == Duration(1, 4)
    assert duration[1] == Duration(1, 4)
    assert duration[2] == Duration(1, 2)


def test_mathtools_divide_number_by_ratio_02():
    r'''Divide fraction by ratio.
    '''

    duration = mathtools.divide_number_by_ratio(Duration(1, 2), [1, 1, 2])

    assert len(duration) == 3
    assert duration[0] == Duration(1, 8)
    assert duration[1] == Duration(1, 8)
    assert duration[2] == Duration(1, 4)


def test_mathtools_divide_number_by_ratio_03():
    r'''Raise type error on nonnumber.
    '''

    statement = "mathtools.divide_number_by_ratio('foo', [1, 1, 3])"
    assert pytest.raises(Exception, statement)


def test_mathtools_divide_number_by_ratio_04():
    r'''Duration returns durations.
    '''

    result = mathtools.divide_number_by_ratio(Duration(1, 4), [1, 1, 1])
    assert result == [Duration(1, 12), Duration(1, 12), Duration(1, 12)]
