from abjad import *
import py.test


def test_NamedChromaticPitchClassSet___slots___01():
    '''Named chromatic pitch-class set can not be changed after initialization.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_set = pitchtools.NamedChromaticPitchClassSet(ncpcs)

    assert py.test.raises(AttributeError, "named_chromatic_pitch_class_set.foo = 'bar'")
