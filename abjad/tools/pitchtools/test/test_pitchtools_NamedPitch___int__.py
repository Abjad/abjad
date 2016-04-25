# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NamedPitch___int___01():
    r'''Returns pitch number of 12-ET named pitch as int.
    '''

    named_pitch = NamedPitch(13)
    assert isinstance(int(named_pitch), int)
    assert int(named_pitch) == 13


def test_pitchtools_NamedPitch___int___02():
    r'''Raise type error on non-12-ET named pitch.
    '''

    named_pitch = NamedPitch(13.5)
    assert pytest.raises(TypeError, 'int(named_pitch)')
