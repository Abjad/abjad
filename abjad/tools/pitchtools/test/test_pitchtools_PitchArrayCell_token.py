# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayCell_token_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(NamedPitch(0))
    array[0].cells[1].pitches.extend([NamedPitch(2), NamedPitch(4)])

    '''
    [c'] [d' e'     ] []
    [             ] [] []
    '''

    assert array[0].cells[0].item == ('c', 4)
    assert array[0].cells[1].item == ([('d', 4), ('e', 4)], 2)
    assert array[0].cells[2].item == 1

    assert array[1].cells[0].item == 2
    assert array[1].cells[1].item == 1
    assert array[1].cells[2].item == 1