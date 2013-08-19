# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayCell_width_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(pitchtools.NamedPitch(0))
    array[0].cells[1].pitches.extend([pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)])

    '''
    [c'] [d' e'     ] []
    [             ] [] []
    '''

    assert array[0].cells[0].width == 1
    assert array[0].cells[1].width == 2
    assert array[0].cells[2].width == 1

    assert array[1].cells[0].width == 2
    assert array[1].cells[1].width == 1
    assert array[1].cells[2].width == 1
