from abjad import *


def test_PitchArray_list_nonspanning_subarrays_01():

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

    subarrays = array.list_nonspanning_subarrays()

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
