# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitch___slots___01():
    r'''Numbered pitches are immutable.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13)
    assert pytest.raises(AttributeError, "numbered_pitch.foo = 'bar'")
