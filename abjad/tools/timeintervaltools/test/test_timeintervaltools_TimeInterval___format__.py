# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeInterval___format___01():

    t = timeintervaltools.TimeInterval(0, 1, {
        'a': timeintervaltools.TimeInterval(3, 4, {'x': 'y'}), 'b': 3
    })

    assert systemtools.TestManager.compare(
        format(t),
        r'''
        timeintervaltools.TimeInterval(
            Offset(0, 1),
            Offset(1, 1),
            {
                'a': timeintervaltools.TimeInterval(
                    Offset(3, 1),
                    Offset(4, 1),
                    {
                        'x': 'y',
                    }),
                'b': 3,
            })
        '''
        )
