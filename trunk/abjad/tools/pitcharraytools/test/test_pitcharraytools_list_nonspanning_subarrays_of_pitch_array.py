from abjad import *
from abjad.tools import pitcharraytools


def test_pitcharraytools_list_nonspanning_subarrays_of_pitch_array_01():

    array = pitcharraytools.PitchArray([
        [2, 2, 3, 1],
        [1, 2, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])

    '''
    [      ] [      ] [            ] []
    [] [      ] [] [] [      ] []
    [] [] [] [] [] [] [] []
    '''

    subarrays = pitcharraytools.list_nonspanning_subarrays_of_pitch_array(array)

    '''
    [      ] [      ]
    [] [      ] []
    [] [] [] []
    '''

    assert subarrays[0] == pitcharraytools.PitchArray(
        [[2, 2], [1, 2, 1], [1, 1, 1, 1]])

    '''
    [            ]
    [] [      ]
    [] [] []
    '''

    assert subarrays[1] == pitcharraytools.PitchArray([[3], [1, 2], [1, 1, 1]])

    '''
    []
    []
    []
    '''

    assert subarrays[2] == pitcharraytools.PitchArray([[1], [1], [1]])
