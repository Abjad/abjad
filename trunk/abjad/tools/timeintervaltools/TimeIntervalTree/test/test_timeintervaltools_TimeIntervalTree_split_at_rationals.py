# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_split_at_rationals_01():

    t1 = timeintervaltools.TimeInterval(0, 8, {'name': 't1'})
    t2 = timeintervaltools.TimeInterval(2, 6, {'name': 't2'})
    t3 = timeintervaltools.TimeInterval(4, 12, {'name': 't3'})

    tree = timeintervaltools.TimeIntervalTree([t1, t2, t3])

    result = tree.split_at_rationals(4)
    assert 2 == len(result)
    assert all(isinstance(x, type(tree)) for x in result)

    result_1, result_2 = result
    assert 2 == len(result_1)
    assert 3 == len(result_2)

    assert result_1[0] == timeintervaltools.TimeInterval(0, 4, {'name': 't1'})
    assert result_1[1] == timeintervaltools.TimeInterval(2, 4, {'name': 't2'})

    assert result_2[0] == timeintervaltools.TimeInterval(4, 6, {'name': 't2'})
    assert result_2[1] == timeintervaltools.TimeInterval(4, 8, {'name': 't1'})
    assert result_2[2] == timeintervaltools.TimeInterval(4, 12, {'name': 't3'})


def test_timeintervaltools_TimeIntervalTree_split_at_rationals_02():

    t1 = timeintervaltools.TimeInterval(0, 8, {'name': 't1'})
    t2 = timeintervaltools.TimeInterval(2, 6, {'name': 't2'})
    t3 = timeintervaltools.TimeInterval(4, 12, {'name': 't3'})

    tree = timeintervaltools.TimeIntervalTree([t1, t2, t3])

    result = tree.split_at_rationals(0, 2, 4, 6, 8, 12)

    assert result == tuple([
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(Offset(0, 1), Offset(2, 1), {'name': 't1'})
        ]),
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 't1'}),
            timeintervaltools.TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 't2'})
        ]),
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 't1'}),
            timeintervaltools.TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 't2'}),
            timeintervaltools.TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 't3'})
        ]),
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(Offset(6, 1), Offset(8, 1), {'name': 't1'}),
            timeintervaltools.TimeInterval(Offset(6, 1), Offset(8, 1), {'name': 't3'})
        ]),
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(Offset(8, 1), Offset(12, 1), {'name': 't3'})
        ])
    ])


def test_timeintervaltools_TimeIntervalTree_split_at_rationals_03():
    splits = [-1, 16]
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    split = timeintervaltools.TimeIntervalTree(tree.split_at_rationals(splits))
    assert tree[:] == split[:]
