# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_partition_integer_by_ratio_01():
    r'''Partition integer n according to ratio.
    '''

    t = mathtools.partition_integer_by_ratio(10, [1])
    assert t == [10]

    t = mathtools.partition_integer_by_ratio(10, [1, 1])
    assert t == [5, 5]

    t = mathtools.partition_integer_by_ratio(10, [1, -1, -1])
    assert t == [3, -4, -3]

    t = mathtools.partition_integer_by_ratio(-10, [1, 1, 1, 1])
    assert t == [-3, -2, -3, -2]

    t = mathtools.partition_integer_by_ratio(-10, [1, 1, 1, 1, 1])
    assert t == [-2, -2, -2, -2, -2]


def test_mathtools_partition_integer_by_ratio_02():
    r'''Partition integer n according to ratio.
    '''

    partition = mathtools.partition_integer_by_ratio(10, [1, 2])
    assert partition == [3, 7]

    partition = mathtools.partition_integer_by_ratio(10, [3, 1])
    assert partition == [8, 2]

    partition = mathtools.partition_integer_by_ratio(-10, [-3, 2])
    assert partition == [6, -4]


def test_mathtools_partition_integer_by_ratio_03():
    r'''Raise type error on noninteger n.
    '''

    statement = "mathtools.partition_integer_by_ratio('foo', [1, 1, 1])"
    assert pytest.raises(TypeError, statement)
