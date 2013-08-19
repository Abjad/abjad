# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NamedChromticPitchSegment___slots___01():

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_segment = pitchtools.NamedPitchSegment(ncps)

    assert py.test.raises(AttributeError, "named_chromatic_pitch_segment.foo = 'bar'")
