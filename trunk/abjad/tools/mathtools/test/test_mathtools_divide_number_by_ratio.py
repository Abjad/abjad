# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import mathtools
import py.test


def test_mathtools_divide_number_by_ratio_01():
    r'''Divide int by ratio.
    '''

    t = mathtools.divide_number_by_ratio(1, [1, 1, 2])

    assert len(t) == 3
    assert t[0] == Duration(1, 4)
    assert t[1] == Duration(1, 4)
    assert t[2] == Duration(1, 2)


def test_mathtools_divide_number_by_ratio_02():
    r'''Divide fraction by ratio.
    '''

    t = mathtools.divide_number_by_ratio(Duration(1, 2), [1, 1, 2])

    assert len(t) == 3
    assert t[0] == Duration(1, 8)
    assert t[1] == Duration(1, 8)
    assert t[2] == Duration(1, 4)


def test_mathtools_divide_number_by_ratio_03():
    r'''Raise type error on nonnumber.
    '''

    assert py.test.raises(Exception, "mathtools.divide_number_by_ratio('foo', [1, 1, 3])")


def test_mathtools_divide_number_by_ratio_04():
    r'''Duration returns durations.
    '''

    result = mathtools.divide_number_by_ratio(Duration(1, 4), [1, 1, 1])
    assert result == [Duration(1, 12), Duration(1, 12), Duration(1, 12)]
