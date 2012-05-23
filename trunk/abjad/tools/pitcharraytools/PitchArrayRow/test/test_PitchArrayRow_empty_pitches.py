from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayRow_empty_pitches_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
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
