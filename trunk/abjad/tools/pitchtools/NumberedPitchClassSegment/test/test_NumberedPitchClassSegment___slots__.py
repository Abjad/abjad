# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitchClassSegment___slots___01():
    r'''Numbered chromatic pitch-class segments are immutable.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment = pitchtools.NumberedPitchClassSegment(cpns)

    assert py.test.raises(AttributeError, "numbered_chromatic_pitch_class_segment.foo = 'bar'")
