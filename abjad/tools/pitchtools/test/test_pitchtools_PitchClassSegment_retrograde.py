# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_retrograde_01():

    pitch_class_segment_1 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('g'),])

    pitch_class_segment_2 = pitchtools.PitchClassSegment([
        pitchtools.NamedPitchClass('g'),
        pitchtools.NamedPitchClass('f'),
        pitchtools.NamedPitchClass('e'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('c'),])

    assert pitch_class_segment_1.retrograde() == pitch_class_segment_2
    assert pitch_class_segment_2.retrograde() == pitch_class_segment_1


def test_pitchtools_PitchClassSegment_retrograde_02():

    pitch_class_segment= pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])

    assert pitch_class_segment.retrograde() == \
        pitchtools.PitchClassSegment([2, 9, 4, 10, 6, 0])
