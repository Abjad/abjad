from abjad import *
import py.test


def testNumberedObjectChromaticPitchClass___slots___01():
    '''Numbered chromatic pitch-classes are immutable.
    '''

    numbered_chromatic_pitch_class = pitchtools.NumberedChromaticPitchClass(1)
    assert py.test.raises(AttributeError, "numbered_chromatic_pitch_class.foo = 'bar'")
