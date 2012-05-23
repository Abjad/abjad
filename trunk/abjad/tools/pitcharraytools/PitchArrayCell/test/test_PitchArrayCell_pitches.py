from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell


def test_PitchArrayCell_pitches_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(pitchtools.NamedChromaticPitch(0))
    array[0].cells[1].pitches.append(pitchtools.NamedChromaticPitch(2))

    '''
    [c'] [d'     ] []
    [         ] [] []
    '''

    assert array[0].cells[0].pitches == [pitchtools.NamedChromaticPitch(0)]
    assert array[0].cells[1].pitches == [pitchtools.NamedChromaticPitch(2)]
    assert array[0].cells[2].pitches == []

    assert array[1].cells[0].pitches == []
    assert array[1].cells[1].pitches == []
    assert array[1].cells[2].pitches == []


def test_PitchArrayCell_pitches_02():

    cell = PitchArrayCell([pitchtools.NamedChromaticPitch(0)])

    assert cell.pitches == [pitchtools.NamedChromaticPitch(0)]
