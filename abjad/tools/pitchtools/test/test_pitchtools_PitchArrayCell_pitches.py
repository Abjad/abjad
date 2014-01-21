# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayCell_pitches_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(NamedPitch(0))
    array[0].cells[1].pitches.append(NamedPitch(2))

    '''
    [c'] [d'     ] []
    [         ] [] []
    '''

    assert array[0].cells[0].pitches == [NamedPitch(0)]
    assert array[0].cells[1].pitches == [NamedPitch(2)]
    assert array[0].cells[2].pitches == []

    assert array[1].cells[0].pitches == []
    assert array[1].cells[1].pitches == []
    assert array[1].cells[2].pitches == []


def test_pitchtools_PitchArrayCell_pitches_02():

    cell = pitchtools.PitchArrayCell([NamedPitch(0)])

    assert cell.pitches == [NamedPitch(0)]
