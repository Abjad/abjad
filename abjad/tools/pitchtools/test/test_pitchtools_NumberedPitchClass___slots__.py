# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitchClass___slots___01():
    r'''Numbered pitch-classes are immutable.
    '''

    numbered_pitch_class = pitchtools.NumberedPitchClass(1)
    assert pytest.raises(AttributeError, "numbered_pitch_class.foo = 'bar'")
