# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray_to_measures_01():

    array = pitchtools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    measures = array.to_measures()
    score = Score(Staff([]) * 2)
    score[0].append(measures[0])
    score[1].append(measures[1])

    r'''
    \new Score <<
        \new Staff {
            {
                \time 4/8
                r8
                d'8
                <bf bqf>4
            }
        }
        \new Staff {
            {
                \time 4/8
                g'4
                fs'8
                r8
            }
        }
    >>
    '''

    assert inspect_(score).is_well_formed()
    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                {
                    \time 4/8
                    r8
                    d'8
                    <bf bqf>4
                }
            }
            \new Staff {
                {
                    \time 4/8
                    g'4
                    fs'8
                    r8
                }
            }
        >>
        '''
        )
