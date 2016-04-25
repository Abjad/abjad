# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayColumn_start_pitches_01():

    array = pitchtools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    array.columns[0].start_pitches == (NamedPitch(7), )
    array.columns[1].start_pitches == (NamedPitch(2), )
    array.columns[2].start_pitches == (
        NamedPitch(-2), NamedPitch(-1.5), NamedPitch(6))
    array.columns[3].start_pitches == ()
