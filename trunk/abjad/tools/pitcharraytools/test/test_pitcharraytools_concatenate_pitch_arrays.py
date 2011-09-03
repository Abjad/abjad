from abjad import *
from abjad.tools import pitcharraytools


def test_pitcharraytools_concatenate_pitch_arrays_01():

    array_1 = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    array_2 = pitcharraytools.PitchArray([[3, 4], [4, 3]])

    '''
    [      ] [       ]
    [       ] [      ]
    '''

    array_3 = pitcharraytools.PitchArray([[1, 1], [1, 1]])

    '''
    [] []
    [] []
    '''

    merged_array = pitcharraytools.concatenate_pitch_arrays([array_1, array_2, array_3])

    '''
    [] [      ] [] [      ] [       ] [] []
    [      ] [] [] [       ] [      ] [] []
    '''

    assert merged_array.dimensions == (2, 13)
    assert merged_array.cell_widths_by_row == (
        (1, 2, 1, 3, 4, 1, 1), (2, 1, 1, 4, 3, 1, 1))
    assert merged_array.pitches_by_row == ((), ())
