from abjad import *
import py.test


def testNumberedObjectChromaticPitch___slots___01():
    '''Numbered chromatic pitches are immutable.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedChromaticPitch(13)
    assert py.test.raises(AttributeError, "numbered_chromatic_pitch.foo = 'bar'")
