# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayRow_copy_subrow_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[1].cells[2].pitches.append(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    subrow = array[0].copy_subrow(2, None)

    '''
    [d'] []
    '''

    assert subrow.dimensions == (1, 2)
    assert subrow.cell_widths == (1, 1)
    assert subrow.pitches == (NamedPitch('d', 4), )
    assert subrow.parent_array is None