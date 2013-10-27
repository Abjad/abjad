# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_PitchClassSegment___slots___01():

    pitch_class_segment = pitchtools.PitchClassSegment([
        'gs', 'a', 'as', 'c', 'cs'])
    assert py.test.raises(AttributeError, "pitch_class_segment.foo = 'bar'")


def test_pitchtools_PitchClassSegment___slots___02():

    pitch_class_tokens = [-2, -1.5, 6, 7, -1.5, 7]
    pitch_class_segment = pitchtools.PitchClassSegment(pitch_class_tokens)
    assert py.test.raises(AttributeError, "pitch_class_segment.foo = 'bar'")
