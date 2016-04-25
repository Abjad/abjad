# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_PitchRange___setattr___01():
    r'''Pitch ranges are immutable.
    '''

    pitch_range = pitchtools.PitchRange.from_pitches(-12, 36)

    assert pytest.raises(AttributeError, "pitch_range.foo = 'bar'")
