from abjad import *
import py.test


def test_NumberedDiatonicPitch___setattr___01():
    r'''Slots constrain numbere diatonic pitch attributes.
    '''

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
    assert py.test.raises(AttributeError, "numbered_diatonic_pitch.foo = 'bar'")
