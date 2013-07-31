from abjad import *
import py.test


def test_NumberedDiatonicPitchClass___slots___01():
    r'''Numbered diatonic pitch-classes are immutable.
    '''

    numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(0)
    assert py.test.raises(AttributeError, "numbered_diatonic_pitch_class.foo = 'bar'")
