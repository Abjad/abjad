# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import TimeInterval, TimeIntervalTree


def test_timeintervaltools_TimeIntervalTree__format___01():

    a = TimeInterval(Offset(-1, 1), Offset(3, 1), {
        'a': 1, 'b': 2, 't': TimeInterval(Offset(2, 1), Offset(3, 1), {'x': 'b'})})
    b = TimeInterval(Offset(0, 1), Offset(1, 1), {'x': 'y'})
    tree = TimeIntervalTree([a, b])

    assert testtools.compare(
        format(tree),
        r'''
        timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                Offset(-1, 1),
                Offset(3, 1),
                {
                    'a': 1,
                    'b': 2,
                    't': timeintervaltools.TimeInterval(
                        Offset(2, 1),
                        Offset(3, 1),
                        {
                            'x': 'b',
                        }),
                }),
            timeintervaltools.TimeInterval(
                Offset(0, 1),
                Offset(1, 1),
                {
                    'x': 'y',
                }),
            ])
        '''
        )
