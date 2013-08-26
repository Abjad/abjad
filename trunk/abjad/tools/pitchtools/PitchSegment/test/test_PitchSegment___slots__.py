# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_PitchSegment___slots___01():

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_pitch_segment = pitchtools.PitchSegment(ncps)

    assert py.test.raises(AttributeError, "named_pitch_segment.foo = 'bar'")
