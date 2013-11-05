# -*- encoding: utf-8 -*-
from abjad import *


def test_pitcharraytools_PitchArrayRow_to_measure_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    measure = array.rows[0].to_measure()

    r'''
    {
        \time 4/8
        r8
        d'8
        <bf bqf>4
    }
    '''

    assert inspect(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 4/8
            r8
            d'8
            <bf bqf>4
        }
        '''
        )
