# -*- encoding: utf-8 -*-
from abjad import *


def test_pitcharraytools_PitchArrayCell_is_last_in_row_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert not array[0].cells[0].is_last_in_row
    assert not array[0].cells[1].is_last_in_row
    assert array[0].cells[2].is_last_in_row

    assert not array[1].cells[0].is_last_in_row
    assert not array[1].cells[1].is_last_in_row
    assert array[1].cells[2].is_last_in_row



def test_pitcharraytools_PitchArrayCell_is_last_in_row_02():

    cell = pitcharraytools.PitchArrayCell([NamedPitch(1)])

    assert not cell.is_last_in_row
