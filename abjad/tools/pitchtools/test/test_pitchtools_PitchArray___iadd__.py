# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray___iadd___01():

    array_1 = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    array_2 = pitchtools.PitchArray([[3, 4], [4, 3]])

    '''
    [      ] [       ]
    [       ] [      ]
    '''

    array_3 = pitchtools.PitchArray([[1, 1], [1, 1]])

    '''
    [] []
    [] []
    '''

    array_1 += array_2
    array_1 += array_3

    '''
    [] [      ] [] [      ] [       ] [] []
    [      ] [] [] [       ] [      ] [] []
    '''

    assert array_1.dimensions == (2, 13)
    assert array_1.cell_widths_by_row == (
        (1, 2, 1, 3, 4, 1, 1), (2, 1, 1, 4, 3, 1, 1))
    assert array_1.pitches_by_row == ((), ())
