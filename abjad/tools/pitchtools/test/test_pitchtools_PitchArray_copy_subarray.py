# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArray_copy_subarray_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(0)
    array[0].cells[1].append_pitch(2)
    array[1].cells[2].append_pitch(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    subarray = array.copy_subarray((0, 0), (2, 2))

    '''
    [c'] [d']
    [         ]
    '''

    assert subarray.dimensions == (2, 2)
    assert subarray.cell_widths_by_row == ((1, 1), (2,))
    assert subarray.pitches_by_row == (
        (NamedPitch(0), NamedPitch(2)),
        (),
        )
