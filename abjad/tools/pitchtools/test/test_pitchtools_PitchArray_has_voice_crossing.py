# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray_has_voice_crossing_01():

    array = pitchtools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert array.has_voice_crossing
