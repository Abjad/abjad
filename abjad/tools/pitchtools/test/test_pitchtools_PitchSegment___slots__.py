# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_PitchSegment___slots___01():

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_pitch_segment = pitchtools.PitchSegment(ncps)

    assert pytest.raises(AttributeError, "named_pitch_segment.foo = 'bar'")
