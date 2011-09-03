from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayCell_pitches_append_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[0].cells[2].pitches.append(4)

    '''
    [c'] [d'     ] [e']
    [         ] [] [  ]
    '''

    assert array[0].cells[0].pitches == [pitchtools.NamedChromaticPitch(0)]
    assert array[0].cells[1].pitches == [pitchtools.NamedChromaticPitch(2)]
    assert array[0].cells[2].pitches == [pitchtools.NamedChromaticPitch(4)]
