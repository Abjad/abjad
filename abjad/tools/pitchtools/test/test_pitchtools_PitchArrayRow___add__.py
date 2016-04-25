# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayRow___add___01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(0)
    array[0].cells[1].append_pitch(2)
    array[1].cells[2].append_pitch(4)

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
