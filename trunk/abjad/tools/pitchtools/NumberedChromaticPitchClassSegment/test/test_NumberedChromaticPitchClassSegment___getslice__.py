from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitchClassSegment


def test_NumberedChromaticPitchClassSegment___getslice___01():
    '''Return new numbered chromatic pitch-class segment.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = NumberedChromaticPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = numbered_chromatic_pitch_class_segment_1[:2]

    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedChromaticPitchClassSegment)
    assert numbered_chromatic_pitch_class_segment_2 == NumberedChromaticPitchClassSegment(cpns[:2])


def test_NumberedChromaticPitchClassSegment___getslice___02():
    '''Return new numbered chromatic pitch-class segment.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = NumberedChromaticPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = numbered_chromatic_pitch_class_segment_1[-2:]

    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedChromaticPitchClassSegment)
    assert numbered_chromatic_pitch_class_segment_2 == NumberedChromaticPitchClassSegment(cpns[-2:])
