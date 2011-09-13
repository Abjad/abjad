from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitchClassSegment


def test_NamedChromaticPitchClassSegment___repr___01():
    '''Named chromatic pitch-class segment repr is evaluable.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_segment_1 = pitchtools.NamedChromaticPitchClassSegment(ncpcs)
    named_chromatic_pitch_class_segment_2 = eval(repr(named_chromatic_pitch_class_segment_1))

    assert isinstance(named_chromatic_pitch_class_segment_1, NamedChromaticPitchClassSegment)
    assert isinstance(named_chromatic_pitch_class_segment_2, NamedChromaticPitchClassSegment)
