from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell
import py.test


def test_PitchArrayCell_next_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0][1].next is array[0][3]


def test_PitchArrayCell_next_02():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert py.test.raises(IndexError, 'array[0][-1].next')


def test_PitchArrayCell_next_03():

    cell = PitchArrayCell([pitchtools.NamedChromaticPitch(1)])

    assert py.test.raises(IndexError, 'cell.next')
