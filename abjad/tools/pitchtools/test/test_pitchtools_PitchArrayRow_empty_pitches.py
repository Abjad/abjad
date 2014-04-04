# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayRow_empty_pitches_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[1].cells[2].pitches.append(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    array[0].empty_pitches()

    '''
    [] [      ] [  ]
    [      ] [] [e']
    '''

    assert array[0].dimensions == (1, 4)
    assert array[0].cell_widths == (1, 2, 1)
    assert array[0].pitches == ()