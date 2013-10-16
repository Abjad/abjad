# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitch___int___01():
    r'''Return pitch number of 12-ET numbered pitch as int.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13)
    assert isinstance(int(numbered_pitch), int)
    assert int(numbered_pitch) == 13


def test_NumberedPitch___int___02():
    r'''Raise type error on non-12-ET numbered pitch.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13.5)
    assert py.test.raises(TypeError, 'int(numbered_pitch)')
