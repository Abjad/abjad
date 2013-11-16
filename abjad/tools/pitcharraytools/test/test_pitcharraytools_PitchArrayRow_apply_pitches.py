# -*- encoding: utf-8 -*-
from abjad import *


def test_pitcharraytools_PitchArrayRow_apply_pitches_01():

    array = pitcharraytools.PitchArray([
        [1, (0, 1), (0, 2)],
        [(0, 2), (0, 1), 1],
        ])

    '''
    [  ] [c'] [c'     ]
    [c'      ] [c'] []
    '''

    array[0].apply_pitches([-2, -1.5])

    '''
    [  ] [bf] [bqf     ]
    [c'      ] [c' ] []
    '''

    assert array[0].dimensions == (1, 4)
    assert array[0].cell_widths == (1, 1, 2)
    assert array[0].pitches == (NamedPitch(-2), NamedPitch(-1.5))
