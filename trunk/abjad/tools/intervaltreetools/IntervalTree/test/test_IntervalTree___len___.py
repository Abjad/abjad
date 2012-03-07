from abjad.tools.intervaltreetools import *


def test_IntervalTree___len____01():
    '''IntervalTree containing no TimeIntervals report 0 length.'''
    tree = IntervalTree([])
    assert len(tree) == 0


def test_IntervalTree___len____02():
    '''IntervalTree reports total count of TimeIntervals contained.'''
    block_a = TimeInterval(0, 5, {'a': 1})
    block_b = TimeInterval(0, 10, {'b': 2})
    block_c = TimeInterval(5, 20, {'c': 3})
    tree = IntervalTree([block_a, block_b, block_c])
    assert len(tree) == 3
