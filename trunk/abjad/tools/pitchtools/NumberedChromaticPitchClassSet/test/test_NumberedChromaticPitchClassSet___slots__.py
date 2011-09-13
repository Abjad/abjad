from abjad import *
import py.test


def test_NumberedChromaticPitchClassSet___slots___01():
    '''Numbered chromatic pitch-class sets are immutable.
    '''

    numbered_chromatic_pitch_class_set = pitchtools.NumberedChromaticPitchClassSet([6, 7, 10, 10.5])
    assert py.test.raises(AttributeError, "numbered_chromatic_pitch_class_set.foo = 'bar'")
