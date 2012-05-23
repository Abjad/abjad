from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayRow___iadd___01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[1].cells[2].pitches.append(4)

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
    assert row.pitches == tuple(pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, 0, 2]))
