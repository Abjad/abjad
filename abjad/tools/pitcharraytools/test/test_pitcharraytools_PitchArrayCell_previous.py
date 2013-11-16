# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_pitcharraytools_PitchArrayCell_previous_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0][1].prev is array[0][0]


def test_pitcharraytools_PitchArrayCell_previous_02():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert pytest.raises(IndexError, 'array[0][0].prev')


def test_pitcharraytools_PitchArrayCell_previous_03():

    cell = pitcharraytools.PitchArrayCell([NamedPitch(1)])

    assert pytest.raises(IndexError, 'cell.prev')
