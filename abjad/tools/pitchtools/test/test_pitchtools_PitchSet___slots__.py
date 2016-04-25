# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_PitchSet___slots___01():
    r'''Named pitch sets are immutable.
    '''

    pitch_classes = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    pitch_set = pitchtools.PitchSet(pitch_classes)

    assert pytest.raises(AttributeError, "pitch_set.foo = 'bar'")
