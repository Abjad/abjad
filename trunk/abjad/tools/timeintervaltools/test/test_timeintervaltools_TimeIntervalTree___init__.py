# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTree___init___01():
    r'''TimeIntervalTree can be initialized without arguments.
    '''
    tree = TimeIntervalTree([])


def tree_TimeIntervalTree___init___02():
    r'''TimeIntervalTree can be instantiated from time_interval_1 single TimeInterval.
    '''
    time_interval_1 = TimeInterval(0, 10)
    tree = TimeIntervalTree(time_interval_1)
    assert time_interval_1 in tree


def tree_TimeIntervalTree___init___03():
    r'''TimeIntervalTree can be instantiated from time_interval_1 single TimeIntervalTree.
    '''
    time_interval_1 = TimeInterval(0, 10)
    timeintervaltree = TimeIntervalTree(time_interval_1)
    tree = TimeIntervalTree(timeintervaltree)
    assert time_interval_1 in tree


def test_timeintervaltools_TimeIntervalTree___init___02():
    r'''TimeIntervalTree can be initialized from time_interval_1 list of TimeIntervals.
    '''
    time_interval_1 = TimeInterval(0, 10, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(5, 15, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(10, 25, {'time_interval_3': 3})
    tree = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert all(block in tree for block in [time_interval_1, time_interval_2, time_interval_3])


def test_timeintervaltools_TimeIntervalTree___init___03():
    r'''TimeIntervalTree can be initialized from time_interval_1 list of TimeIntervals.
    '''
    time_interval_1 = TimeInterval(0, 10, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(5, 15, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(10, 25, {'time_interval_3': 3})
    tree = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])


def test_timeintervaltools_TimeIntervalTree___init___04():
    r'''TimeIntervalTree recursively flattens its input argument,
    allowinging instantiation from any nested collection of
    TimeIntervals and / or trees.'''
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(5, 15)
    timeintervaltree = TimeIntervalTree([time_interval_1, time_interval_2])
    time_interval_3 = TimeInterval(21, 23)
    time_interval_4 = TimeInterval(2001, 2009)
    tree = TimeIntervalTree([time_interval_1, time_interval_2, [time_interval_3, time_interval_4], [[timeintervaltree]]])
    assert [x.signature for x in tree] == \
        [(0, 10), (0, 10), (5, 15), (5, 15), (21, 23), (2001, 2009)]
