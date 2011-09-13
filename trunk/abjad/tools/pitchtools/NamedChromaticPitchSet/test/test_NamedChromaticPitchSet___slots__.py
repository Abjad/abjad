from abjad import *
import py.test


def test_NamedChromaticPitchSet___slots___01():
    '''Named chromatic pitch sets are immutable.
    '''

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_set = pitchtools.NamedChromaticPitchSet(ncps)

    assert py.test.raises(AttributeError, "named_chromatic_pitch_set.foo = 'bar'")
