from abjad import *
import py.test


def testNumberedObjectDiatonicPitch___setattr___01():
    '''Slots constrain numbere diatonic pitch attributes.
    '''

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
    assert py.test.raises(AttributeError, "numbered_diatonic_pitch.foo = 'bar'")
