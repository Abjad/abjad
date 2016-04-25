# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayCell_is_first_in_row_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0].cells[0].is_first_in_row
    assert not array[0].cells[1].is_first_in_row
    assert not array[0].cells[2].is_first_in_row

    assert array[1].cells[0].is_first_in_row
    assert not array[1].cells[1].is_first_in_row
    assert not array[1].cells[2].is_first_in_row



def test_pitchtools_PitchArrayCell_is_first_in_row_02():

    cell = pitchtools.PitchArrayCell([NamedPitch(1)])

    assert not cell.is_first_in_row
