# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitchtools_NumberedPitch___slots___01():
    r'''Numbered pitches are immutable.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13)
    assert pytest.raises(AttributeError, "numbered_pitch.foo = 'bar'")
