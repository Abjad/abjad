from abjad import *
import py.test


def test_NamedChromaticPitchClassSegment___slots___01():

    named_chromatic_pitch_class_segment = pitchtools.NamedChromaticPitchClassSegment([
        'gs', 'a', 'as', 'c', 'cs'])
    assert py.test.raises(AttributeError, "named_chromatic_pitch_class_segment.foo = 'bar'")
