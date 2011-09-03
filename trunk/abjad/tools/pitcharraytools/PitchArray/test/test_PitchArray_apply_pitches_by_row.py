from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArray_apply_pitches_by_row_01():

    array = pitcharraytools.PitchArray([
        [1, (0, 1), (0, 2)],
        [(0, 2), (0, 1), 1],
        ])

    '''
    [  ] [c'] [c'     ]
    [c'      ] [c'] []
    '''

    array.apply_pitches_by_row([[-2, -1.5], [7, 6]])

    '''
    [  ] [bf] [bqf     ]
    [c'      ] [c' ] []
    '''

    assert array.dimensions == (2, 4)
    assert array.cell_widths_by_row == ((1, 1, 2), (2, 1, 1))
    assert array.pitches_by_row == (
        (pitchtools.NamedChromaticPitch('bf', 3), pitchtools.NamedChromaticPitch('bqf', 3)), (pitchtools.NamedChromaticPitch('g', 4), pitchtools.NamedChromaticPitch('fs', 4)))
