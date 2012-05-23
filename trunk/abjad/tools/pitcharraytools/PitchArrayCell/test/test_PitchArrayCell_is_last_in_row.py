from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell


def test_PitchArrayCell_is_last_in_row_01():

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



def test_PitchArrayCell_is_last_in_row_02():

    cell = PitchArrayCell([pitchtools.NamedChromaticPitch(1)])

    assert not cell.is_last_in_row
