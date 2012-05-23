from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitchClassSegment


def test_NumberedChromaticPitchClassSegment___repr___01():
    '''Numbered chromatic pitch-class segment repr is evaluable.
    '''

    cpns = [-2, -1.5, 6, 7, -1.5, 7]
    numbered_chromatic_pitch_class_segment_1 = pitchtools.NumberedChromaticPitchClassSegment(cpns)
    numbered_chromatic_pitch_class_segment_2 = eval(repr(numbered_chromatic_pitch_class_segment_1))

    assert isinstance(numbered_chromatic_pitch_class_segment_1, NumberedChromaticPitchClassSegment)
    assert isinstance(numbered_chromatic_pitch_class_segment_2, NumberedChromaticPitchClassSegment)
