# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitch___int___01():
    r'''Returns pitch number of 12-ET numbered pitch as int.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13)
    assert isinstance(int(numbered_pitch), int)
    assert int(numbered_pitch) == 13


def test_pitchtools_NumberedPitch___int___02():
    r'''Raise type error on non-12-ET numbered pitch.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13.5)
    assert pytest.raises(TypeError, 'int(numbered_pitch)')
