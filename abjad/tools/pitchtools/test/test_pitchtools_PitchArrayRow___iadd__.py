# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayRow___iadd___01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(0)
    array[0].cells[1].append_pitch(2)
    array[1].cells[2].append_pitch(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    row = array[0].withdraw()
    row += row

    '''
    [c'] [d'] [] [c'] [d'] []
    '''

    assert row.cell_widths == (1, 2, 1, 1, 2, 1)
    assert row.dimensions == (1, 8)
    assert row.pitches == tuple([NamedPitch(x) for x in [0, 2, 0, 2]])
