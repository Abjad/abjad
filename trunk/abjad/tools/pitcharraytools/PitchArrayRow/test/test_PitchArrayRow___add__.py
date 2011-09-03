from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayRow___add___01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[1].cells[2].pitches.append(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    new_row = array[0] + array[1]

    '''
    [c'] [d'] [] [] [] [e']
    '''

    assert new_row.parent_array is None
    assert new_row.cell_widths == (1, 2, 1, 2, 1, 1)
    assert new_row.depth == 1
    assert new_row.width == 8
