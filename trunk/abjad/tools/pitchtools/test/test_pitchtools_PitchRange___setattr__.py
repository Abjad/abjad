# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_PitchRange___setattr___01():
    r'''Pitch ranges are immutable.
    '''

    pitch_range = pitchtools.PitchRange(-12, 36)

    assert py.test.raises(AttributeError, "pitch_range.foo = 'bar'")
