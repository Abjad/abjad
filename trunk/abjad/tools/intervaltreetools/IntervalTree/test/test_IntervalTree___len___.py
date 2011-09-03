from abjad.tools.intervaltreetools import *


def test_IntervalTree___len____01():
    '''IntervalTree containing no BoundedIntervals report 0 length.'''
    tree = IntervalTree([])
    assert len(tree) == 0


def test_IntervalTree___len____02():
    '''IntervalTree reports total count of BoundedIntervals contained.'''
    block_a = BoundedInterval(0, 5, {'a': 1})
    block_b = BoundedInterval(0, 10, {'b': 2})
    block_c = BoundedInterval(5, 20, {'c': 3})
    tree = IntervalTree([block_a, block_b, block_c])
    assert len(tree) == 3
