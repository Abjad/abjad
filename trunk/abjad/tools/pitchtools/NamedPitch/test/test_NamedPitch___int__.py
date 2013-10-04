# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedPitch___int___01():
    r'''Return chromatic pitch number of 12-ET named chromatic pitch as int.
    '''

    named_pitch = pitchtools.NamedPitch(13)
    assert isinstance(int(named_pitch), int)
    assert int(named_pitch) == 13


def test_NamedPitch___int___02():
    r'''Raise type error on non-12-ET named chromatic pitch.
    '''

    named_pitch = pitchtools.NamedPitch(13.5)
    assert py.test.raises(TypeError, 'int(named_pitch)')
