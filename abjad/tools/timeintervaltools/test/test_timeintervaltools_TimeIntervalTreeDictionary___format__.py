# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTreeDictionary___format___01():

    a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
    b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
    c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
    d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])

    treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

    assert systemtools.TestManager.compare(
        format(treedict),
        r'''
        timeintervaltools.TimeIntervalTreeDictionary({
            'a': timeintervaltools.TimeIntervalTree([
                timeintervaltools.TimeInterval(
                    Offset(0, 1),
                    Offset(1, 1),
                    {
                        'name': 'a',
                    }),
                ]),
            'c': timeintervaltools.TimeIntervalTree([
                timeintervaltools.TimeInterval(
                    Offset(0, 1),
                    Offset(3, 1),
                    {
                        'name': 'c',
                    }),
                ]),
            'b': timeintervaltools.TimeIntervalTree([
                timeintervaltools.TimeInterval(
                    Offset(1, 1),
                    Offset(2, 1),
                    {
                        'name': 'b',
                    }),
                ]),
            'd': timeintervaltools.TimeIntervalTree([
                timeintervaltools.TimeInterval(
                    Offset(2, 1),
                    Offset(3, 1),
                    {
                        'name': 'd',
                    }),
                ]),
            })
        '''
        )
