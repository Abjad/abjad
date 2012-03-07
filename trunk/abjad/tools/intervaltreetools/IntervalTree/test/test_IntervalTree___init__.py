from abjad.tools.intervaltreetools import *


def test_IntervalTree___init___01():
    '''IntervalTree can be initialized without arguments.'''
    tree = IntervalTree([])


def tree_IntervalTree___init___02():
    '''IntervalTree can be instantiated from a single TimeInterval.'''
    a = TimeInterval(0, 10)
    tree = IntervalTree(a)
    assert a in tree


def tree_IntervalTree___init___03():
    '''IntervalTree can be instantiated from a single IntervalTree.'''
    a = TimeInterval(0, 10)
    t = IntervalTree(a)
    tree = IntervalTree(t)
    assert a in tree


def test_IntervalTree___init___02():
    '''IntervalTree can be initialized from a list of TimeIntervals.'''
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(5, 15, {'b': 2})
    c = TimeInterval(10, 25, {'c': 3})
    tree = IntervalTree([a, b, c])
    assert all([block in tree for block in [a, b, c]])


def test_IntervalTree___init___03():
    '''IntervalTree can be initialized from a list of TimeIntervals.'''
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(5, 15, {'b': 2})
    c = TimeInterval(10, 25, {'c': 3})
    tree = IntervalTree([a, b, c])


def test_IntervalTree___init___04():
    '''IntervalTree recursively flattens its input argument,
    allowinging instantiation from any nested collection of
    TimeIntervals and / or trees.'''
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    t = IntervalTree([a, b])
    c = TimeInterval(21, 23)
    d = TimeInterval(2001, 2009)
    tree = IntervalTree([a, b, [c, d], [[t]]])
    assert [x.signature for x in tree] == \
        [(0, 10), (0, 10), (5, 15), (5, 15), (21, 23), (2001, 2009)]
