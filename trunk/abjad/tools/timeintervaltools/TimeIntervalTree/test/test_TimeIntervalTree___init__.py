from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___init___01():
    '''TimeIntervalTree can be initialized without arguments.'''
    tree = TimeIntervalTree([])


def tree_TimeIntervalTree___init___02():
    '''TimeIntervalTree can be instantiated from a single TimeInterval.'''
    a = TimeInterval(0, 10)
    tree = TimeIntervalTree(a)
    assert a in tree


def tree_TimeIntervalTree___init___03():
    '''TimeIntervalTree can be instantiated from a single TimeIntervalTree.'''
    a = TimeInterval(0, 10)
    t = TimeIntervalTree(a)
    tree = TimeIntervalTree(t)
    assert a in tree


def test_TimeIntervalTree___init___02():
    '''TimeIntervalTree can be initialized from a list of TimeIntervals.'''
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(5, 15, {'b': 2})
    c = TimeInterval(10, 25, {'c': 3})
    tree = TimeIntervalTree([a, b, c])
    assert all([block in tree for block in [a, b, c]])


def test_TimeIntervalTree___init___03():
    '''TimeIntervalTree can be initialized from a list of TimeIntervals.'''
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(5, 15, {'b': 2})
    c = TimeInterval(10, 25, {'c': 3})
    tree = TimeIntervalTree([a, b, c])


def test_TimeIntervalTree___init___04():
    '''TimeIntervalTree recursively flattens its input argument,
    allowinging instantiation from any nested collection of
    TimeIntervals and / or trees.'''
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    t = TimeIntervalTree([a, b])
    c = TimeInterval(21, 23)
    d = TimeInterval(2001, 2009)
    tree = TimeIntervalTree([a, b, [c, d], [[t]]])
    assert [x.signature for x in tree] == \
        [(0, 10), (0, 10), (5, 15), (5, 15), (21, 23), (2001, 2009)]
