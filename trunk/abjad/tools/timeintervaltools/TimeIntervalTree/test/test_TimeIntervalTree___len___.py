from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___len____01():
    '''TimeIntervalTree containing no TimeIntervals report 0 length.'''
    tree = TimeIntervalTree([])
    assert len(tree) == 0


def test_TimeIntervalTree___len____02():
    '''TimeIntervalTree reports total count of TimeIntervals contained.'''
    block_a = TimeInterval(0, 5, {'a': 1})
    block_b = TimeInterval(0, 10, {'b': 2})
    block_c = TimeInterval(5, 20, {'c': 3})
    tree = TimeIntervalTree([block_a, block_b, block_c])
    assert len(tree) == 3
