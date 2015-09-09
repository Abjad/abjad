# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_PitchArrayCell_next_01():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert getattr(array[0][1], 'next') is array[0][3]


def test_pitchtools_PitchArrayCell_next_02():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert pytest.raises(IndexError, 'array[0][-1].next')


def test_pitchtools_PitchArrayCell_next_03():

    cell = pitchtools.PitchArrayCell([NamedPitch(1)])

    assert pytest.raises(IndexError, 'cell.next')
