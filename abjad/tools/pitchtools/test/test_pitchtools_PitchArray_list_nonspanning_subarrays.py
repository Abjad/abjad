# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray_list_nonspanning_subarrays_01():

    array = pitchtools.PitchArray([
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

    assert subarrays[0] == pitchtools.PitchArray(
        [[2, 2], [1, 2, 1], [1, 1, 1, 1]])

    '''
    [            ]
    [] [      ]
    [] [] []
    '''

    assert subarrays[1] == pitchtools.PitchArray([[3], [1, 2], [1, 1, 1]])

    '''
    []
    []
    []
    '''

    assert subarrays[2] == pitchtools.PitchArray([[1], [1], [1]])
