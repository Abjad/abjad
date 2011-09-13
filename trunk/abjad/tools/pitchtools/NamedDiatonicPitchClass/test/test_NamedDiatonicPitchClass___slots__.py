from abjad import *
import py.test


def test_NamedDiatonicPitchClass___slots___01():
    '''Named diatonic pitch-classes are immutable.
    '''

    named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass('c')
    assert py.test.raises(AttributeError, "named_diatonic_pitch_class.foo = 'bar'")
