from abjad import *
import py.test


def test_NamedChromaticPitchClass___slots___01():

    named_chromatic_pitch_class = pitchtools.NamedChromaticPitchClass("cs")
    assert py.test.raises(AttributeError, "named_chromatic_pitch_class.foo = 'bar'")
